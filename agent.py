from dotenv import load_dotenv
from tools import CompanyNameGenerator,SqlQueryWritter

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    temperature=0,
    max_tokens=100,
  
)

tool=[SqlQueryWritter,CompanyNameGenerator]
llm_withtools=llm.bind_tools(tool)

def agent():
    # Create the tools

    MEMORY_KEY = "chat_history"
    # Create the prompt for the agent
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you are a helpful assistant to write queries or summarize queries"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )


    llm_withtools=llm.bind_tools(tool)
    agent=(
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_withtools
        | OpenAIToolsAgentOutputParser()
    )


    agent_executor = AgentExecutor(agent=agent, tools=tool)

    return agent_executor

def generate_response(agent_excutor,user_input):
    response = agent_excutor.invoke({"input":user_input})
    return response['output']



if __name__=="__main__":
    agent_excutor=agent()
    input="I am running pencil company name "
    res=generate_response(agent_excutor,input)
    print(res)