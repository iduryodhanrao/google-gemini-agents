import sqlite3
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()


def main():
    instruction = """You are an expert in financial and banking products. 
    Your task is to answer questions related to financial terminology in easily language. Use analogies and examples that are relatable. 
    Use humor and make the conversation both educational and interesting. Ask questions so that you can better understand the 
    user and improve the experience. 
    Suggest way that these concepts can be related to the real world.
    """


    # Set the GOOGLE_API_KEY from the environment
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    # Start a chat with automatic function calling enabled.
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction
        ),
    )

    #resp = chat.send_message("What is the cheapest product?")
    #print(f"\n{resp.text}")
    #resp = chat.send_message("Customer names with products ordered")
    #print(f"\n{resp.text}")

    print("General Bot: Hello, how can i help you? or enter 'quit' when you are done")
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