from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # loads OPENAI_API_KEY from .env

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY not found. Check your .env file.")
    print("Current working directory:", os.getcwd())
    print(".env path should be:", os.path.join(os.getcwd(), ".env"))
else:
    print("API key found (first 10 chars):", api_key[:10])

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what a resume is in 2 sentences."}
    ]
)

print(response.choices[0].message.content)