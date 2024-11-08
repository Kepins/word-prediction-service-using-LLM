import torch
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, LlamaForCausalLM, pipeline

router = APIRouter(
    prefix='',
    responses={404: {'description': 'Not found'}},
)


class ResponseModel(BaseModel):
    """Response Model"""

    response: str


@router.put(
    '/',
    summary='Returns next token from LLM',
    description='Returns a next token generated from prompt.',
    response_model=ResponseModel,
)
def generate_next_token(prompt: str):
    """Returns the next token generated by LLaMA based on the prompt.

    - **prompt**: The prompt text to base the next token generation on.

    Example response:
    - **response**: The next token generated from the prompt.
    """
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
    return {'response': next_token}
