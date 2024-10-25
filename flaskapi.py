from flask import Flask,request
from agent import LangAgent
from function_call_tools import FunctionCall
app = Flask(__name__)

@app.route("/")
def start():
    return "success"


# Below api works for Custom Agent
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
    


#Below API works for FunctionCall
@app.route("/functioncallchat",methods=["POST"])
def functioncallchat():
    try:
        prompt = request.json["prompt"]
        print(prompt)
        if not prompt:
            return {"error": "No user input provided"}, 400
        
        function_call = FunctionCall()
        response = function_call.generate_reponse(prompt)

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}, 500

if __name__=="__main__":
    app.run(debug=True)