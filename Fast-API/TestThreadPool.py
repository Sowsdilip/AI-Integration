import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://localhost:8000/slow-def"

def call_api(i):
    start = time.time()

    response = requests.get(URL)

    elapsed = time.time() - start

    return i, response.status_code, elapsed


start = time.time()

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = [
        executor.submit(call_api, i)
        for i in range(50)
    ]

    for future in as_completed(futures):
        i, status, elapsed = future.result()
        print(f"Request {i:02d}: {status} - {elapsed:.2f}s")

print(f"\nTotal time: {time.time() - start:.2f}s")
