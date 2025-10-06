import os

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API key found! ✅")
else:
    print("API key NOT found. ❌")
