import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def hit(path):
    start = time.perf_counter()
    urllib.request.urlopen(f"http://127.0.0.1:8000{path}").read()
    return time.perf_counter() - start


for path in ("/slow-async", "/slow-blocking"):
    total_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as pool:
        times = list(pool.map(hit, [path, path]))
    total = time.perf_counter() - total_start