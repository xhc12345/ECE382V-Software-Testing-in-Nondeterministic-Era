import time
from meta_ai_api import MetaAI

client = MetaAI()


def get_llama_response(prompt):
    start_time = time.time()

    response = client.prompt(message=prompt)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Llama Reponse Time: {time_taken:.3f}s")
    # print(response)
    return response["message"]


if __name__ == "__main__":
    prompt = "Tell me a short fun fact about space."
    response = get_llama_response(prompt)
    print(response)
