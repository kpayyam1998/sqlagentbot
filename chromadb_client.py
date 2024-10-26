from dotenv import load_dotenv
#from langchain_chr.vectorstores import Chroma
from langchain_chroma import Chroma

from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_retrieval_chain,create_history_aware_retriever

from typing import Dict

chat_history = []

class Chormadb:
    def __init__(self):
        load_dotenv()
        self.openai = ChatOpenAI(model="gpt-3.5-turbo-1106",temperature=0.7)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    
    def createdb(self):


        

        # Load url
        loaders=UnstructuredURLLoader(urls=[
            "https://www.icicibank.com/personal-banking/cards/credit-card",
            "https://www.hdfcbank.com/personal/pay/cards/credit-cards",
        ])

        data=loaders.load()



        # splitting chunkingour data
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        docs=text_splitter.split_documents(data)


        vector_store=Chroma.from_documents(documents=docs,embedding=self.embeddings,persist_directory="./ChormaDB")

        print("DB created")

    def loadchromadb(self):
        vector_store = Chroma(persist_directory="./ChormaDB",embedding_function=self.embeddings)

        retriever = vector_store.as_retriever(k=4)

        return retriever
    
    def generate_response(self):
        retriever = self.loadchromadb()

        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            self.openai, retriever, contextualize_q_prompt
        )





        SYSTEM_TEMPLATE = """
            You are the helpfull assistant to get best and suitable Answer the user's questions based on the below context. 
            If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

                    <context>
                    {context}
                    </context>
                    """
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_TEMPLATE
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ]
        )



        question_answer_chain = create_stuff_documents_chain(llm=self.openai,prompt=qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        return rag_chain
        


if __name__=="__main__":
    db = Chormadb()

    rag_chain = db.generate_response()

    response = rag_chain.invoke({"input" : "Explain about this Millennia Credit Card card and offer details", "chat_history" :chat_history})

    print(response['answer'])