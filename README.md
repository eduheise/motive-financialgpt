# FinancialGPT Repository

This repository houses tools and scripts designed for financial data processing and analysis using Python. It includes
core functionalities for modeling financial data and utility scripts for various data operations.

## Repository Structure

- `financialgpt/`: Core Python package for financial data processing.
- `scripts/`: Utility scripts for data manipulation and processing.
- `tests/`: Unit tests to validate functionality and ensure code robustness.
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