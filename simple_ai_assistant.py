from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))
messages: list[ChatCompletionMessageParam] = []
while True:
    user_input = input("\nYOU: ")

    if user_input in ["exit", "bye", "goodbye"]:
        break

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b", messages=messages
    )

    reply = response.choices[0].message.content
    if reply is None:
        raise RuntimeError("The model returned no text content.")

    print("ASSISTANT: ", reply)
    messages.append({"role": "assistant", "content": reply})
