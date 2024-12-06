import os
from dotenv import load_dotenv
from github import Github
import csv
import re

# GitHub Personal Access Token
load_dotenv(dotenv_path=".env")
GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)

CSV_NAME = "accepted-py-data.csv"
BASE_FOLDER = "data"

SOURCE_FILE = os.path.join(BASE_FOLDER, "collection", CSV_NAME)
if not os.path.exists(SOURCE_FILE):
    print(f"Cannot find source: {SOURCE_FILE}")
    exit(1)

DESTINATION_FOLDER = os.path.join(BASE_FOLDER, "test-suites")
if not os.path.exists(DESTINATION_FOLDER):
    print(f"Cannot find output: {DESTINATION_FOLDER}")
    exit(1)


def fetch_files_before_pr(repo_name: str, pr_number: int):
    # Get the repository
    repo = g.get_repo(repo_name)

    # Get the pull request
    pr = repo.get_pull(pr_number)

    # Get the base commit (state before PR changes)
    base_sha = pr.base.sha
    print(f"Base SHA: {base_sha}")

    # List files changed in the PR
    changed_files = pr.get_files()
    for file in changed_files:
        project_and_file_name = file.filename
        print(f"Fetching content for: {project_and_file_name}")

        try:
            # Fetch the file content at the base commit
            file_content_raw = repo.get_contents(project_and_file_name, ref=base_sha)
            file_content = file_content_raw.decoded_content.decode("utf-8")
            file_name = repo_name.split("/")[-1] + project_and_file_name.split("/")[-1]
            return (file_name, file_content)
        except Exception as e:
            print(f"Failed to fetch content for {project_and_file_name}: {e}")
            return (None, None)


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
    print(f"Creating file at: {file_path}")

    # Write the content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(fContent)

    print(f"File saved at: {file_path}")


# Function to extract repository name and PR number
def extract_repo_and_pr(link):
    # Use a regex to extract the repo and PR number
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)", link)
    if match:
        repo_name = str(match.group(1))  # e.g., 'airbrake/pybrake'
        pr_number = int(match.group(2))  # e.g., '163'
        return repo_name, pr_number
    else:
        return None, None  # If the URL doesn't match the expected format


def get_file_from_pr_link(pr_link: str):
    repo_name, pr_number = extract_repo_and_pr(pr_link)
    if repo_name and pr_number:
        print(f"Grabbing {repo_name} PR #{pr_number}")
        fName, fContent = fetch_files_before_pr(repo_name, pr_number)
        if fName and fContent:
            store_file(fName, fContent)
        else:
            print("NO FILE FOUND FOR:", pr_link)
    else:
        print(f"Invalid PR Link format: {pr_link}")


if __name__ == "__main__":
    # Open the CSV file
    with open(SOURCE_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        i = 0
        for row in reader:
            link = row["PR Link"]
            print(f"{i} - READING: {link}")
            get_file_from_pr_link(link)
            print()
            i += 1
