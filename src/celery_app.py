import time

import torch
from celery import Celery
from redis import Redis
from transformers import AutoTokenizer, LlamaForCausalLM, pipeline

celery_app = Celery(__name__)


@celery_app.task()
def inference():
    redis = Redis(host='redis', port=6379, db=0)
    lock_acquired = redis.set("GENERATE_NEXT_TOKENS", "locked", nx=True, ex=60)
    if not lock_acquired:
        print("LOCK NOT ACQUIRED")
        return

    prompts = redis.lpop("PROMPT_QUEUE", 2)

    time.sleep(2)

    print(prompts)

    # model_id = './Llama-3.2-1B'
    # model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    # tokenizer = AutoTokenizer.from_pretrained(model_id)
    #
    # pipe = pipeline(
    #     'text-generation',
    #     model=model,
    #     tokenizer=tokenizer,
    #     device=0,
    #     max_new_tokens=1,  # Limit to one token
    # )
    # responses = pipe(prompt)
    # next_token = responses[0]['generated_text'].replace(prompt, '').strip()

    redis.delete("GENERATE_NEXT_TOKENS")
    return "next_token"
