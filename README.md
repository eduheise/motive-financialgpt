# FinancialGPT Repository

This repository houses a chat application with a LLM capable of extracting data from a SQL database and answer with it.

## Repository Structure

- `financialgpt/`: The core Python package, with the functions for financial data processing.
- `scripts/`: Utility scripts to operate with `financialgpt`.
- `tests/`: Unit tests.
- `data/`: Data used to process as the base sample to run build the SQL.

## Usage

All the dependencies from this repository is being managed by Poetry. Thus, we need to run this command to properly
install it and install the dependencies.

```bash
pip install poetry
poetry install
```

We also need a SQL database to store all the needed data. We are going to use PostgreSQL running in a Docker.

### Running with Docker Compose

To run the application using Docker Compose, ensure Docker and Docker Compose are installed. Navigate to the repository
directory and execute:

```bash
docker-compose up
````

### Populating Data with load_data.py

To populate the application with initial data, use the `load_data.py` script located in the scripts/ directory. Ensure
Docker containers are running, then execute:

```bash
python scripts/load_data.py
```

This script is going to create all tables needed and populate them with the samples.

### Running the Streamlit Chatbot

To run the Streamlit-based chatbot script (`chatbot.py`), ensure you have Streamlit installed and execute:

```bash
streamlit run scripts/chatbot.py
```

## Running Tests

Tests are included to validate the functionality of the financial processing tools. Use pytest to run all tests:

```bash
pytest
```

Ensure Python 3.x is installed and all dependencies are met before running the tests.