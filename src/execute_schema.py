import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("database/testdb.db")
cursor = conn.cursor()

# Read the schema.sql file
#with open(r"e:\MyRepo\New folder\google-gemini-sql-agent\database\schema.sql", "r") as file:
#    schema = file.read()

# Read the seed_Data.sql file
with open(r"database/seed_data.sql", "r") as file:
    schema = file.read()

# Execute the schema
cursor.executescript(schema)

# Commit and close the connection
conn.commit()
conn.close()

print("Schema executed successfully!")