import asyncio
import datetime
import httpx

client = httpx.AsyncClient()

URL = 'http://127.0.0.1:5000/'
CONCURRENCY = 10
NUM_REQUESTS = 40

class C:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

async def make_request(semaphore):
    async with semaphore:
        try:
            timeout_ms = 500
            respond_by = datetime.datetime.now() + datetime.timedelta(milliseconds=timeout_ms)
            resp = await client.get(
                URL,
                headers={ 'X-Respond-By' : respond_by.isoformat() },
                timeout=timeout_ms / 1000
            )

            resp.raise_for_status()
            print(f'{C.GREEN}.{C.RESET}', end='', flush=True)
        except:
            print(f'{C.RED}X{C.RESET}', end='', flush=True)


async def main():
    global CONCURRENCY
    print()
    print('Simulating a thundering herd...')
    print(f'Executing {NUM_REQUESTS} requests with {CONCURRENCY} connections')
    print()

    semaphore = asyncio.Semaphore(CONCURRENCY)
    await asyncio.gather(*[
        make_request(semaphore)
        for idx in range(NUM_REQUESTS)
    ])

    CONCURRENCY = 2
    print()
    print()
    print('Now simulating traffic at normal levels')
    print(f'Executing {NUM_REQUESTS} requests with {CONCURRENCY} connections')
    print()

    semaphore = asyncio.Semaphore(CONCURRENCY)
    await asyncio.gather(*[
        make_request(semaphore)
        for idx in range(NUM_REQUESTS)
    ])




asyncio.run(main())
# asyncio.run(make_request(asyncio.Semaphore(100)))
asyncio.run(client.aclose())
