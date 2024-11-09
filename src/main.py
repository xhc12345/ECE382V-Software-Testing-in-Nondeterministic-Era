from prompts.initial_detect import flaky_detect_1
from prompts.test_apis import test_api

TEST1 = "/data/test-suites/example/FlakyTestSuite.java"
TEST2 = "/data/test-suites/example/FlakyTestSuiteObfuscated.java"


def main():
    # test_api()

    test_path = TEST1
    # Load your Java file content
    with open(test_path, "r") as file:
        test_code = file.read()

    flaky_detect_1(test_path, test_code)


if __name__ == "__main__":
    main()
