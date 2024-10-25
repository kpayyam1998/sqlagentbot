from langchain_openai import OpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain


class Retriver:
    def __init__(self):
        self.llm=OpenAI()
        self.embeddings=OpenAIEmbeddings()
        

    def vectordb_retriver(self):
        # # Load Vector
        vectordb=FAISS.load_local("credicard",self.embeddings,allow_dangerous_deserialization=True)
        # retriever
        retrieverdb=vectordb.as_retriever(search_kwargs={'k': 3})

        #llm = OpenAI(temperature=0.9,max_tokens=400)

        # Create chain
        chain=RetrievalQAWithSourcesChain.from_chain_type(self.llm, chain_type="stuff", retriever=retrieverdb)

        return chain

