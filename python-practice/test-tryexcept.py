import json

raw_text = '{"message":"hi"}'

try:
    result = json.loads(raw_text)
except json.JSONDecodeError as e:
    print("Bad JSON:", e)
except Exception as e:
    print("Something else went wrong:", e)
else:
    print("Parsed successfully:", result)
finally:
    print("This always runs, error or not")