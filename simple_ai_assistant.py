from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

while True:
    user_input = input("\nYOU: ")
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b", messages=[{"role": "user", "content": user_input}]
    )
    print("ASSISTANT: ", response.choices[0].message.content)
