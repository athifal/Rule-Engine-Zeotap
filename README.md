# Rule Engine Application

This project is a **Rule Engine** built with **Flask** and **SQLAlchemy**, providing an API for creating, combining, and evaluating rules based on custom logical expressions. It supports CRUD operations for rules stored in a SQLite database and offers functionalities for evaluating these rules against given data.

## Features

- Create rules with custom logical expressions.
- Combine multiple rules using logical operators (AND, OR).
- Evaluate rules against a dataset.
- Store rules in an SQLite database.
- Fetch all saved rules from the database.

## Technologies Used

- **Backend**: Flask, Flask-RESTful, SQLAlchemy, SQLite
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

## 1. Installation Instructions
Guide to set up the project in a local environment.


### Setup Instructions
Follow these steps to set up the project:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-folder>

# Set up a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

# Install the required dependencies
pip install -r requirements.txt
