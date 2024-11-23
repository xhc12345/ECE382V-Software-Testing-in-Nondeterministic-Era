import os

DATA_PATH = os.getenv("DATA_PATH", "./data")
OUTPUT_DIR = f"{DATA_PATH}/output"


def write_to_output(filename: str, content: str):
    # Create the directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/{filename}", "w") as file:
        file.write(content)
