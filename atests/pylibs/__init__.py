import asyncio
import time
from gevent import joinall, spawn, pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def sleep_threading(iterations: int, seconds: int):
    with ThreadPoolExecutor(10) as t:
        futures = [t.submit(time.sleep, seconds) for _ in range(iterations)]

        for f in futures:
            f.result()


def sleep_processing(iterations: int, seconds: int):
    with ProcessPoolExecutor(10) as t:
        futures = [t.submit(time.sleep, seconds) for _ in range(iterations)]

        for f in futures:
            f.result()


def sleep_gevent_coros(iterations: int, seconds: int):
    jobs = [spawn(time.sleep, seconds) for _ in range(iterations)]
    _ = joinall(jobs, timeout=30)


def sleep_asyncio(iterations: int, seconds: int):
    async def do_something():
        jobs = [asyncio.sleep(seconds) for _ in range(iterations)]
        _ = await asyncio.gather(*jobs)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_something())
