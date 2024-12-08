import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis

from .routers import example
from .tasks import inference

context = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    context["redis"] = Redis(host='redis', port=6379, db=0)
    stop_event = asyncio.Event()
    context["stop_event"] = stop_event
    # Start the inference loop
    context["inference_task"] = asyncio.create_task(inference(stop_event))
    yield
    # Stop the inference loop
    stop_event.set()
    await context["redis"].close()

app = FastAPI(
    title='Word prediction service',
    description='Word prediction service using LLM',
    version='0.1',
    lifespan=lifespan,
)

app.include_router(example.router)
