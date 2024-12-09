import os
import csv


BASE_FOLDER = "data"
PY_DATA = "accepted-py-data.csv"
PR_DATA = "accepted-pr-data.csv"
GR_DATA = "accepted-gr-data.csv"

PY_DATA = os.path.join(BASE_FOLDER, "collection", PY_DATA)
if not os.path.exists(PY_DATA):
    print(f"Cannot find source: {PY_DATA}")
    exit(1)

PR_DATA = os.path.join(BASE_FOLDER, "collection", PR_DATA)
if not os.path.exists(PR_DATA):
    print(f"Cannot find source: {PR_DATA}")
    exit(1)

GR_DATA = os.path.join(BASE_FOLDER, "collection", GR_DATA)
if not os.path.exists(GR_DATA):
    print(f"Cannot find source: {GR_DATA}")
    exit(1)


DESTINATION_FILE = os.path.join(BASE_FOLDER, "collection", "accepted-flakies.csv")
print("Destination file:", DESTINATION_FILE)


# Helper functions
def extract_project_name(url):
    """Extract project name from the project URL."""
    return url.rstrip("/").split("/")[-1]


def parse_pytest_name(pytest_name):
    """Parse Pytest Test Name."""
    parts = pytest_name.split("::")
    if len(parts) == 3:
        suite_name = parts[0].split("/")[-1]
        method_name = parts[2]
    elif len(parts) == 2:
        suite_name = parts[0].split("/")[-1]
        method_name = parts[1]
    else:
        suite_name = parts[0].split("/")[-1]
        method_name = None
    suite_name = suite_name.replace(".py", "")
    # print(suite_name)
    return suite_name, method_name


def parse_fully_qualified_name(fqtn):
    """Parse Fully-Qualified Test Name."""
    parts = fqtn.split(".")
    if len(parts) >= 2:
        suite_name = parts[-2]
        method_name = parts[-1]
    else:
        suite_name, method_name = None, None
    return suite_name, method_name


def determine_file_extension(category):
    """Determine the file extension based on the category."""
    if category == "Python":
        return "py"
    elif category == "Groovy":
        return "groovy"
    elif category == "Java":
        return "java"
    return ""


# Read and process data
collected_flakies = []

# Process Python data
with open(PY_DATA, "r") as py_file:
    reader = csv.DictReader(py_file)
    for row in reader:
        project_name = extract_project_name(row["Project URL"])
        suite_name, method_name = parse_pytest_name(
            row[
                "Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod)"
            ]
        )
        category = row["Category"]
        file_extension = determine_file_extension("Python")
        collected_flakies.append(
            [project_name, suite_name, method_name, category, file_extension]
        )

# Process Groovy data
with open(GR_DATA, "r") as gr_file:
    reader = csv.DictReader(gr_file)
    for row in reader:
        project_name = extract_project_name(row["Project URL"])
        suite_name, method_name = parse_fully_qualified_name(
            row["Fully-Qualified Test Name (packageName.ClassName.methodName)"]
        )
        category = row["Category"]
        file_extension = determine_file_extension("Groovy")
        collected_flakies.append(
            [project_name, suite_name, method_name, category, file_extension]
        )

# Process Java data
with open(PR_DATA, "r") as pr_file:
    reader = csv.DictReader(pr_file)
    for row in reader:
        project_name = extract_project_name(row["Project URL"])
        suite_name, method_name = parse_fully_qualified_name(
            row["Fully-Qualified Test Name (packageName.ClassName.methodName)"]
        )
        category = row["Category"]
        file_extension = determine_file_extension("Java")
        collected_flakies.append(
            [project_name, suite_name, method_name, category, file_extension]
        )

# Write to the output file
with open(DESTINATION_FILE, "w", newline="") as output_csv:
    writer = csv.writer(output_csv)
    # Write the header
    writer.writerow(
        [
            "Project Name",
            "Test Suite Name",
            "Test Method Name",
            "Category",
            "File Extension",
        ]
    )
    # Write the collected data
    writer.writerows(collected_flakies)

print(f"Data collected and saved to {DESTINATION_FILE}")
