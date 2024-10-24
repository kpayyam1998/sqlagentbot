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

class LangAgent:
    def __init__(self):
        # Initialize the LLM

        self.llm = ChatOpenAI(
            temperature=0.7,
            max_tokens=100, # We can give as many as we want 
        
        )

        self.tool=[SqlQueryWritter,CompanyNameGenerator]
        self.llm_withtools=self.llm.bind_tools(self.tool)
        self.MEMORY_KEY = "chat_history"
        self.chat_history=[]


    def agent(self):

            # Create the prompt for the agent
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "you are a helpful assistant to write queries or summarize queries"),
                    MessagesPlaceholder(variable_name=self.MEMORY_KEY),
                    ("user", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),


                ]
            )


            agent=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                    "chat_history": lambda x : x['chat_history']
                }
                | prompt
                | self.llm_withtools
                | OpenAIToolsAgentOutputParser()
            )


            agent_executor = AgentExecutor(agent=agent, tools=self.tool) # verbose=True which will help understand what is the process behind Agents

            return agent_executor
    def generate_response(self,agent_excutor,user_input):
            response = agent_excutor.invoke({"input":user_input,"chat_history":self.chat_history})
            return response['output']



if __name__=="__main__":
    lang_agent = LangAgent()
    agent_excutor = lang_agent.agent()
    input = "I am running pencil company name "
    res = lang_agent.generate_response(agent_excutor,input)
    print(res)