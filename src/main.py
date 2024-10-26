# Example usage
from gemini import get_gemini_response
from gpt import get_chatgpt_response


def main():
    print("Prompt")
    prompt = "Tell me a short fun fact about space."
    print(prompt)
    print()

    print("ChatGPT:")
    gpt_response = get_chatgpt_response(prompt)
    print(gpt_response)
    with open("/data/gpt_output.txt", "w") as file:
        file.write(gpt_response)
    print()

    print("Gemini:")
    gemini_response = get_gemini_response(prompt)
    print(gemini_response)
    with open("/data/gemini_output.txt", "w") as file:
        file.write(gemini_response)
    print()


if __name__ == "__main__":
    main()
