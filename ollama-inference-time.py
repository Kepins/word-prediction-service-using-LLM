import asyncio
import time

from ollama import AsyncClient

PROMPTS = [
    "Kocham czytać ",
    "Lubię biegać po ",
    "Czuję radość, gdy słucham ",
    "Pamiętam wspaniałe chwile z ",
    "Chciałbym odwiedzić ",
    "Widzę piękne krajobrazy w tym ",
    "Jem smaczne jedzenie z ",
    "Lubię rozmawiać o ",
    "Czuję się szczęśliwy, gdy ",
    "Kocham oglądać zachody ",
    "Biegam codziennie ",
    "Pamiętam każdą podróż, którą ",
    "Lubię gotować nowe ",
    "Chciałbym poznać nowe ",
    "Widzę w przyszłości wiele ",
    "Czuję spokój, gdy ",
]

def n_prompts(n: int) -> list[str]:
    return [PROMPTS[i % len(PROMPTS)] for i in range(n)]

async def generate_responses(prompts, async_client):
    tasks = [
        async_client.generate(model='llama3.2', prompt=prompt, options={"stop": [" "]})
        for prompt in prompts
    ]
    # Run all tasks concurrently
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses

async def main():
    prompts = n_prompts(1024)
    async_client = AsyncClient()
    start_time = time.time()
    responses = await generate_responses(prompts, async_client)
    duration = time.time() - start_time
    print(f"Time per prompt: {duration / len(prompts)} seconds")

if __name__ == "__main__":
    asyncio.run(main())
