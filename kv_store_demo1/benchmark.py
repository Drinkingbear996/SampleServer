import time
import requests
import random

# Define the base URLs for the three container instances
BASE_URLS = ["http://localhost:8081", "http://localhost:8082", "http://localhost:8083"]

NUM_REQUESTS = 100  # Number of requests to be sent for each operation


def put(key, value):
    """
    Sends a PUT request to store a key-value pair.
    Randomly selects one of the instances to handle the request.
    """
    url = random.choice(BASE_URLS)  # Randomly choose an instance
    response = requests.post(f"{url}/{key}", json={"value": value})
    return response.json()


def get(key):
    """
    Sends a GET request to retrieve the value for a given key.
    Randomly selects one of the instances to handle the request.
    """
    url = random.choice(BASE_URLS)
    response = requests.get(f"{url}/{key}")
    return response.json()


def delete(key):
    """
    Sends a DELETE request to remove a key-value pair.
    Randomly selects one of the instances to handle the request.
    """
    url = random.choice(BASE_URLS)
    response = requests.delete(f"{url}/{key}")
    return response.json()


def run_benchmark():
    """
    Runs the benchmark tests for PUT, GET, and DELETE operations.
    Measures throughput, latency, and total time for each operation type.
    """
    start_time = time.time()

    # Test PUT requests
    put_start_time = time.time()
    for i in range(NUM_REQUESTS):
        put(f"key_{i}", f"value_{i}")
    put_end_time = time.time()

    # Test GET requests
    get_start_time = time.time()
    for i in range(NUM_REQUESTS):
        get(f"key_{i}")
    get_end_time = time.time()

    # Test DELETE requests
    delete_start_time = time.time()
    for i in range(NUM_REQUESTS):
        delete(f"key_{i}")
    delete_end_time = time.time()

    # Calculate time metrics
    total_time = time.time() - start_time
    put_time = put_end_time - put_start_time
    get_time = get_end_time - get_start_time
    delete_time = delete_end_time - delete_start_time

    # Calculate throughput and latency
    throughput = (NUM_REQUESTS * 3) / total_time
    put_throughput = NUM_REQUESTS / put_time
    get_throughput = NUM_REQUESTS / get_time
    delete_throughput = NUM_REQUESTS / delete_time

    # Output the results
    print("\nBenchmark Results:")
    print(f"Total operations: {NUM_REQUESTS * 3}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Overall Throughput: {throughput:.2f} operations per second")
    print(f"PUT Throughput: {put_throughput:.2f} operations per second")
    print(f"GET Throughput: {get_throughput:.2f} operations per second")
    print(f"DELETE Throughput: {delete_throughput:.2f} operations per second")
    print(f"PUT Latency: {put_time / NUM_REQUESTS:.5f} seconds per operation")
    print(f"GET Latency: {get_time / NUM_REQUESTS:.5f} seconds per operation")
    print(f"DELETE Latency: {delete_time / NUM_REQUESTS:.5f} seconds per operation")


if __name__ == "__main__":
    run_benchmark()
