import sqlite3
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import streamlit as st



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
    #print(f' - DB CALL: execute_query({sql})')
    st.write(f' - DB CALL: execute_query({sql})')

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

    Keep trying until you get the correct SQL statement. If the SQL returns more than 1 row then    
    display the output in tabular or table format properly column aligned.
    If the SQL returns only 1 row then display the output in a single line.
    """
    
    # Set the GOOGLE_API_KEY from the environment
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

    # Start a chat with automatic function calling enabled.
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            tools=db_tools,
        ),
    )
    # Set up the Streamlit app
    st.set_page_config(layout="wide", page_title="SQL Chatbot", page_icon=":robot_face:")

    # Initialize session state to store chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Set up the layout with two columns
    left_col, spacer, right_col = st.columns([5,0.2,5])
    with left_col:
        st.header("Chat with SQL Bot")
        #st.write("Hello, how can i help you?")
        user_input = st.text_input("You: ",key="user_input")
        if st.button("Send"):
        # Get user input and respond using the chat model
            if user_input.strip():
                response = chat.send_message(user_input)
                model_response = response.text
                st.write(f"Bot: {model_response}")
                bot_response =f'Bot: {model_response}'
                st.session_state.history.append(bot_response)
    
    # Add a spacer between the two columns
    with spacer:
        st.empty()

    # Right column: History pane
    with right_col:
        st.header("History")
        # Clear history button
        if st.button("Clear History"):
            st.session_state.history.clear()
            user_input = ""
            st.session_state[user_input] = ""        
            
        # Display history in a scrollable text area
        history_text = "\n".join(st.session_state.history)
        st.text_area("Conversation History:", value=history_text, height=400, key="history_area", disabled=True)

    

if __name__ == "__main__":
    main()