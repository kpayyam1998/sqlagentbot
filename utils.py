import json
from openai import OpenAI
from retriver import Retriver
from chromadb_client import Chormadb
openai=OpenAI()

def get_fancy_names(question :str):

    """Get flight information between two locations."""
    response=openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": question},
        ],
        max_tokens=100,
        temperature=0.7,
        n=1,
    )
    response=response.choices[0].message.content.replace("\n","")

    return response
   

def get_creditcard_info(question :str):
    chat_history = []
    db=Chormadb()
    rag_chain = db.generate_response()
    response = rag_chain.invoke({"input" : question, "chat_history" :chat_history})

    return response['answer']

