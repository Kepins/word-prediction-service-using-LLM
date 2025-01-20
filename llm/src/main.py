import asyncio
import json
import signal

import torch
from transformers import (
    LlamaForCausalLM,
    PreTrainedTokenizerFast,
    pipeline,
    LlamaTokenizer,
    StoppingCriteriaList,
    StoppingCriteria,
)

from redis.asyncio import Redis

BATCH_SIZE = 64


def has_alnum(s: str):
    return any(c.isalnum() for c in s)


def first_word(s: str):
    s = s.rstrip()
    space_idx = s.find(' ')
    while space_idx != -1 and not has_alnum(s[:space_idx]):
        space_idx = s.find(' ', space_idx + 1)
    return s[:space_idx] if space_idx != -1 else s


class StopAfterOneFullWord(StoppingCriteria):
    def __init__(self, tokenizer, prompts_lengths):
        self.tokenizer = tokenizer
        self.prompts_lengths = prompts_lengths
        self.finished_sequences = set()  # Track sequences that generated one full word

    def __call__(self, input_ids, scores, **kwargs):
        batch_size = input_ids.shape[0]
        # Loop over each sequence in the batch
        for batch_idx in range(batch_size):
            if batch_idx in self.finished_sequences:
                continue  # Skip sequences that already generated one full word
            # Decode the sequence so far
            decoded_text = self.tokenizer.decode(input_ids[batch_idx], skip_special_tokens=True)
            # Check if at least one new full word (with space after) was generated
            if ' ' in decoded_text[self.prompts_lengths[batch_idx] + 1 :]:
                self.finished_sequences.add(batch_idx)
        # Stop generation when all sequences have generated at least one new word
        return len(self.finished_sequences) == batch_size


async def inference(stop_event):
    redis = Redis(host='redis', port=6379, db=0)
    pubsub = redis.pubsub()
    await pubsub.psubscribe('__keyspace@0__:PROMPT_QUEUE')

    model_id = './resources/models/Qra-1B'
    model = LlamaForCausalLM.from_pretrained(
        model_id, torch_dtype=torch.bfloat16, device_map=0
    )
    tokenizer = LlamaTokenizer.from_pretrained(model_id, padding_side='left')

    # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
    model.generation_config.pad_token_id = model.generation_config.eos_token_id

    pipe = pipeline(
        'text-generation',
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=10,  # Limit to 10 tokens
        batch_size=BATCH_SIZE,
    )

    # Enable batching
    pipe.tokenizer.pad_token_id = model.config.eos_token_id

    stop_event_task = asyncio.create_task(stop_event.wait())

    while True:
        prompts_raw = await redis.lpop('PROMPT_QUEUE', BATCH_SIZE)
        if prompts_raw:
            prompts_dict = [json.loads(p.decode()) for p in prompts_raw]
            prompts_ids = [p['prompt_id'] for p in prompts_dict]
            prompts = [p['prompt'] for p in prompts_dict]
            prompts_lengths = [len(p) for p in prompts]

            stopping_criteria = StoppingCriteriaList([StopAfterOneFullWord(tokenizer, prompts_lengths)])

            responses = pipe(
                prompts,
                stopping_criteria=stopping_criteria,
            )

            for idx_batch, (prompt_id, prompt, response) in enumerate(zip(prompts_ids, prompts, responses)):
                new_text = response[0]['generated_text'][prompts_lengths[idx_batch] :]
                next_word = first_word(new_text)
                await redis.set(prompt_id, next_word, ex=60)

        # Prepare the wait for either the stop_event or PubSub message
        tasks = [
            asyncio.create_task(pubsub.get_message(ignore_subscribe_messages=True)),
            stop_event_task,
        ]

        # Wait for the first event to occur (either pubsub message or stop_event)
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            if task is tasks[1]:  # If stop_event was triggered
                await pubsub.unsubscribe()
                await pubsub.close()
                return

            if task is tasks[0]:  # If a PubSub message was received
                message = task.result()
                if message and message['type'] == 'pmessage' and message['data'] == b'rpush':
                    break


def shutdown_handler(signum, frame, stop_event):
    stop_event.set()  # Trigger the stop event


if __name__ == '__main__':
    stop_event = asyncio.Event()

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, lambda signum, frame: shutdown_handler(signum, frame, stop_event))
    signal.signal(signal.SIGINT, lambda signum, frame: shutdown_handler(signum, frame, stop_event))

    asyncio.run(inference(stop_event))
