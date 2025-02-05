import json
import uuid

from fastapi import APIRouter
from pydantic import BaseModel, Field

from redis.asyncio import Redis

router = APIRouter(
    prefix='',
    responses={404: {'description': 'Not found'}},
)


class InputModel(BaseModel):
    prompt: str = Field(..., max_length=500)


class ResponseModel(BaseModel):
    """Response Model"""

    response: str


@router.put(
    '/',
    summary='Returns next word from QRA-1B LLM',
    description='Returns a next word generated from prompt.',
    response_model=ResponseModel,
)
async def generate_next_token(input: InputModel):
    """Returns the next word generated by QRA-1B based on the prompt.

    - **prompt**: The prompt text to base the next word generation on.

    Example response:
    - **response**: The next word generated from the prompt.
    """
    from ..main import context
    redis: Redis = context["redis"]
    pubsub = redis.pubsub()

    prompt_id = str(uuid.uuid4())
    prompt = input.prompt
    await pubsub.psubscribe(f'__keyspace@0__:{prompt_id}')
    await redis.rpush("PROMPT_QUEUE", json.dumps({"prompt_id": prompt_id, "prompt": prompt}))

    async for message in pubsub.listen():
        if message['type'] == 'pmessage' and message['data'] == b'set':
            # token has been generated
            break
    response_token = await redis.getdel(prompt_id)

    await pubsub.unsubscribe()
    await pubsub.close()
    return {"response": response_token.decode('utf-8')}
