import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

#Load api key
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Chat

llm = ChatOpenAI(temperature=0.9, max_tokens=150)

# Function to generate a response

def generate_response(user_message : str) -> str:
    messages=[
        (
            "system",
            "You are a helpful assistent you are going to teach me the steps to learn english"
        ),
        ("human",user_message)
    ]
    response=llm.invoke(messages)

    return response.content

# Test the function

user_message = "How to speak english in 30 days?"
print(generate_response(user_message))

