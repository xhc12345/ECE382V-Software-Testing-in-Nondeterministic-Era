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
