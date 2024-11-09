import time
import google.generativeai as genai
import os

# Initialize the API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print("GOOGLE API Key = ", GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
client = genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(prompt):
    start_time = time.time()

    response = client.generate_content(prompt)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Gemini Reponse Time: {time_taken:.3f}s")

    # print(response.text)
    return response.text


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    response = get_gemini_response(prompt)
    print(response)
