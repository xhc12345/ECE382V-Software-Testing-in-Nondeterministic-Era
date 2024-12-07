import sqlite3


def db_init_table(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            testname TEXT NOT NULL,
            testfile TEXT NOT NULL,
            repo TEXT NOT NULL
        )
        """
    )
    db.commit()


def db_tests_insert(db: sqlite3.Connection, testName, testFile, repo):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tests (testname, testfile, repo) VALUES (?, ?, ?)",
        (testName, testFile, repo),
        # ("test1", "testFile.py", "testOrg/testRepo"),
    )
    db.commit()


def db_tests_get_all(db: sqlite3.Connection):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM tests")
    all_tests = cursor.fetchall()

    return all_tests
