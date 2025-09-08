# from openai import OpenAI
from abc import ABC, abstractmethod
from loguru import logger

# client = OpenAI()

class AgentBaseclass(ABC):
    def __init__(self,name,max_retries,system,client):
        self.name = name
        self.max_iterations = max_retries
        self.system = system
        self.messages = []
        if self.system is not None:
            self.messages.append({"role":"system","content":self.system})
    @abstractmethod
    def exectutor(self,*args,**kwargs):
        pass
    def call_llm(self,input):
        self.input = input
        self.messages.append({"role":"user","content":self.input})
        retries = 0 
        while retries < self.max_retries:
            retries+=1
            try:
                response = self.client.responses.create(
                    model= "gpt-5",
                    input = self.messages
                )
                return response.output_text
            except Exception as e:
                retires += 1
                logger.error(f"[{self.name}] error during llm call: {e}.Retry {retries}/{self.max_retries}")


class PromptChaining:
    pass
class Routing:
    pass
class Parallelizationn:
    pass
class OrchestratorWorker:
    pass
class EvaluatorOptimizer:
    pass
