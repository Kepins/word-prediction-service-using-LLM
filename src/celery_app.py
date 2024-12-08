import torch
from celery import Celery
from transformers import AutoTokenizer, LlamaForCausalLM, pipeline


celery_app = Celery(__name__)


@celery_app.task()
def inference(prompt):
    model_id = './Llama-3.2-1B'
    model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    pipe = pipeline(
        'text-generation',
        model=model,
        tokenizer=tokenizer,
        device=0,
        max_new_tokens=1,  # Limit to one token
    )
    responses = pipe(prompt)
    next_token = responses[0]['generated_text'].replace(prompt, '').strip()
    return next_token