import json
from openai import OpenAI

from utils import get_creditcard_info,get_fancy_names

class FunctionCall:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_fancy_names",
                "description": "This question will ask user to answered to llm.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "This question will ask user to answered to llm .",
                        },
                    },
                    "required": ["question"],
                    
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_creditcard_info",
                "description": "This funtion will return the credit card details  informations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "question": "This question will ask user to answered to llm .",
                        },
                    },
                    "required": ["question"],
                },
            }
        },
    ]


    def __init__(self) :

        self.openai = OpenAI()
            

    def process_function_call(cls, query):

        output = cls.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role" : "system",
                    "content" : " You are the helpfull assistence to give me the better results"
                },
                {
                    "role" : "user",
                    "content" : " user will ask questions which might be present in the llm or vector database"
                },
                {
                    "role" : "assistant",
                    "content" : "Hi there! I can help with that. Can you please provide more info?"
                },
                {
                    "role" : "user",
                    "content" : query
                }
            ],
            tools=cls.tools
        )

        return output
    def generate_reponse(self,user_prompt):

        output=self.process_function_call(user_prompt)
        if output:
            llm_response=output.choices[0].message.tool_calls
            # Making which function will call
            if llm_response:
                function_name=output.choices[0].message.tool_calls[0].function.name
                if function_name == "get_creditcard_info":
                    creadit_card_info=json.loads(output.choices[0].message.tool_calls[0].function.arguments)
                    card_function=eval(output.choices[0].message.tool_calls[0].function.name)
                    pixel_play_card = card_function(**creadit_card_info)
                    #print(pixel_play_card)
                    return pixel_play_card

                elif function_name == "get_fancy_names":
                    fancy_info=json.loads(output.choices[0].message.tool_calls[0].function.arguments)
                    get_fancy_function=eval(output.choices[0].message.tool_calls[0].function.name)
                    fancy_names = get_fancy_function(**fancy_info)
                    #print(fancy_names)

                    return fancy_names

            #if name == "get_creditcard_info" :
            else:
                print("Error while getting function call from llm")
        else:
            print("Error in generating response from LLM")


            


