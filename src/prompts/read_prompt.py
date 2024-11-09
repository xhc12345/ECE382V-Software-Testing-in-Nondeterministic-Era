import yaml

prompts_file = "/data/input/prompts.yaml"


def test_read_yaml():
    # Read from the YAML file
    with open(prompts_file, "r") as file:
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


def get_prompt(prompt_name) -> str | None:
    # Read from the YAML file
    with open(prompts_file, "r") as file:
        data = yaml.safe_load(file)

    # Safely access the 'prompts' key, defaulting to an empty dictionary if it doesn't exist
    prompts = data.get("prompts", {})

    # Safely fetch each prompt, with a default empty string if it doesn't exist
    prompt = prompts.get(prompt_name, None)
    if not prompt:
        print(f"ERR: PROMPT FOR `{prompt_name}` WAS NOT FOUND IN {prompts_file}!")

    return prompt


if __name__ == "__main__":
    test_read_yaml()
