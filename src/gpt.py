from openai import OpenAI
import os

# Initialize the API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)


def get_chatgpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=64,
        top_p=1,
    )
    return response["choices"][0]["message"]["content"]
