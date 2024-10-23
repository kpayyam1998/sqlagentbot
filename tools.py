from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenAI(
    temperature=0.9,max_tokens=500
)
@tool
def SqlQueryGenerator(user_input : str)->str:
    """
    A tool that generates SQL queries based on user input.
    """
   
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are an helpfull assistent , i dont know how to write best SQL Queries for my problem"),
        
            ("user","{query}")
        ]
    )

    chain = llm | prompt

    response=chain.invoke(user_input)

    return response


@tool
def SqlQuerySummarizer(user_input : str)->str:
    """
    A tool that generates SQL queries based on user input.
    """
   
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are an helpfull assistent , Summarize the SQL Queries"),
        
            ("user","{query}")
        ]
    )

    chain = llm | prompt
    response=chain.invoke(user_input)
    return response
