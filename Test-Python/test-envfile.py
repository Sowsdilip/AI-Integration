import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api-key")
print("api-key from env file ")
print(api_key[:10])