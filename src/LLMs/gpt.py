import sys
import time
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

# from src.prompts.read_prompt import get_prompt

load_dotenv(dotenv_path=".env")
TIME_LIMIT = 180.0  # up to 180 seconds for each response

# Initialize the API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI API Key = ", OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

assistant = client.beta.assistants.create(
    name="FlakyDetector",
    # instructions=get_prompt("praise_the_LLM"),
    # instructions="You are a flaky test detection tool.",
    # instructions="You are an expert astronomer",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
)

thread = client.beta.threads.create()


def get_chatgpt_response(prompt: str) -> str | None:
    global thread
    start_time = time.time()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        # instructions="Answer the user's question",
    )

    while (time.time() - start_time) < TIME_LIMIT:
        if run.status == "completed":
            break
    else:
        print("TIME OUT FOR GPT", file=sys.stderr)
        return None

    end_time = time.time()
    time_taken = end_time - start_time
    # print(f"GPT Reponse Time: {time_taken:.3f}s")

    # get the object that `chat.completions.create()` would have returned
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    # print(json.dumps(messages.to_dict(), indent=4))
    # print(response)
    return messages.data[0].content[0].text.value


def reset_chatgpt_conversation():
    global thread
    thread = client.beta.threads.create()
    print("Cleared ChatGPT conversation.")


def single_get_chatgpt_response(prompt):
    """
    old version with no ability to maintain conversation
    """
    start_time = time.time()
    response = client.chat.completions.with_raw_response.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        # max_tokens=25600,
        top_p=1,
    )
    # print(response.headers.get("x-ratelimit-limit-tokens"))

    end_time = time.time()
    time_taken = end_time - start_time
    # print(f"GPT Reponse Time: {time_taken:.3f}s")

    # get the object that `chat.completions.create()` would have returned
    response = response.parse()
    # print(response)
    return response.choices[0].message.content


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    print("Prompt:", prompt)
    response = get_chatgpt_response(prompt)
    print(response)
    print()

    prompt = "Why did the United States fight for independence?"
    print("Prompt:", prompt)
    response = single_get_chatgpt_response(prompt)
    print(response)
    print()

    prompt = "What was my previous question?"
    print("Prompt:", prompt)
    response = get_chatgpt_response(prompt)
    print(response)
    print()

    reset_chatgpt_conversation()
    print()

    prompt = "What was my previous question?"
    print("Prompt:", prompt)
    response = get_chatgpt_response(prompt)
    print(response)
    print()
