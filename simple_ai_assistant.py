from tools import TOOLS, FUNCTIONS_NAME_TO_FUNCTION
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

messages: list[ChatCompletionMessageParam] = []

messages.append(
    {
        "role": "system",
        "content": "Act as Intelligent Mentor. Who guides the student to solve the problem by thier own.",
    }
)
while True:
    user_input = input("\nYOU: ")

    if user_input in ["exit", "bye", "goodbye"]:
        break

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        tools=TOOLS,
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")
            tool_function = FUNCTIONS_NAME_TO_FUNCTION[func_name]
            result = tool_function(**func_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

        # 2nd api call to get the final response after tool call
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
        )

        msg = response.choices[0].message

    messages.append(
        {
            "role": "assistant",
            "content": msg.content,
        }
    )

    print(f"\nAI: {msg.content}")
