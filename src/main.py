import os
from data_io import read_all_from_output, write_to_output
from db.database_batch import (
    db_get_json_1,
    db_get_json_2,
    db_store_json_1,
    db_store_json_2,
)
from db.database_operations import (
    db_init_tables,
    db_nuke,
    db_tests_get_all,
    db_tests_populate_data,
)
from prompts.convert_to_json import jsonify_detect_1, jsonify_detect_2
from prompts.initial_detect import flaky_detect_1
from prompts.second_detect import flaky_detect_2
from prompts.test_apis import test_api
import sqlite3

DATA_PATH = os.getenv("DATA_PATH", "./data")
DB_PATH = os.path.join(DATA_PATH, "database.db")

COLLECTED_FLAKIES = os.path.join(DATA_PATH, "collection", "collected-flakies.csv")

EXAMPLE_1 = f"{DATA_PATH}/test-suites/example/FlakyTestSuite.java"
EXAMPLE_2 = f"{DATA_PATH}/test-suites/example/FlakyTestSuiteObfuscated.java"


DB: sqlite3.Connection = None


def test_database():
    all_tests = db_tests_get_all(DB)
    print("currently all tests:", all_tests)

    db_tests_populate_data(DB, COLLECTED_FLAKIES)

    all_tests = db_tests_get_all(DB)
    print("currently all tests:", all_tests)


def process_test(test_path):
    # Load your Java file content
    with open(test_path, "r") as file:
        test_code = file.read()

    first_pass = flaky_detect_1(test_path, test_code)
    gpt_response = first_pass.get("ChatGPT")[0]
    gemini_response = first_pass.get("Gemini")[0]
    llama_response = first_pass.get("Llama")[0]
    _, first_responses = jsonify_detect_1(gpt_response, gemini_response, llama_response)
    db_store_json_1(DB, test_path, Json=first_responses, time=first_pass)
    write_to_output(f"detect_1_jsonified_output.json", first_responses)

    db_results = db_get_json_1(DB, test_path)
    (res_gpt, _), (res_gemini, _), (res_llama, _) = db_results
    # for res, time in db_results:
    #     print(time)
    #     print(res)
    #     print()

    second_pass = flaky_detect_2(
        result_gpt=res_gpt, result_gemini=res_gemini, result_llama=res_llama
    )
    gpt_response = second_pass.get("ChatGPT")[0]
    gemini_response = second_pass.get("Gemini")[0]
    llama_response = second_pass.get("Llama")[0]
    _, second_responses = jsonify_detect_2(
        gpt_response, gemini_response, llama_response
    )
    db_store_json_2(DB, test_path, Json=second_responses, time=second_pass)
    write_to_output(f"detect_2_jsonified_output.json", second_responses)

    db_results = db_get_json_2(DB, test_path)
    for res, time in db_results:
        print(time)
        print(res)
        print()


def test_example():
    process_test(EXAMPLE_1)


def main():
    global DB
    DB = sqlite3.connect(DB_PATH)

    db_nuke(DB)

    db_init_tables(DB)

    test_example()

    DB.close()


if __name__ == "__main__":
    main()
