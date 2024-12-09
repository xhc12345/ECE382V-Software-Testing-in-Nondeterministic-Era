import csv
import os
import sqlite3
from typing import Literal

FLAKY_TEST_TABLE = "flaky_tests"
FAILED_TEST_TABLE = "failed_tests"

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


def db_init_tables(db: sqlite3.Connection):
    cursor = db.cursor()

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {FLAKY_TEST_TABLE} (
            Project_Name TEXT NOT NULL,
            Test_Suite_Name TEXT NOT NULL,
            Test_Method_Name TEXT,
            Category TEXT NOT NULL,
            File_Extension TEXT NOT NULL
        )
        """
    )
    db.commit()

    for table in LLM_TABLES_1:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                Project_Name TEXT NOT NULL,
                Test_Suite_Name TEXT NOT NULL,
                Response TEXT NOT NULL,
                File_Extension TEXT NOT NULL,
                Execution_Time REAL
            )
            """
        )
        db.commit()

    for table in LLM_TABLES_2:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                Project_Name TEXT NOT NULL,
                Test_Suite_Name TEXT NOT NULL,
                Response TEXT NOT NULL,
                File_Extension TEXT NOT NULL,
                Execution_Time REAL
            )
            """
        )
        db.commit()


def db_nuke(db: sqlite3.Connection):
    cursor = db.cursor()

    # Disable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = OFF;")

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]};")

    # Commit changes
    db.commit()
    print("Deleted all tables")


def db_tests_populate_data(db: sqlite3.Connection, csv_path: str):
    cursor = db.cursor()

    with open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            cursor.execute(
                f"""
                    INSERT INTO {FLAKY_TEST_TABLE} (Project_Name, Test_Suite_Name, Test_Method_Name, Category, File_Extension)
                    VALUES (?, ?, ?, ?, ?);
                """,
                row,
            )

    db.commit()


def db_results_insert(
    db: sqlite3.Connection,
    table: Literal[
        "GPT_result_1",
        "GPT_result_2",
        "Gemini_result_1",
        "Gemini_result_2",
        "Llama_result_1",
        "Llama_result_2",
    ],
    project_name: str,
    test_suite_name: str,
    response: str,
    file_extension: str,
    execution_time: float,
):
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO {table} (Project_Name, Test_Suite_Name, Response, File_Extension, Execution_Time) VALUES (?, ?, ?, ?, ?)",
        (project_name, test_suite_name, response, file_extension, execution_time),
    )
    db.commit()


def db_results_fetch_one(
    db: sqlite3.Connection,
    table: Literal[
        "GPT_result_1",
        "GPT_result_2",
        "Gemini_result_1",
        "Gemini_result_2",
        "Llama_result_1",
        "Llama_result_2",
    ],
    project_name: str,
    test_suite_name: str,
) -> tuple[str, float]:
    cursor = db.cursor()
    cursor.execute(
        f"SELECT * FROM {table} WHERE Project_Name = ? AND Test_Suite_Name = ? LIMIT 1",
        (project_name, test_suite_name),
    )
    row = cursor.fetchone()
    _, _, Response, _, Execution_Time = row
    return Response, Execution_Time


def db_tests_get_all(
    db: sqlite3.Connection,
    table: Literal[
        "flaky_tests",
        "failed_tests",
        "GPT_result_1",
        "GPT_result_2",
        "Gemini_result_1",
        "Gemini_result_2",
        "Llama_result_1",
        "Llama_result_2",
    ],
):
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    all_tests = cursor.fetchall()

    return all_tests
