from gemini import get_gemini_response
from gpt import get_chatgpt_response
from llama import get_llama_response
from data_io import write_to_output
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def test_api():
    print("Prompt")
    prompt = "Tell me a short fun fact about space."
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
