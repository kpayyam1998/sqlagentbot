import os
import streamlit as st
from streamlit_chat import message
import base64
import requests  # Import requests library

def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i], key=str(i))

def main():
    # Set up Streamlit input and session state
    user_input = st.text_input("Prompt", key="input")

    if "generated" not in st.session_state:
        st.session_state["generated"] = ["I am ready to help you"]
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey there"]

    if user_input:
        # Add user input to conversation history
        st.session_state["past"].append(user_input)

        # Make POST request to Flask API with user input
        try:
            response = requests.post(
                "http://127.0.0.1:5000/chat",
                json={"prompt": user_input}  # Send user_input as JSON
            )
            response_data = response.json()  # Parse JSON response

            # Assuming the response data contains the result under 'result' key
            answer = response_data.get("response")
            st.session_state["generated"].append(answer)

        except requests.exceptions.RequestException as e:
            st.session_state["generated"].append("Error: Could not reach the API.")
            st.error(f"Error: {e}")

    # Display conversation history
    if st.session_state["generated"]:
        display_conversation(st.session_state)

if __name__ == "__main__":
    main()
