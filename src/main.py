from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis

from .routers import example

context = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    context["redis"] = Redis(host='redis', port=6379, db=0)
    yield
    await context["redis"].close()
app = FastAPI(
    title='Word prediction service',
    description='Word prediction service using LLM',
    version='0.1',
    lifespan=lifespan,
)

app.include_router(example.router)
