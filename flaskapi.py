from flask import Flask,request
from agent import LangAgent
app = Flask(__name__)

@app.route("/")
def start():
    return "success"

@app.route("/chat", methods=["POST"])
def chat():
    try:

        prompt = request.json["prompt"]
        #print(f"User input: {prompt}")
        if not prompt:
            return {"error": "No user input provided"}, 400
        
        # Create an instance of the LangAgent class and use it to generate a response
        lang_agent = LangAgent()
        agentexcutor = lang_agent.botagent()
        

        response = lang_agent.generate_response(agentexcutor,prompt)

        #print(response)
        return {"response": response}
    
    except Exception as e:
        return {"error": str(e)}, 500
    
if __name__=="__main__":
    app.run(debug=True)