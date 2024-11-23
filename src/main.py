import os
from prompts.initial_detect import flaky_detect_1
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

    # flaky_detect_1(test_path, test_code)

    test_api()
    test_api(("test_check_previous_conversation", "txt"))


if __name__ == "__main__":
    main()
