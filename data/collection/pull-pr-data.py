import os
import sys
from dotenv import load_dotenv
from github import Github
import csv
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Standard Colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
INFO = f"[{BLUE} INFO {RESET}]"
ERROR = f"[{RED} ERROR {RESET}]"

DEBUG: bool = True

# GitHub Personal Access Token
load_dotenv(dotenv_path=".env")
GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)

# CSV_NAME = "accepted-pr-data.csv"
CSV_NAME = "accepted-gr-data.csv"
# CSV_NAME = "sample.csv"
BASE_FOLDER = "data"


def print_colored(text: str, color: str):
    print(f"{color}{text}{RESET}")


def print_info(text: str):
    if DEBUG:
        print(f"{INFO}:\t{text}")


def print_err(text: str):
    print(f"{ERROR}:\t{text}", file=sys.stderr)


SOURCE_FILE = os.path.join(BASE_FOLDER, "collection", CSV_NAME)
if not os.path.exists(SOURCE_FILE):
    print_err(f"Cannot find source: {SOURCE_FILE}")
    exit(1)

DESTINATION_FOLDER = os.path.join(BASE_FOLDER, "test-suites")
if not os.path.exists(DESTINATION_FOLDER):
    print_err(f"Cannot find output: {DESTINATION_FOLDER}")
    exit(1)


def fetch_specific_file(repo_name: str, pr_number: int, file_path: str):
    # Get the repository
    repo = g.get_repo(repo_name)

    # Get the pull request
    pr = repo.get_pull(pr_number)

    # Get the base commit (state before PR changes)
    base_sha = pr.base.sha
    print_info(f"Base SHA: {base_sha}")

    print_info(f"Fetching content for: {file_path}")
    try:
        # Fetch the file content at the base commit
        file_content_raw = repo.get_contents(file_path, ref=base_sha)
        file_content = file_content_raw.decoded_content.decode("utf-8")
        file_name = repo_name.split("/")[-1] + "/" + file_path.split("/")[-1]
        return file_name, file_content
    except Exception as e:
        print_err(f"Failed to fetch content for {file_path}: {e}")
        return None, None


def store_file(fName: str, fContent: str):
    # Extract the project name and file name
    parts = fName.split("/")
    project_name = parts[0]
    file_name = parts[-1]
    file_extension = file_name.split(".")[-1]  # Get the file extension

    # Create the folder for the file extension
    extension_folder = os.path.join(DESTINATION_FOLDER, file_extension)
    os.makedirs(extension_folder, exist_ok=True)

    # Create the project subdirectory inside 'test-suites'
    project_path = os.path.join(extension_folder, project_name)
    os.makedirs(project_path, exist_ok=True)

    # Create the full path to the file directly under the project folder
    file_path = os.path.join(project_path, file_name)
    print_info(f"Creating file at: {file_path}")

    # Write the content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(fContent)

    print_colored(f"File saved at: {file_path}", GREEN)


# Function to extract repository name, PR number, and file path
def extract_repo_pr_and_file(link: str, fully_qualified_name: str):
    # Extract the repository name and PR number
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)", link)
    if match:
        repo_name = str(match.group(1))  # e.g., 'airbrake/pybrake'
        pr_number = int(match.group(2))  # e.g., '163'

    # Extract the changed files in the PR
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    try:
        changed_files = [file.filename for file in pr.get_files()]
        print_info(f"Changed files in PR #{pr_number}: {changed_files}")

        # Convert the fully qualified name to a partial path
        parts = fully_qualified_name.rsplit(
            ".", 2
        )  # Expecting packageName.ClassName.methodName
        if len(parts) >= 2:
            package_path = parts[0].replace(".", "/")  # Convert package name to path
            class_name = parts[1]
            partial_path = f"{package_path}/{class_name}"

            # Attempt to match the partial path to one of the changed files
            for file_path in changed_files:
                if partial_path in file_path:
                    print_info(f"Matched file: {file_path}")
                    return repo_name, pr_number, file_path
            print_err(f"No exact match found for {partial_path} in changed files.")
        else:
            print_err(f"Invalid fully qualified name format: {fully_qualified_name}")
    except Exception as e:
        print_err(f"Error fetching changed files for PR #{pr_number}: {e}")

    return None, None, None


def get_file_from_pr_link(pr_link: str, fully_qualified_name: str) -> bool:
    repo_name, pr_number, file_path = extract_repo_pr_and_file(
        pr_link, fully_qualified_name
    )
    if repo_name and pr_number and file_path:
        print_info(f"Grabbing {repo_name} PR #{pr_number} File: {file_path}")
        fName, fContent = fetch_specific_file(repo_name, pr_number, file_path)
        if fName and fContent:
            print_info(f"Fetched {fName}")
            store_file(fName, fContent)
            return True
        else:
            print_err(f"NO FILE FOUND FOR: {pr_link}")
    else:
        print_err(
            f"Invalid PR Link or Fully Qualified Name format: {pr_link}, {fully_qualified_name}"
        )
    return False


def init_pr_fetch_failed_file():
    """
    Initializes the pr-fetch-failed.csv file in the {BASE_FOLDER}/collection directory.
    If the file already exists, it resets it by creating a new empty file with the specified columns.
    """
    # Define the file path
    file_path = os.path.join(BASE_FOLDER, "collection", "pr-fetch-failed.csv")

    # Reset the file with headers
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["test_name", "pr_link"])


def pr_fetch_failed(test_name, pr_link):
    """
    Appends a new entry with the given test_name and pr_link to the pr-fetch-failed.csv file.
    Assumes that init_pr_fetch_failed_file has already been called.

    Parameters:
        test_name (str): The name of the test.
        pr_link (str): The pull request link.
    """
    # Define the file path
    file_path = os.path.join(BASE_FOLDER, "collection", "pr-fetch-failed.csv")

    # Append the new row to the file
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([test_name, pr_link])


# Function to process a single row
def process_row(row, index):
    pr_link = row["PR Link"]
    fully_qualified_name = row[
        "Fully-Qualified Test Name (packageName.ClassName.methodName)"
    ]
    print_colored(f"{index} - READING: {pr_link}", YELLOW)

    try:
        saved = get_file_from_pr_link(pr_link, fully_qualified_name)
    except Exception as e:
        print_err(f"Error processing row {index}: {e}")
        saved = False

    if not saved:
        pr_fetch_failed(fully_qualified_name, pr_link)

    print()
    return index


if __name__ == "__main__":
    WORKER_COUNT = 2  # Fixed number of workers
    DEBUG = False
    START_ROW = 0  # resume from this row

    # Open the CSV file
    with open(SOURCE_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Filter rows to start from the specified row
    rows_to_process = rows[START_ROW:]
    total_rows = len(rows_to_process)

    print_colored(f"Total rows to process: {total_rows}", MAGENTA)
    print()

    init_pr_fetch_failed_file()  # Initialize the failure file

    # Using ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=WORKER_COUNT) as executor:
        # Submit tasks to the executor
        future_to_index = {
            executor.submit(process_row, row, index): index
            for index, row in enumerate(rows_to_process)
        }

        # Monitor and handle task completion
        for future in as_completed(future_to_index):
            try:
                future.result()
            except Exception as e:
                print_err(f"Unexpected error in row {future_to_index[future]}: {e}")
