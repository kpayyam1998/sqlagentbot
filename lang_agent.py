from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
class LangAgent:
    def __init__(self):
        self.llm=ChatOpenAI()
        
    
    def _generateResponse(self,query:str):

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                            you are an helpfull asssistent based on the user query you should respond.
                            if the user asked SQL releated querey then return sql or SQL .Dont make anything smarter"""),
                ("human","{input}"),           
            ]
        )

        self.chain = self.prompt|self.llm

        response = self.chain.invoke({"input": query})

        return response.content
    def _generateSQlQuery(self,query:str):
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                            you are an helpfull asssistent based on the user query you should generate Optimize SQL Query.
                            if dont know the answer ask user to give more input. dont make anything smarter"""),
                ("human","{input}"),           
            ]
        )

        self.chain = self.prompt|self.llm

        response = self.chain.invoke({"input": query})

        return response.content
    
    def _generateVectorResponse(self,query):
        # write retriver function to genreate response if user ask different query
        pass

    def sql_or_vector(self,query):
        response_content = self._generateResponse(query)

        if response_content.lower() =='sql':
            # make one LLM Call to generate the SQL response
            qry_response = self._generateSQlQuery(query)
            print(qry_response)
        else :
            # use retriever to generate the reposn
            pass

    

if __name__ == '__main__':
    agent = LangAgent()
    print(agent.sql_or_vector("Insert record in sql table"))
    # print(agent._generateResponse("What is the SQL query to get the top 10 records"))
    # print(agent._generateResponse("Can you explain the SQL join operation?"))
    # print(agent._generateResponse("What is the SQL query to find the average salary of employees?"))
    # print(agent._generateResponse("What is the SQL query to update the employee's salary?"))
    # print(agent._generateResponse("What is the SQL query to delete the employee with ID 123?"))