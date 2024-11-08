from flask import Flask,request
from agent import LangAgent
from function_call_tools import FunctionCall
from logging.config import dictConfig

# Logging configuration for Console
dictConfig(
    {
        'version' : 1,
        'disable_existing_loggers' : False, # Don't disable Flask's default loggers
        'formatters' : {
            'default':{
                'format': ' %(asctime)s %(levelname)s in %(module)s : %(message)s '
            }
        },
        'handlers' : {
            'wsgi' : {
                'class' : 'logging.StreamHandler',
                'stream' : 'ext://flask.logging.wsgi_errors_stream', ## Direct to Flask's error stream
                'formatter' : 'default' 
            }
        },
        'root' : {
            'level' : 'INFO',
            'handlers' : ['wsgi']
        }
    }
)


app = Flask(__name__)

@app.route("/")
def start():
    app.logger.info("Started")
    return "success"

@app.route("/error")
def error():
    app.logger.error("An error occurred")
    return "An error occurred", 500

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