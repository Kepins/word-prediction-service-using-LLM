from fastapi import FastAPI

from .routers import example

app = FastAPI(
    title='Word prediction service',
    description='Word prediction service using LLM',
    version='0.1',
)

app.include_router(example.router)
