import os
from data_io import read_all_from_output
from prompts.initial_detect import flaky_detect_1
from prompts.second_detect import flaky_detect_2
from prompts.test_apis import test_api

DATA_PATH = os.getenv("DATA_PATH", "./data")
TEST1 = f"{DATA_PATH}/test-suites/example/FlakyTestSuite.java"
TEST2 = f"{DATA_PATH}/test-suites/example/FlakyTestSuiteObfuscated.java"


def main():
    # test_api()

    test_path = TEST1
    # Load your Java file content
    with open(test_path, "r") as file:
        test_code = file.read()

    flaky_detect_1(test_path, test_code)

    res_gpt, res_gemini, res_llama = read_all_from_output()
    flaky_detect_2(result_gpt=res_gpt, result_gemini=res_gemini, result_llama=res_llama)


if __name__ == "__main__":
    main()
