from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",temperature=0.9,max_tokens=500
)

@tool
def SqlQueryWritter(user_input : str)->str:
    """
    A tool that generates SQL queries based on user input.
    """
   
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are an helpfull assistent to write the SQL Queries"),
        
            ("user","{query}")
        ]
    )

    chain = prompt | llm 

    response = chain.invoke({"query":user_input})

    return response.content



@tool
def CompanyNameGenerator(user_input : str)->str:
    """
    A tool that generates SQL queries based on user input.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are an helpfull assistent , Generate Beatifull comapnyname"),
        
            ("user","{query}")
        ]
    )

    chain = prompt | llm 

    response = chain.invoke({"query":user_input})

    return response.content
