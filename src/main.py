import openai
import os

# Initialize the API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]


# Example usage
if __name__ == "__main__":
    prompt = "Tell me a fun fact about space."
    response = get_chatgpt_response(prompt)
    print(response)

    # Write the response to a file in the /data directory
    with open("/data/output.txt", "w") as file:
        file.write(response)
