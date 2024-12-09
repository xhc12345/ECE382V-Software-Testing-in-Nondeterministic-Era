import os
import yaml

DATA_PATH = os.getenv("DATA_PATH", "./data")
PROMPTS_FILE = f"{DATA_PATH}/input/prompts.yaml"
BLACKLIST = f"{DATA_PATH}/input/blacklist.yaml"


def test_read_yaml():
    # Read from the YAML file
    with open(PROMPTS_FILE, "r") as file:
        data = yaml.safe_load(file)

    # Safely access the 'prompts' key, defaulting to an empty dictionary if it doesn't exist
    prompts = data.get("prompts", {})

    # Safely fetch each prompt, with a default empty string if it doesn't exist
    prompt1 = prompts.get("prompt1", "")
    prompt2 = prompts.get("prompt2", "")
    prompt3 = prompts.get("prompt3", "")

    # Print each prompt to verify
    print("Prompt 1:", prompt1)
    print("Prompt 2:", prompt2)
    print("Prompt 3:", prompt3)


def get_prompt(prompt_name: str) -> str | None:
    # Read from the YAML file
    with open(PROMPTS_FILE, "r") as file:
        data = yaml.safe_load(file)

    # Safely access the 'prompts' key, defaulting to an empty dictionary if it doesn't exist
    prompts = data.get("prompts", {})

    # Safely fetch each prompt, with a default empty string if it doesn't exist
    prompt = prompts.get(prompt_name, None)
    if not prompt:
        print(f"ERR: PROMPT FOR `{prompt_name}` WAS NOT FOUND IN {PROMPTS_FILE}!")

    return prompt


def get_blacklisted_projects() -> list[str]:
    with open(BLACKLIST, "r") as file:
        data = yaml.safe_load(file)

    projects = data["projects"]

    # Extract the list of project names
    project_names = [project["name"] for project in projects]

    print(f"Skipped projects: {project_names}")

    return project_names


if __name__ == "__main__":
    test_read_yaml()
    # get_blacklisted_projects()
