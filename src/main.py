import os
import time
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
from prompts.read_prompt import get_blacklisted_projects
from prompts.second_detect import flaky_detect_2
from prompts.test_apis import test_api
import sqlite3

DATA_PATH = os.getenv("DATA_PATH", "./data")
DB_PATH = os.path.join(DATA_PATH, "database.db")

COLLECTED_FLAKIES = os.path.join(DATA_PATH, "collection", "collected-flakies.csv")

EXAMPLE_1 = f"{DATA_PATH}/test-suites/example/FlakyTestSuite.java"
EXAMPLE_2 = f"{DATA_PATH}/test-suites/example/FlakyTestSuiteObfuscated.java"
EXAMPLE_3 = f"{DATA_PATH}/test-suites/example/GiganticTestSuite.java"


DB: sqlite3.Connection = None
BLACK_LIST: list[str] = None


def test_database():
    all_tests = db_tests_get_all(DB, "flaky_tests")
    print("currently all tests:", all_tests)

    db_tests_populate_data(DB, COLLECTED_FLAKIES)

    all_tests = db_tests_get_all(DB, "flaky_tests")
    print("currently all tests:", all_tests)


def process_test(test_path):
    # Load your Java file content
    with open(test_path, "r") as file:
        test_code = file.read()

    first_pass = flaky_detect_1(test_path, test_code)
    gpt_response = first_pass.get("ChatGPT")[0]
    if not gpt_response:
        gpt_response = ""
    gemini_response = first_pass.get("Gemini")[0]
    if not gemini_response:
        gemini_response = ""
    llama_response = first_pass.get("Llama")[0]
    if not llama_response:
        llama_response = ""
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
    if not gpt_response:
        gpt_response = ""
    gemini_response = second_pass.get("Gemini")[0]
    if not gemini_response:
        gemini_response = ""
    llama_response = second_pass.get("Llama")[0]
    if not llama_response:
        llama_response = ""
    _, second_responses = jsonify_detect_2(
        gpt_response, gemini_response, llama_response
    )
    db_store_json_2(DB, test_path, Json=second_responses, time=second_pass)
    write_to_output(f"detect_2_jsonified_output.json", second_responses)

    # db_results = db_get_json_2(DB, test_path)
    # for res, time in db_results:
    #     print(time)
    #     print(res)
    #     print()


def test_example():
    process_test(EXAMPLE_1)


def test_mega():
    process_test(EXAMPLE_3)


def has_file(file_path: str):
    # Placeholder for the function logic
    if not os.path.isfile(file_path):
        return False
    return True


def process_all():
    cursor = DB.cursor()

    cursor.execute(
        "SELECT Project_Name, Test_Suite_Name, File_Extension FROM flaky_tests"
    )

    rows = cursor.fetchall()
    numrows = len(rows)

    checked_files: set[str] = set()

    start_from = 200

    # Start timer
    start_time = time.time()

    # Iterate through the rows and generate file paths
    i = 0
    for row in rows:
        i += 1
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(f"[Test Suite {i}/{numrows}] Elapsed time since start: {formatted_time}")

        project_name, test_suite_name, file_extension = row

        # Skip processing if the project is in the blacklist
        if project_name in BLACK_LIST:
            print(f"\tSkipping blacklisted project: {project_name}")
            continue

        file_path = os.path.join(
            DATA_PATH,
            "test-suites",
            file_extension,
            project_name,
            f"{test_suite_name}.{file_extension}",
        )

        # Call process_test for each file path
        if not has_file(file_path):
            print(f"\tFile not found: {file_path}")
            continue

        if file_path in checked_files:
            print(f"\tAlready checked file")
            continue
        checked_files.add(file_path)

        if i < start_from:
            continue

        process_test(file_path)


def main():
    global DB, BLACK_LIST
    DB = sqlite3.connect(DB_PATH)
    BLACK_LIST = get_blacklisted_projects()

    # db_nuke(DB)

    # add 'collected-flakies.csv' into the 'flaky_tests' table
    # db_tests_populate_data(DB, COLLECTED_FLAKIES)

    db_init_tables(DB)

    process_all()

    DB.close()


if __name__ == "__main__":
    main()
