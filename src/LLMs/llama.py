import time
from meta_ai_api import MetaAI

client = MetaAI()


def get_llama_response(prompt: str, new_conversation: bool = False) -> str:
    global client
    start_time = time.time()

    response = client.prompt(message=prompt, new_conversation=new_conversation)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Llama Reponse Time: {time_taken:.3f}s")
    # print(response)
    return response["message"]


def reset_llama_conversation():
    global client
    client = MetaAI()
    print("Cleared Llama conversation.")


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    print("Prompt:", prompt)
    response = get_llama_response(prompt)
    print(response)
    print()

    prompt = "What was my previous question?"
    print("Prompt:", prompt)
    response = get_llama_response(prompt)
    print(response)
    print()

    reset_llama_conversation()
    prompt = "What was my previous question?"
    response = get_llama_response(prompt)
    print(response)
    print()
