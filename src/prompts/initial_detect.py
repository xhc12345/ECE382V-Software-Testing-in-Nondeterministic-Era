from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
from data_io import write_to_output
from LLMs.gemini import get_gemini_response
from LLMs.gpt import get_chatgpt_response
from LLMs.llama import get_llama_response
from prompts.read_prompt import get_prompt


def flaky_detect_1(file_path: str, file_content: str):
    base_prompt = get_prompt("flaky_detect_1")
    if not base_prompt:
        return

    filename = os.path.basename(file_path)

    middle_prompt = f"Here is the content of `{filename}` that contains the test(s):\n"

    prompt = base_prompt + "\n" + middle_prompt + "```" + file_content + "```"
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
        write_to_output(f"{name.lower()}_output.txt", response)
        print()
