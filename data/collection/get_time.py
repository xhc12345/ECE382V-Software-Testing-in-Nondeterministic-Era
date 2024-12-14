import os
import sqlite3
import sys

from matplotlib import pyplot as plt

DB_NAME = "database.db"
SVG1_NAME = "time-plot-1.svg"
SVG2_NAME = "time-plot-2.svg"
BASE_FOLDER = "data"


SOURCE_FILE = os.path.join(BASE_FOLDER, DB_NAME)
if not os.path.exists(SOURCE_FILE):
    print(f"Cannot find source: {SOURCE_FILE}", file=sys.stderr)
    exit(1)

DESTINATION_FILE_1 = os.path.join(BASE_FOLDER, "collection", SVG1_NAME)
DESTINATION_FILE_2 = os.path.join(BASE_FOLDER, "collection", SVG2_NAME)

GPT_RESULT_TABLE_1 = "GPT_result_1"
GPT_RESULT_TABLE_2 = "GPT_result_2"

GEMINI_RESULT_TABLE_1 = "Gemini_result_1"
GEMINI_RESULT_TABLE_2 = "Gemini_result_2"

LLAMA_RESULT_TABLE_1 = "Llama_result_1"
LLAMA_RESULT_TABLE_2 = "Llama_result_2"

LLM_TABLES_1 = [
    GPT_RESULT_TABLE_1,
    GEMINI_RESULT_TABLE_1,
    LLAMA_RESULT_TABLE_1,
]

LLM_TABLES_2 = [
    GPT_RESULT_TABLE_2,
    GEMINI_RESULT_TABLE_2,
    LLAMA_RESULT_TABLE_2,
]


def get_execution_times(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    tables = LLM_TABLES_1 + LLM_TABLES_2

    execution_times = {}

    for table in tables:
        print("grabbing", table, "data")
        # Verify the table has the required structure
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]

        required_columns = {
            "Project_Name",
            "Test_Suite_Name",
            "Response",
            "File_Extension",
            "Execution_Time",
        }
        # print("found columns:", columns)
        if set(required_columns).issubset(columns):
            # If the table has the required structure, fetch Execution_Time
            cursor.execute(f"SELECT Execution_Time FROM {table}")
            execution_times[table] = [row[0] for row in cursor.fetchall()]
        else:
            print("Bad table format!", file=sys.stderr)

    conn.close()
    return execution_times


# Example usage
execution_times = get_execution_times(SOURCE_FILE)


def two_by_three_charts():
    # Create a figure with 2x3 subplots
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    axes = axes.T.flatten()  # Transpose to fill columns first
    for i, (table, times_og) in enumerate(execution_times.items()):
        times = []
        for j in range(len(times_og)):
            if isinstance(times_og[j], float):
                times.append(times_og[j])
        print(f"Execution times from table '{table}': {len(times)}/{len(times_og)}")
        print("Is all float?", all(isinstance(item, float) for item in times))
        ax = axes[i]
        ax.boxplot(times, patch_artist=True, vert=True)
        ax.set_title(f"Table: {table}")
        ax.set_ylabel("Execution Time")
        ax.grid(True)
        ax.set_ylim(bottom=0)  # Set x-axis limit to start at 0
    # Hide any unused subplots
    for j in range(len(execution_times), len(axes)):
        axes[j].axis("off")

    plt.tight_layout()

    # Save the plot as an SVG file
    plt.savefig(DESTINATION_FILE_1, format="svg")
    # plt.savefig("data/collection/time.png", format="png")


def combine_chart():
    custom_order = [
        GPT_RESULT_TABLE_1,
        GPT_RESULT_TABLE_2,
        GEMINI_RESULT_TABLE_1,
        GEMINI_RESULT_TABLE_2,
        LLAMA_RESULT_TABLE_1,
        LLAMA_RESULT_TABLE_2,
    ]
    # Prepare data for the plot based on the specified order
    all_times = []
    table_names = []
    for table in custom_order:
        if table in execution_times:
            times = []
            times_og = execution_times[table]
            for j in range(len(times_og)):
                if isinstance(times_og[j], float):
                    times.append(times_og[j])
            print(f"Execution times from table '{table}': {len(times)}/{len(times_og)}")
            print("Is all float?", all(isinstance(item, float) for item in times))
            all_times.append(times)
            table_names.append(table)

    # Create a single plot with all box plots in the specified order
    plt.figure(figsize=(12, 8))
    plt.boxplot(all_times, patch_artist=True, vert=True, labels=table_names)
    plt.title("Execution Time Box Plot of Different LLMs")
    plt.ylabel("Execution Time (s)")
    plt.xlabel("Model Name and Conversation Depth")
    plt.grid(True, axis="y")
    plt.ylim(bottom=0, top=60)  # Set y-axis limit to start at 0

    plt.tight_layout()
    # Save the plot as an SVG file
    plt.savefig(DESTINATION_FILE_2, format="svg")


# two_by_three_charts()
combine_chart()
