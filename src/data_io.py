import os


output_dir = "/data/output"


def write_to_output(filename, content):
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/{filename}", "w") as file:
        file.write(content)
