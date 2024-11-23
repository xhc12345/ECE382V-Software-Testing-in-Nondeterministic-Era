import os

DATA_PATH = os.getenv("DATA_PATH", "./data")
OUTPUT_DIR = f"{DATA_PATH}/output"


def write_to_output(filename: str, content: str):
    # Create the directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/{filename}", "w") as file:
        file.write(content)


def read_all_from_output() -> tuple[str, str, str]:
    # List all files in the folder
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json")]

    # Initialize a list to store JSON file contents
    json_contents = []

    for file in files:
        file_path = os.path.join(OUTPUT_DIR, file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()  # Read the file as a string
            json_contents.append(content)

    # Return all JSON file contents as a tuple of strings
    return tuple(json_contents)
