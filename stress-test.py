import concurrent.futures
import random
import http.client
import json
import time
import statistics

# Define the endpoint and predefined list of values
host = "127.0.0.1"
port = 8080
url = "/"
payload_values = prompts = [
    "Dzień dobry, jak się",
    "Na obiad ugotuję zupę",
    "Czy mogę prosić o trochę",
    "Idziemy dzisiaj na spacer do",
    "Pogoda jest dzisiaj bardzo",
    "Wczoraj wieczorem oglądałem świetny",
    "Chciałbym pojechać na wakacje do",
    "Poproszę o kawę z mlekiem i",
    "W sobotę wybieramy się na",
    "Na śniadanie zjadłam chleb z",
    "Czy widziałeś mój nowy",
    "W weekend planujemy malować ściany na",
    "Do szkoły zawsze noszę w plecaku",
    "Mój ulubiony owoc to",
    "Czy pomożesz mi znaleźć moje",
    "Książka, którą ostatnio czytałem, była bardzo",
    "Na urodziny dostałem piękny",
    "Proszę zapisać to na kartce",
    "Wieczorem pójdziemy do kina na",
    "Moim ulubionym kolorem jest",
]


# Function to send a single PUT request
def send_request():
    payload = {"prompt": random.choice(payload_values)}
    headers = {"Content-Type": "application/json"}
    try:
        conn = http.client.HTTPConnection(host, port)
        start_time = time.time()
        conn.request("PUT", url, json.dumps(payload), headers)
        response = conn.getresponse()
        end_time = time.time()
        return response.status, response.read().decode(), (end_time - start_time)
    except Exception as e:
        return None, str(e), None
    finally:
        conn.close()


# Stress test configuration
num_requests = 10000  # Total number of requests
max_workers = 100  # Maximum number of concurrent workers


# Function to run the stress test
def run_stress_test():
    print(f"Starting stress test with {num_requests} requests and {max_workers} workers...")

    results = []
    response_times = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            if result[2] is not None:
                response_times.append(result[2])

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
