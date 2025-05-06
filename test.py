import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
api_key = os.getenv('BINANCE_API_KEY')
secret = os.getenv('BINANCE_API_SECRET')


print(OPENAI_API_KEY)
print(api_key)
print(secret)