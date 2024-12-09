from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys
import time
from typing import Literal
from data_io import write_to_output
from LLMs.gemini import get_gemini_response
from LLMs.gpt import get_chatgpt_response, single_get_chatgpt_response
from LLMs.llama import get_llama_response
from prompts.read_prompt import get_prompt

JSONIFY_1 = "jsonify_detect_1"
JSONIFY_2 = "jsonify_detect_2"
OUTPUT_EXTENSION = "json"

DEBUG = False


def jsonify_detect(
    prompt_tag: Literal["jsonify_detect_1", "jsonify_detect_2"],
    gpt_response: str,
    gemini_response: str,
    llama_response: str,
):
    base_prompt = get_prompt(prompt_tag)
    if not base_prompt:
        return
    prompt = (
        base_prompt
        + "\nChatGPT:\n"
        + "```\n"
        + gpt_response
        + "```\n\n"
        + "\nGemini:\n"
        + "```\n"
        + gemini_response
        + "```\n\n"
        + "\nLlama:\n"
        + "```\n"
        + llama_response
        + "```"
    )
    if DEBUG:
        print("Prompt:")
        print(prompt)
        print()

    responses = {
        "ChatGPT": lambda: single_get_chatgpt_response(prompt),
        # "Gemini": lambda: get_gemini_response(prompt),
        # "Llama": lambda: get_llama_response(prompt),
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
                print(f"{name} generated an exception: {e}", file=sys.stderr)

    # Print all responses together after all functions have completed
    for name, response in results.items():
        if DEBUG:
            print(f"{name}:")
            print(response)
            write_to_output(f"{name.lower()}_output.{OUTPUT_EXTENSION}", response)
            print()
        return name, response


def jsonify_detect_1(gpt_response: str, gemini_response: str, llama_response: str):
    return jsonify_detect(JSONIFY_1, gpt_response, gemini_response, llama_response)


def jsonify_detect_2(gpt_response: str, gemini_response: str, llama_response: str):
    return jsonify_detect(JSONIFY_2, gpt_response, gemini_response, llama_response)
