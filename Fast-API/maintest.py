from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/slow-def")
def slow_def():
    time.sleep(5)
    return {"type": "def"}
