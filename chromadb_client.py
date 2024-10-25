from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.runnables import RunnablePassthrough

from typing import Dict
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

openai = ChatOpenAI(model="gpt-3.5-turbo-1106",temperature=0.7)

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


vector_store=Chroma.from_documents(documents=docs,embedding=embeddings,persist_directory="./ChormaDB")


retriever = vector_store.as_retriever(k=4)

docs=retriever.invoke("Explain about this Millennia Credit Card card and offer details")




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
        MessagesPlaceholder(variable_name="chat_history")
    ]
)

document_chain = create_stuff_documents_chain(llm=openai,prompt=qa_prompt)

# response=document_chain.invoke(
#     {
#         "context": docs,
#         "chat_history":(
#             HumanMessage(content="Explain about this Millennia Credit Card card and offer details")
#         )
#     }
# )



def parse_retriver_input(params:Dict):
    return params['chat_history'][-1].content


retrieval_chain=RunnablePassthrough.assign(
    context = parse_retriver_input | retriever,
).assign(answer = document_chain)

#Creating Chain to make better answer

final_res=retrieval_chain.invoke(
    {
        "chat_history": [
            HumanMessage(content="Explain about this Millennia Credit Card card and offer details?")
        ],
    }
)

print(final_res['answer'])



# if __name__=="__main__":
#     print(res)
