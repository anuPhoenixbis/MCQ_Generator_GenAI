from dotenv import load_dotenv
import os
import streamlit as st
from google import genai

#prepare the environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini client
client = genai.Client()

response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents="Write a SQL query to find the names of all employees who work in the 'Sales' department and have a salary greater than 50000."
)

print(response.text)
