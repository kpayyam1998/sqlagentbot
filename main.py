import os
import streamlit as st
from streamlit_chat import message
import requests  # Required for making API requests

st.title("CreditCard QA Bot using OpenAI")

# API endpoint
API_URL = "http://127.0.0.1:5000/functioncallchat"

def process_question(data):
    """Makes a request to the API with user input and returns the response."""
    try:
        # Send a POST request to the API
        response = requests.post(API_URL, json=data)
        
        # Check if the response is successful
        if response.status_code == 200:
            # Parse the JSON response from the API
            return response.json().get("response", "No response received.")
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: Could not connect to API. {str(e)}"

def display_conversation(state):
    """Displays the conversation history using Streamlit messages."""
    for i in range(len(state["generated"])):
        # Display the user message
        message(state["past"][i], is_user=True, key=f"user_{i}")
        # Display the bot's response
        message(state["generated"][i], key=f"bot_{i}")

def main():
    st.markdown("<h4 style='color:black;'>Chat Here</h4>", unsafe_allow_html=True)

    # Prompt for user input
    user_input = st.text_input("Prompt", key="input")

    # Initialize session state to store conversation history
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["I am ready to help you"]
    if "past" not in st.session_state:
        st.session_state["past"] = ["hey there"]

    # Process user input and get a response
    if user_input:
        answer = process_question({'prompt': user_input})
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(answer)

    # Display the conversation history
    if st.session_state["generated"]:
        display_conversation(st.session_state)

if __name__ == "__main__":
    main()
