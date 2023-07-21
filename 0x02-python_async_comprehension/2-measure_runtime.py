#!/usr/bin/env python3
"""
Import async_comprehension from the previous file and write a measure_runtime
coroutine that will execute async_comprehension
four times in parallel using asyncio.gather.

measure_runtime should measure the total runtime and return it

Notice that the total runtime is roughly 10 seconds, explain it to yourself.
"""
from time import perf_counter
from asyncio import gather
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measures the runtime of async_comprehension() when run
    concurrently 4 times"""
    start: float = perf_counter()
    await gather(*(async_comprehension() for i in range(4)))
    return perf_counter() - start
