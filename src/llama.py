from meta_ai_api import MetaAI

client = MetaAI()


def get_llama_response(prompt):
    response = client.prompt(message=prompt)
    # print(response)
    return response["message"]


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    response = get_llama_response(prompt)
    print(response)
