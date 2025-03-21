import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define the API URL
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Streamlit UI
st.title("Groq API Chatbot")

# Sidebar for API Key and Model Selection
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password", value=GROQ_API_KEY)
model = st.sidebar.selectbox("Select Model", ["llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

# User Input
st.write("Ask me anything!")
user_input = st.text_input("You:")

# Function to Generate Response
def generate_response(question, api_key, model, temperature, max_tokens):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.json()}"

# Display Response
if user_input and api_key:
    response = generate_response(user_input, api_key, model, temperature, max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter your Groq API key in the sidebar.")
