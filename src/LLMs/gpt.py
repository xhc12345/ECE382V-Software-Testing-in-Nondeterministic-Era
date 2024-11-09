import time
from openai import OpenAI
import os
import json

# Initialize the API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI API Key = ", OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)


def get_chatgpt_response(prompt):
    start_time = time.time()
    response = client.chat.completions.with_raw_response.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=5000,
        top_p=1,
    )
    # print(response.headers.get("x-ratelimit-limit-tokens"))

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"GPT Reponse Time: {time_taken:.3f}s")

    # get the object that `chat.completions.create()` would have returned
    response = response.parse()
    # print(response)
    return response.choices[0].message.content


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    response = get_chatgpt_response(prompt)
    print(response)
