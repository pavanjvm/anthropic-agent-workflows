from base_agent import AgentBaseclass
from loguru import logger
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel

class OutputResult(BaseModel):
    problem: str
    product: str
    urgency: str
    solution: str
    next_step: str

class PromptChaining(AgentBaseclass):
    def __init__(self,name,max_retries,system,client,output_class):
        super().__init__(name,max_retries,system,client,output_class)      
    
    def execute(self,input):
        
        self.input = input
        self.messages.append({"role":"user","content":self.input})
        logger.info(f"appending input to prompt.")
        response = self.call_llm(self.messages)
        result = json.loads(response)
        logger.info(f"response from first llm call {result}")
        if result["next_step"] == "final_answer":

            return result
        elif result["next_step"] =="pass_to_next_LLM":
            self.messages.append({"role":"assistant","content":json.dumps(result)})
            final_response = self.call_llm(self.messages)
            logger.info(f"response from the second llm call")
            parsed = json.loads(final_response)
            print(parsed["solution"])  


import json
from system_prompt import prompt_chaining
system_message = prompt_chaining
from openai import OpenAI
client = OpenAI()
from dotenv import load_dotenv
load_dotenv

chaining_agent = PromptChaining(name = "laptop problem analyser",  
                                max_retries = 2,
                                system = system_message,
                                client = client,
                                output_class = OutputResult )
                                

                                
result = chaining_agent.execute('''
                       "User email: "My laptop keeps overheating and shuts down randomly. I need this fixed ASAP!"
                        Task: Summarize the problem and provide structured information for the next agent.
                    ''')
print(result)