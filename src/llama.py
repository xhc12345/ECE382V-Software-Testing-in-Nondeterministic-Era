from meta_ai_api import MetaAI

prompt = "Tell me a short fun fact about space."

client = MetaAI()


def get_llama_response(prompt):
    response = client.prompt(message=prompt)
    # print(response)
    return response


if __name__ == "__main__":
    print(get_llama_response)
