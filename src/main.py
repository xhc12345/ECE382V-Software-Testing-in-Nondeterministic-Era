# Example usage
from gpt import get_chatgpt_response


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    print(prompt)
    response = get_chatgpt_response(prompt)
    print(response)

    # Write the response to a file in the /data directory
    with open("/data/output.txt", "w") as file:
        file.write(response)
