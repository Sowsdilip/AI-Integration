import time,random

class TransientError(Exception):
    pass

calls = 0
def call_claude_api():
    global calls
    calls += 1
    print(f"call #{calls}")
    if calls <= 5:
        raise TransientError("temporary")
    return "success"

def call_with_retry_count(fn,base_delay = 1.0,max_attempts = 4, max_delay = 10.0):
    for attempt in range(max_attempts):
        print(f"attempt  {attempt}")
        try:
            return fn()
        except TransientError as e:
            print("Transient error")
            if attempt == max_attempts-1:     
                raise TransientError("max attempts reached no more reties") from e
            delay =  min(max_delay, base_delay * 2 ** attempt) + random.uniform(0, 0.5)  
            print(f"transient failure, retrying in {delay:.2f}s")  
            time.sleep(delay)   


print(call_with_retry_count(call_claude_api))

    