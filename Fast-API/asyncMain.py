import asyncio
import time

from fastapi import FastAPI,Request


app = FastAPI()

@app.middleware("http")
async def log_processing_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)          # runs the actual endpoint
    elapsed = time.perf_counter() - start
    print(f"{request.method} {request.url.path} took {elapsed:.2f}s")
    response.headers["X-Process-Time"] = f"{elapsed:.2f}"
    return response

@app.get("/slow-async")
async def slowAsync():
    await asyncio.sleep(5)
    return{"type":"async"}

@app.get("/slow-blocking")
async def slowBlocking():
    time.sleep(5)
    return{"type":"blocking"}


