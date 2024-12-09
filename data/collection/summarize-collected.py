# Paths to the input and output files
import csv
import os
import sys

BASE_FOLDER = "data"
TEST_SUITES = os.path.join(BASE_FOLDER, "test-suites")
ACCEPTED_FLAKIES = os.path.join(BASE_FOLDER, "collection", "accepted-flakies.csv")
COLLECTED_CSV = os.path.join(BASE_FOLDER, "collection", "collected-flakies.csv")
MISSING_CSV = os.path.join(BASE_FOLDER, "collection", "missing-flakies.csv")
if not os.path.exists(ACCEPTED_FLAKIES):
    print(f"Cannot find source: {ACCEPTED_FLAKIES}")
    exit(1)


# Function to build a set of existing project-test pairs from the test-suites directory
def collect_existing_tests(test_suites_dir):
    existing_tests = set()
    for ext_folder in os.listdir(test_suites_dir):
        ext_path = os.path.join(test_suites_dir, ext_folder)
        if not os.path.isdir(ext_path):
            continue
        for project in os.listdir(ext_path):
            project_path = os.path.join(ext_path, project)
            if not os.path.isdir(project_path):
                continue
            for test_file in os.listdir(project_path):
                file_name = test_file.split(".")[0]
                existing_tests.add((project, file_name))
    return existing_tests


# Collect existing project-test pairs
existing_tests = collect_existing_tests(TEST_SUITES)
# print(existing_tests)

print(f"Number of test files collected: {len(existing_tests)}")

# Read the collected flakies and filter for actually collected flakies
with open(ACCEPTED_FLAKIES, "r") as input_csv, open(
    COLLECTED_CSV, "w", newline=""
) as collected_csv_file, open(MISSING_CSV, "w", newline="") as missing_csv_file:
    reader = csv.DictReader(input_csv)
    fieldnames = reader.fieldnames

    collected_writer = csv.DictWriter(collected_csv_file, fieldnames=fieldnames)
    collected_writer.writeheader()

    missing_writer = csv.DictWriter(missing_csv_file, fieldnames=fieldnames)
    missing_writer.writeheader()

    for row in reader:
        project = row["Project Name"]
        suite_name = row["Test Suite Name"]
        # Check if the project-test pair exists in the test-suites directory
        if (project, suite_name) in existing_tests:
            collected_writer.writerow(row)
        else:
            # print(
            #     f"{project}/{suite_name} is not present in the collected-flakies.csv",
            #     file=sys.stderr,
            # )
            missing_writer.writerow(row)

print(f"Filtered flakies written to: {COLLECTED_CSV}")
