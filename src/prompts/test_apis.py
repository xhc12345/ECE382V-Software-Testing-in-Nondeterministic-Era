from LLMs.gemini import get_gemini_response
from LLMs.gpt import get_chatgpt_response
from LLMs.llama import get_llama_response
from data_io import write_to_output
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from prompts.read_prompt import get_prompt

TARGET_PROMPT = [
    ("test_fun_fact", "txt"),
    ("test_json_response", "json"),
    ("test_check_previous_conversation", "txt"),
]


def test_api(test_info: tuple[str, str] = TARGET_PROMPT[0], save: bool = True):
    target_name, target_extension = test_info
    prompt = get_prompt(target_name)
    if not prompt:
        return
    print("Prompt:")
    print(prompt)
    print()

    responses = {
        "ChatGPT": lambda: get_chatgpt_response(prompt),
        "Gemini": lambda: get_gemini_response(prompt),
        "Llama": lambda: get_llama_response(prompt),
    }

    results = {}

    with ThreadPoolExecutor() as executor:
        # Submit tasks with start times
        future_to_name = {}
        start_times = {}

        for name, func in responses.items():
            start_times[name] = time.time()
            future = executor.submit(func)
            future_to_name[future] = name

        # Process completed tasks
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            end_time = time.time()
            time_taken = end_time - start_times[name]

            try:
                response = future.result()
                results[name] = response
                print(f"Time taken for {name}: {time_taken:.3f} seconds")
            except Exception as e:
                results[name] = f"Exception: {e}"
                print(f"{name} generated an exception: {e}")

    # Print all responses together after all functions have completed
    for name, response in results.items():
        print(f"{name}:")
        print(response)
        if save:
            write_to_output(f"{name.lower()}_output.{target_extension}", response)
        print()


if __name__ == "__main__":
    test_api(save=False)
