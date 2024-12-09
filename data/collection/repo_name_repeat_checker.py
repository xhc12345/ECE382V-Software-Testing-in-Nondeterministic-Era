import csv
from collections import defaultdict

# Define the input CSV file
input_csv_files = [
    "accepted-gr-data.csv",
    "accepted-pr-data.csv",
    "accepted-py-data.csv",
]

input_csv_files = ["data/collection/" + item for item in input_csv_files]


# Dictionary to store project names and their associated owners
projects = defaultdict(set)

for input_csv_file in input_csv_files:
    # Read the CSV file and collect project URLs
    with open(input_csv_file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            project_url = row["Project URL"]  # Adjust the column name if necessary

            # Extract owner and project name from the URL
            if project_url.startswith("https://github.com/"):
                _, owner, project_name = project_url.rsplit("/", maxsplit=2)
                projects[project_name].add(owner)

# Identify projects with the same name but different owners
duplicates = {
    project: owners for project, owners in projects.items() if len(owners) > 1
}

# Output the results
if duplicates:
    print("Projects with the same name but different owners:")
    for project, owners in duplicates.items():
        print(f"Project Name: {project}, Owners: {', '.join(owners)}")
else:
    print("No projects found with the same name but different owners.")
