import asyncio
import aiohttp
import time
from itertools import cycle

# Configure the base URLs for the KV store instances
BASE_URLS_LISTS = [
    ['http://127.0.0.1:8081'],                      # Single node
    ['http://127.0.0.1:8081', 'http://127.0.0.1:8082'],  # Two nodes
    ['http://127.0.0.1:8081', 'http://127.0.0.1:8082', 'http://127.0.0.1:8083']  # Three nodes
]

# Configure the number of operations and concurrency
NUM_OPERATIONS = 600  # Total number of operations
CONCURRENCY = 250     # Concurrency level

# To store latencies
latencies = []

# Single KV store operation (async)
async def kv_store_operation(session, op_type, key, value=None, node_iterator=None):
    try:
        base_url = next(node_iterator)  # Round-robin node selection
        start_time = time.time()  # Start timing
        if op_type == 'set':
            async with session.post(f"{base_url}/{key}", json={'value': value}) as response:
                await response.text()
        elif op_type == 'get':
            async with session.get(f"{base_url}/{key}") as response:
                await response.text()
        elif op_type == 'delete':  # Add delete operation
            async with session.delete(f"{base_url}/{key}") as response:
                await response.text()
        latency = time.time() - start_time  # Measure latency
        latencies.append(latency)  # Record latency
    except Exception as e:
        pass  # Ignore errors to maximize throughput

# Worker coroutine function
async def worker(operations, base_urls):
    node_iterator = cycle(base_urls)  # Create node iterator
    async with aiohttp.ClientSession() as session:
        tasks = [kv_store_operation(session, op, key, value, node_iterator) for op, key, value in operations]
        await asyncio.gather(*tasks)  # Execute operations concurrently

# Main testing function
async def test_kv_store(base_urls, num_operations, concurrency):
    # Prepare operations
    operations = []
    for i in range(num_operations // 3):  # Split equally between 'set', 'get', 'delete'
        operations.append(('set', f'key_{i}', f'value_{i}'))
        operations.append(('get', f'key_{i}', None))
        operations.append(('delete', f'key_{i}', None))

    # Divide operations into batches
    operation_batches = [operations[i:i + concurrency] for i in range(0, len(operations), concurrency)]

    # Start benchmark
    start_time = time.time()
    for batch in operation_batches:
        await worker(batch, base_urls)
    total_time = time.time() - start_time

    # Calculate final results
    total_ops = len(operations)
    throughput = total_ops / total_time
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    return total_ops, total_time, throughput, avg_latency

# Main program
async def main():
    results = []
    for base_urls in BASE_URLS_LISTS:
        total_ops, total_time, throughput, avg_latency = await test_kv_store(base_urls, NUM_OPERATIONS, CONCURRENCY)
        results.append((len(base_urls), total_ops, total_time, throughput, avg_latency))

    # Print final results
    print("\nFinal Results:")
    for num_nodes, total_ops, total_time, throughput, avg_latency in results:
        print(f"Nodes: {num_nodes}, Total operations: {total_ops}, Total time: {total_time:.2f} seconds, "
              f"Throughput: {throughput:.2f} operations per second, "
              f"Average Latency: {avg_latency:.5f} seconds per operation")

if __name__ == '__main__':
    asyncio.run(main())
