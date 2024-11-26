import asyncio
import aiohttp
import time
from itertools import cycle

# Configurations for testing distributed KV stores
BASE_URLS_LISTS = [
    ['http://127.0.0.1:8081'],  # Single node
    ['http://127.0.0.1:8081', 'http://127.0.0.1:8082'],  # Two nodes
    ['http://127.0.0.1:8081', 'http://127.0.0.1:8082', 'http://127.0.0.1:8083']  # Three nodes
]

# Total operations and concurrency settings
NUM_OPERATIONS = 600  # Total operations (split between set, get, delete)
CONCURRENCY = 250     # Number of concurrent operations

# Queue for latencies to calculate performance
latencies = []

# Single KV store operation (async)
async def kv_store_operation(session, op_type, key, value=None, node_iterator=None):
    try:
        base_url = next(node_iterator)  # Use round-robin to pick a node
        start_time = time.time()  # Start timing

        if op_type == 'set':
            async with session.post(f"{base_url}/{key}", json={'value': value}) as response:
                await response.text()
        elif op_type == 'get':
            async with session.get(f"{base_url}/{key}") as response:
                await response.text()
        elif op_type == 'delete':
            async with session.delete(f"{base_url}/{key}") as response:
                await response.text()

        latency = time.time() - start_time  # Calculate latency
        latencies.append(latency)  # Store latency
    except Exception as e:
        pass  # Ignore errors for maximum throughput

# Worker coroutine function
async def worker(operations, base_urls):
    node_iterator = cycle(base_urls)  # Create a round-robin iterator for nodes
    async with aiohttp.ClientSession() as session:
        tasks = [kv_store_operation(session, op, key, value, node_iterator) for op, key, value in operations]
        await asyncio.gather(*tasks)  # Concurrent execution

# Main benchmark function
async def test_kv_store(base_urls, num_operations, concurrency):
    # Prepare operations: 1/3 'set', 1/3 'get', 1/3 'delete'
    operations = []
    for i in range(num_operations // 3):
        operations.append(('set', f'key_{i}', f'value_{i}'))
    for i in range(num_operations // 3):
        operations.append(('get', f'key_{i}', None))
    for i in range(num_operations // 3):
        operations.append(('delete', f'key_{i}', None))

    # Divide operations into batches for concurrent execution
    operation_batches = [operations[i:i + concurrency] for i in range(0, len(operations), concurrency)]

    # Start benchmark
    start_time = time.time()
    for batch in operation_batches:
        await worker(batch, base_urls)
    total_time = time.time() - start_time

    # Calculate final results
    total_ops = num_operations
    throughput = total_ops / total_time
    return total_ops, total_time, throughput

# Main program
async def main():
    results = []
    for base_urls in BASE_URLS_LISTS:
        total_ops, total_time, throughput = await test_kv_store(base_urls, NUM_OPERATIONS, CONCURRENCY)
        results.append((len(base_urls), total_ops, total_time, throughput))

    # Print final results
    print("\nFinal Results:")
    for num_nodes, total_ops, total_time, throughput in results:
        print(f"Nodes: {num_nodes}, Total operations: {total_ops}, Total time: {total_time:.2f} seconds, "
              f"Throughput: {throughput:.2f} ops/sec")

if __name__ == '__main__':
    asyncio.run(main())
