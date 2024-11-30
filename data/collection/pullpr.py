from github import Github

# GitHub Personal Access Token
GITHUB_TOKEN = "your_personal_access_token"  # Replace with your token
REPO_NAME = "owner/repo"  # Replace with "owner/repo" format, e.g., "octocat/Hello-World"
PR_NUMBER = 1  # Replace with the pull request number

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)

def fetch_files_before_pr(repo_name, pr_number):
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
        file_path = file.filename
        print(f"Fetching content for: {file_path}")
        
        try:
            # Fetch the file content at the base commit
            file_content = repo.get_contents(file_path, ref=base_sha)
            print(f"Content for {file_path} (base commit):\n{file_content.decoded_content.decode('utf-8')}\n")
        except Exception as e:
            print(f"Failed to fetch content for {file_path}: {e}")

if __name__ == "__main__":
    fetch_files_before_pr(REPO_NAME, PR_NUMBER)
