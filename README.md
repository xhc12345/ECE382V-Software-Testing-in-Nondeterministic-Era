# ECE382V-Software-Testing-in-Nondeterministic-Era
Semester Project

## Requirements
This projects requires Docker to run. Please install Docker and make sure that `docker-compose` command works in your terminal.

## Setup
Copy `.env_copy` file and rename it to `.env`, then inside `.env`, change the `your_api_key_here` to its real repective API key that you need to provide on your own.

## Run
```bash
docker-compose up --build
```

## Complete Stop
```bash
docker-compose down
```

## Data
The `data/input` folder contains `.csv` data of the flaky tests collected from [International Dataset of Flaky Tests (IDoFT)](https://github.com/TestingResearchIllinois/idoft). These only include `Accepted` requests from the system to ensure their validity.

The `data/input` folder also contains `prompts.yaml` used for prompt engineering.

Sample flaky tests used for testing are located in `data/test-suites/example`, these are only used for building the system and are not actual real-world flaky tests (or are they? ;) ).

The actual flaky tests collected are located in subfolders inside `data/test-suites` folder, excluding `example`. Each subfolder name indicates the language of the test files. Inside each subfolder indicated by their language names are the folders for different projects, in there are the actual test suites.

Test suites can be collected manually by running
```bash
python3 data/collection/<scriptname>
```
where `<scriptname>` can be either `pull-py-data.py` or `pull-pr-data.py`. Each will pull python and java+groovy test suites, respectively. You need to give your own GitHub API Key in the `.env` file.

The actual results from running FlakyBusters are collected inside `data/database.db`.

All the collected summaries about the data and analysis are in `data/collection` folder as csv files.