import time
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv(dotenv_path=".env")

# Initialize the API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print("GOOGLE API Key = ", GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
client = genai.GenerativeModel("gemini-1.5-flash")

chat = client.start_chat()


def get_gemini_response(prompt: str) -> str:
    global chat
    start_time = time.time()

    # response = client.generate_content(prompt)
    response = chat.send_message(prompt)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Gemini Reponse Time: {time_taken:.3f}s")

    # print(response.text)
    return response.text


def reset_gemini_conversation():
    global chat
    chat = client.start_chat()
    print("Cleared Gemini conversation.")


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    print("Prompt:", prompt)
    response = get_gemini_response(prompt)
    print(response)
    print()

    prompt = "What was my previous question?"
    print("Prompt:", prompt)
    response = get_gemini_response(prompt)
    print(response)
    print()

    reset_gemini_conversation()
    prompt = "What was my previous question?"
    response = get_gemini_response(prompt)
    print(response)
    print()
