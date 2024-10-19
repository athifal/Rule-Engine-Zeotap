import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
connection = sqlite3.connect('rules.db')
print("Database connected successfully")
