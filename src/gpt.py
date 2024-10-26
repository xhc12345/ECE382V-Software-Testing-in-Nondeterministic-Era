from openai import OpenAI
import os
import json

# Initialize the API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI API Key = ", OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)


def get_chatgpt_response(prompt):
    response = client.chat.completions.with_raw_response.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=64,
        top_p=1,
    )
    # print(response.headers.get("x-ratelimit-limit-tokens"))

    # get the object that `chat.completions.create()` would have returned
    response = response.parse()
    # print(response)
    return response.choices[0].message.content
