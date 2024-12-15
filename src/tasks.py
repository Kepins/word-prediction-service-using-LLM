import asyncio
import json
from threading import Event

import torch
from transformers import LlamaForCausalLM, PreTrainedTokenizerFast, pipeline

from redis.asyncio import Redis

BATCH_SIZE = 128

def has_alnum(s: str):
    return any(c.isalnum() for c in s)

def first_word(s: str):
    s = s.rstrip()
    space_idx = s.find(' ')
    while space_idx != -1 and not has_alnum(s[:space_idx]):
        space_idx = s.find(' ', space_idx + 1)
    return s[:space_idx] if space_idx != -1 else s


async def inference(stop_event: Event):
    redis = Redis(host='redis', port=6379, db=0)
    pubsub = redis.pubsub()
    await pubsub.psubscribe('__keyspace@0__:PROMPT_QUEUE')

    model_id = './resources/models/Llama-3.2-1B'
    model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, attn_implementation="flash_attention_2")
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_id, padding_side='left')

    # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
    model.generation_config.pad_token_id = model.generation_config.eos_token_id

    pipe = pipeline(
        'text-generation',
        model=model,
        tokenizer=tokenizer,
        device=0,
        max_new_tokens=5,  # Limit to 5 tokens
        batch_size=BATCH_SIZE,
    )

    # Enable batching
    pipe.tokenizer.pad_token_id = model.config.eos_token_id

    stop_event_task = asyncio.create_task(stop_event.wait())

    while True:
        prompts_raw = await redis.lpop("PROMPT_QUEUE", BATCH_SIZE)
        if prompts_raw:
            prompts_dict = [json.loads(p.decode()) for p in prompts_raw]
            prompts_ids = [p["prompt_id"] for p in prompts_dict]
            prompts = [p["prompt"] for p in prompts_dict]

            responses = pipe(prompts)
            for prompt_id, prompt, response in zip(prompts_ids, prompts, responses, strict=False):
                new_text = response[0]['generated_text'].replace(prompt, '', 1)
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
