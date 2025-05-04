import os
from dotenv import load_dotenv
import sqlite3
import google.generativeai as genai
import matplotlib.pyplot as plt

load_dotenv()

# Set up Google API key and Gemini Flash model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Database connection (example using SQLite)
conn = sqlite3.connect("database/testdb.db")
cursor = conn.cursor()

# Run SQL query
query = "SELECT name, price FROM product"
cursor.execute(query)
data = cursor.fetchall()
conn.close()

# Prepare prompt for AI agent
prompt = f"Given this data: {data}, analyze trends and suggest visualization."

# AI analyzes the data
response = model.generate_content(prompt)
analysis = response.text

print("AI Analysis:")
print(analysis)

# Extract data for visualization
categories, values = zip(*data)

# Generate a bar chart
plt.bar(categories, values)
plt.xlabel("Categories")
plt.ylabel("Values")
plt.title("Sales Data Chart (AI-Enhanced)")
plt.show()