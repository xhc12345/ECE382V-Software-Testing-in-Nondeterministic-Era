import os
from data_io import read_all_from_output
from db.database_operations import db_init_table, db_tests_get_all, db_tests_insert
from prompts.initial_detect import flaky_detect_1
from prompts.second_detect import flaky_detect_2
from prompts.test_apis import test_api
import sqlite3

DATA_PATH = os.getenv("DATA_PATH", "./data")
DB_PATH = os.path.join(DATA_PATH, "database.db")
EXAMPLE_1 = f"{DATA_PATH}/test-suites/example/FlakyTestSuite.java"
EXAMPLE_2 = f"{DATA_PATH}/test-suites/example/FlakyTestSuiteObfuscated.java"


def process_test(test_path):
    # Load your Java file content
    with open(test_path, "r") as file:
        test_code = file.read()

    flaky_detect_1(test_path, test_code)
    res_gpt, res_gemini, res_llama = read_all_from_output()

    flaky_detect_2(result_gpt=res_gpt, result_gemini=res_gemini, result_llama=res_llama)
    res_gpt, res_gemini, res_llama = read_all_from_output()


def test_example():
    process_test(EXAMPLE_1)


def main():
    db = sqlite3.connect(DB_PATH)
    db_init_table(db)

    all_tests = db_tests_get_all(db)
    print("currently all tests:", all_tests)

    test = ("test1", "testFile.py", "testOrg/testRepo")
    print("inserting:", test)
    db_tests_insert(db, *test)

    all_tests = db_tests_get_all(db)
    print("currently all tests:", all_tests)

    db.close()


if __name__ == "__main__":
    main()
