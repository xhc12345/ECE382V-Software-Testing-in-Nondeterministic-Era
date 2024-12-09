import json
import os
import sqlite3

from db.database_operations import (
    db_results_fetch_one,
    db_results_insert,
    LLM_TABLES_1,
    LLM_TABLES_2,
)

GPT = "ChatGPT"
GEMINI = "Gemini"
LLAMA = "Llama"

DATA_PATH = os.getenv("DATA_PATH", "./data")
TEMP = os.path.join(DATA_PATH, "output", "temp")


def store_temp(proj, file, ext, content):
    path = os.path.join(TEMP, proj)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, f"{file}.{ext}"), "w") as file:
        file.write(content)


def db_store_json_1(
    db: sqlite3.Connection,
    test_path: str,
    Json: str,
    time: dict[str, tuple[str, float]],
):
    responses = json.loads(Json)
    res_gpt = responses.get(GPT, None)
    res_gemini = responses.get(GEMINI, None)
    res_llama = responses.get(LLAMA, None)

    _, proj, file = test_path.rsplit("\\", maxsplit=2)
    file_name, file_extension = file.split(".")

    time_gpt = time.get(GPT, (None, None))[1]
    time_gemini = time.get(GEMINI, (None, None))[1]
    time_llama = time.get(LLAMA, (None, None))[1]

    db_results_insert(
        db,
        LLM_TABLES_1[0],  # gpt table 1
        project_name=proj,
        test_suite_name=file_name,
        response=json.dumps(res_gpt),
        file_extension=file_extension,
        execution_time=time_gpt,
    )

    db_results_insert(
        db,
        LLM_TABLES_1[1],  # gemini table 1
        project_name=proj,
        test_suite_name=file_name,
        response=json.dumps(res_gemini),
        file_extension=file_extension,
        execution_time=time_gemini,
    )

    db_results_insert(
        db,
        LLM_TABLES_1[2],  # llama table 1
        project_name=proj,
        test_suite_name=file_name,
        response=json.dumps(res_llama),
        file_extension=file_extension,
        execution_time=time_llama,
    )


def db_store_json_2(
    db: sqlite3.Connection,
    test_path: str,
    Json: str,
    time: dict[str, tuple[str, float]],
):
    responses = json.loads(Json)
    res_gpt = responses.get(GPT, None)
    res_gemini = responses.get(GEMINI, None)
    res_llama = responses.get(LLAMA, None)

    _, proj, file = test_path.rsplit("\\", maxsplit=2)
    file_name, file_extension = file.split(".")

    time_gpt = time.get(GPT, (None, None))[1]
    time_gemini = time.get(GEMINI, (None, None))[1]
    time_llama = time.get(LLAMA, (None, None))[1]

    db_results_insert(
        db,
        LLM_TABLES_2[0],  # gpt table 2
        project_name=proj,
        test_suite_name=file_name,
        response=json.dumps(res_gpt),
        file_extension=file_extension,
        execution_time=time_gpt,
    )

    db_results_insert(
        db,
        LLM_TABLES_2[1],  # gemini table 2
        project_name=proj,
        test_suite_name=file_name,
        response=json.dumps(res_gemini),
        file_extension=file_extension,
        execution_time=time_gemini,
    )

    db_results_insert(
        db,
        LLM_TABLES_2[2],  # llama table 2
        project_name=proj,
        test_suite_name=file_name,
        response=json.dumps(res_llama),
        file_extension=file_extension,
        execution_time=time_llama,
    )

    store_temp(proj, file_name, file_extension, Json)


def db_get_json_1(
    db: sqlite3.Connection,
    test_path: str,
):
    _, proj, file = test_path.rsplit("\\", maxsplit=2)
    file_name, file_extension = file.split(".")

    gpt_res = db_results_fetch_one(
        db, LLM_TABLES_1[0], project_name=proj, test_suite_name=file_name
    )

    gemini_res = db_results_fetch_one(
        db, LLM_TABLES_1[1], project_name=proj, test_suite_name=file_name
    )

    llama_res = db_results_fetch_one(
        db, LLM_TABLES_1[2], project_name=proj, test_suite_name=file_name
    )

    return gpt_res, gemini_res, llama_res


def db_get_json_2(
    db: sqlite3.Connection,
    test_path: str,
):
    _, proj, file = test_path.rsplit("\\", maxsplit=2)
    file_name, file_extension = file.split(".")

    gpt_res = db_results_fetch_one(
        db, LLM_TABLES_2[0], project_name=proj, test_suite_name=file_name
    )

    gemini_res = db_results_fetch_one(
        db, LLM_TABLES_2[1], project_name=proj, test_suite_name=file_name
    )

    llama_res = db_results_fetch_one(
        db, LLM_TABLES_2[2], project_name=proj, test_suite_name=file_name
    )

    return gpt_res, gemini_res, llama_res
