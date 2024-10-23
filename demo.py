from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI()
def simpleCall(input:str):
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system","you are assistent to make best sql queires"),
            ("human",{input})

        ]
    )

    res=llm.invoke(prompt)
   

    return res 

print(simpleCall("top 20 records"))