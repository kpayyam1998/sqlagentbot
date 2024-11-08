import os
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from chromadb_client import Chormadb

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory


class LangAgent:
    def __init__(self):
        self.llm=ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.db=Chormadb()
    


    #================================================================================================================================
    """
    Below fuction try to understand whether the query  based on the SQL or vector
    """
    #================================================================================================================================ 
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
    
    #================================================================================================================================
    """
    Below fuction Generate SQL query and store to data to mongo database
    """
    #================================================================================================================================ 
    def _generateSQlQuery(self,query:str,config):
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                            you are an helpfull asssistent based on the user query you should generate Optimize SQL Query.
                            if dont know the answer ask user to give more input. dont make anything smarter"""),
                ("human","{input}"),           
            ]
        )

        chain = self.prompt|self.llm

        
        sql_chat_response = RunnableWithMessageHistory(
            chain,
            get_session_history= lambda session_id : MongoDBChatMessageHistory(
                session_id = session_id,
                connection_string = os.getenv("MONGODB_CONNECTION_STRING"),
                database_name = os.getenv("MONGODB_DATABASE_NAME"),
                collection_name = os.getenv("MONGODB_COLLECTION_NAME")  # replace with your collection name
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        response = sql_chat_response.invoke({"input" : query},config=config)

        return response.content


    #================================================================================================================================
    """
    Below fuction make vector DB connection to store respnse and chat history to the mongo database
    """
    #================================================================================================================================
    def _generateVectorResponse(self,query:str, config):

        # write retriver function to genreate response if user ask different query
        qa_system_prompt = """You are an assistant for question-answering releated credit card tasks. \
                Use the following pieces of retrieved context to answer the question. \
                If you don't know the answer, just say that you don't know. \
                

                {context}"""
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")
            ]
        )
        qa_chain = create_stuff_documents_chain(self.llm,qa_prompt)

        rag_chain = create_retrieval_chain(self.db.loadchromadb(),qa_chain)

        vector_response = RunnableWithMessageHistory(
            rag_chain,
            get_session_history= lambda session_id : MongoDBChatMessageHistory(
                session_id = session_id,
                connection_string = os.getenv("MONGODB_CONNECTION_STRING"),
                database_name = os.getenv("MONGODB_DATABASE_NAME"),
                collection_name = os.getenv("MONGODB_COLLECTION_NAME")  # replace with your collection name
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        response = vector_response.invoke({"input" : query},config=config)
        return response['answer']


    #================================================================================================================================
    """
    Below fuction decide whether we need to call SQL LLM or VectorDB
    """
    #================================================================================================================================
    def sql_or_vector(self,query):
        response_content = self._generateResponse(query)

        config = { "configurable" : { "session_id" : str(uuid.uuid4()) }}

        if response_content.lower() =='sql':
            qry_response = self._generateSQlQuery(query,config)
            print(qry_response)
        else :
            response = self._generateVectorResponse(query,config)

            print(response)

    

# if __name__ == '__main__':
#     agent = LangAgent()
#     print(agent.sql_or_vector("How to retrieve the top 10 records in sql table?")) # Explain about this Millennia Credit Card card and offer details?
