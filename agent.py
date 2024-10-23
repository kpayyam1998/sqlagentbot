from tools import SqlQueryGenerator,SqlQuerySummarizer
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor,ZeroShotAgent
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)

llm = ChatOpenAI(temperature=0.9,max_tokens=100)


tools_func=[SqlQueryGenerator,SqlQuerySummarizer]



prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are an helpfull assistent help me to write sql queires or summarize it"),
        
            ("user","{input}")
        ]
    )
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

agent =(
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
    }
    | prompt
    | llm.bind_tools(tools_func)
    | OpenAIToolsAgentOutputParser()
    )

# User input

agent_executor = AgentExecutor(agent=agent, tools=tools_func)


res = agent_executor.invoke({"input":"top 20 records display"})

print(res)




