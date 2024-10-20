# Rule Engine Application

This project is a **Rule Engine** built with **Flask** and **SQLAlchemy**, providing an API for creating, combining, and evaluating rules based on custom logical expressions. It supports CRUD operations for rules stored in a SQLite database and offers functionalities for evaluating these rules against given data.

## Objective
The objective of this application is to develop a rule engine that determines user eligibility based on attributes such as age, department, income, and spend. The engine utilizes an Abstract Syntax Tree (AST) to represent conditional rules.

## Features

- Create rules with custom logical expressions.
- Combine multiple rules using logical operators (AND, OR).
- Evaluate rules against a dataset.
- Store rules in an SQLite database.
- Fetch all saved rules from the database.

## Technologies Used

- **Backend**: Python, Flask, Flask-RESTful, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, JavaScript (Optional)
- **Database**: SQLite
- **Others**: Flask-CORS

## Project Structure

```bash

├── __pycache__/
├── frontend/
│   ├── index.html            # Frontend (optional)
│   ├── script.js             # JavaScript file for frontend interactions
│   └── styles.css            # CSS for styling
├── resources/
│   ├── __pycache__/
│   └── rule.py
├── venv/                     # Python virtual environment (optional)
├── app.py                # Main Flask application file
├── ast_nodes.py          # AST (Abstract Syntax Tree) node definition and utilities
├── attribute_catalog.py   # Attributes for rules
├── database.py           # Database setup (SQLAlchemy)
├── models.py             # Database models (Rules and Metadata)
├── rule_engine.py        # Rule parsing and evaluation engine
├── rules.py              # API resources for rule creation, combination, evaluation
├── requirements.txt      # Python dependencies
└── rules.db                  # SQLite database " give full code and i can copy the all code
```

##  Installation Instructions
Guide to set up the project in a local environment.


### Setup Instructions
Follow these steps to set up the project:


### Clone the repository
```bash
git clone https://github.com/athifal/Rule-Engine-Zeotap.git
cd Rule-Engine-Zeotap
```
### Set up a virtual environment (recommended)
```bash

python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```
### Install the required dependencies
```bash
pip install -r requirements.txt
```
### Run the application:
```bash
python app.py
```
#### Open your browser and go to http://localhost:5000.
## API Endpoints

- `POST /create_rule`: Create a new rule.
- `POST /combine_rules`: Combine multiple rules with logical operators (AND/OR).
- `POST /evaluate_rule`: Evaluate a rule against a dataset.
- `GET /grt_rules`: Get all stored rules.
## Database Information
The application uses SQLite to store rules. The database file rules.db will be automatically generated in the root directory when the Flask application is first run.
To inspect the database, use any SQLite browser or command-line tool:
```bash
sqlite3 rules.db
```
