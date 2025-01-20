import concurrent.futures
import random
import statistics
import time

from ollama import generate

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

# Function to send a single PUT request
def send_request():
    try:
        start_time = time.time()
        response = generate(model='llama3.2', prompt=random.choice(PROMPTS), options={"stop": [" "]})
        end_time = time.time()
        return 200, response["response"], (end_time - start_time)
    except Exception as e:
        return None, str(e), None

num_requests = 1024  # Total number of requests
max_workers = 1024  # Maximum number of concurrent workers

# Function to run the stress test
def run_stress_test():
    print(f"Starting stress test with {num_requests} requests and {max_workers} workers...")

    results = []
    response_times = []
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            if result[2] is not None:
                response_times.append(result[2])
    duration = time.time() - start_time
    print(f"Time per prompt: {duration / num_requests} seconds")

    # Log results
    success_count = sum(1 for result in results if result[0] == 200)
    failure_count = len(results) - success_count

    print(f"\nStress Test Results:")
    print(f"Successful requests: {success_count}")
    print(f"Failed requests: {failure_count}")

    if response_times:
        avg_time = statistics.mean(response_times)
        std_dev_time = statistics.stdev(response_times)
        max_time = max(response_times)
        min_time = min(response_times)

        print(f"\nResponse Time Metrics:")
        print(f"Average time: {avg_time:.4f} seconds")
        print(f"Standard deviation: {std_dev_time:.4f} seconds")
        print(f"Max time: {max_time:.4f} seconds")
        print(f"Min time: {min_time:.4f} seconds")

    if failure_count > 0:
        print(f"\nErrors:")
        for status, error, _ in results:
            if status != 200:
                print(error)

if __name__ == "__main__":
    run_stress_test()
