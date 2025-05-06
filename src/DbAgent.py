import sqlite3
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

#connect to sqllite
db_file = "database/testdb.db"
db_conn = sqlite3.connect(db_file)

#sql functions
# get the list of tables in the database
def list_tables() -> list[str]:
    """Retrieve the names of all tables in the database."""
    # Include print logging statements so you can see when functions are being called.
    #print(' - DB CALL: list_tables()')

    cursor = db_conn.cursor()

    # Fetch the table names.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()
    return [t[0] for t in tables]

# Get the schema for a specific table.
def describe_table(table_name: str) -> list[tuple[str, str]]:
    """Look up the table schema.

    Returns:
      List of columns, where each entry is a tuple of (column, type).
    """
    #print(f' - DB CALL: describe_table({table_name})')

    cursor = db_conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")

    schema = cursor.fetchall()
    # [column index, column name, column type, ...]
    return [(col[1], col[2]) for col in schema]

#execute sql function
def execute_query(sql: str) -> list[list[str]]:
    """Execute an SQL statement, returning the results."""
    print(f' - DB CALL: execute_query({sql})')

    cursor = db_conn.cursor()

    cursor.execute(sql)
    return cursor.fetchall()

def main():
    # These are the Python functions defined above.
    db_tools = [list_tables, describe_table, execute_query]

    instruction = """You are a helpful chatbot that can interact with an SQL database
    for a computer store. You will take the users questions and turn them into SQL
    queries using the tools available. Once you have the information you need, you will
    answer the user's question using the data returned. 

    Use list_tables to see what tables are present, describe_table to understand the
    schema, and execute_query to issue an SQL SELECT query


    Use below business rules to answer the user queries:
    CPM = CPI = Cost per Impression = Spend / Number of impressions
    CPQS = Cost per Quote Start = Spend / number of Quote Starts
    CPQC = Cost per Quote Complete = Spend / number of Quote Completes
    CPAS = Cost per Application Start = Spend / number of application starts
    CPAC = Cost per Application Complete = Spend / number of application completes
    CPP = Cost per Product Acquisition = Spend / number of Products acquired
    member number = member_id
    product = campaign_product, converted_product
    channel = conversion_channel
    conversion type = quote_start, quote_complete, app_start, app_complete, prod_acq
    cosa = lob, line of business, campaign_cosa, converted_cosa
    funding source = campaign_funding_source, funding_source
    demography = geography, city, state, region, country, age group
    quote = quote, quote start, quote complete, quote conversion
    applications = app, application, app start, app complete, app conversion

    When checking for string values convert them to lower case in both the SQL and the user input.
    eg. get me the campaign name for Auto insurance from paid channel tables

    Keep trying until you get the correct SQL statement. 
    Once you have the SQL statement, execute it using the execute_query function.
    for questions like "give me the all the campaign names" or "give me the all the campaign names for auto insurance"
    provide the sql query with distinct keyword in it.


    if the sql running for more than 15 seconds then stop the execution and return a message saying "SQL query is taking too long to execute. Please try again with a different query".


    final: 
    Display the output in table format properly column aligned.
    If the SQL returns greater than 100 rows then display only 100 rows and put a message at the end of the table saying "Only 100 rows displayed".
    """


    # Set the GOOGLE_API_KEY from the environment
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    """#test gemini api
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Explain how AI works in a few words"
    )
    print(response.text)"""

    # Start a chat with automatic function calling enabled.
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            tools=db_tools,
        ),
    )

    #resp = chat.send_message("What is the cheapest product?")
    #print(f"\n{resp.text}")
    #resp = chat.send_message("Customer names with products ordered")
    #print(f"\n{resp.text}")

    # Send the user input to the chat
    print("SQL Bot: Hello, I can help you with writing SQLs and executing on the database. \n how can I help you? or when you are done enter 'quit'")
    user_input = input("You: ")

    while 'quit' not in user_input.lower():

        
        #rint()

        response = chat.send_message(user_input)

        model_response = response.text

        print(f'Bot: {model_response}')
        print()
        user_input = input("You: ")

if __name__ == "__main__":
    main()