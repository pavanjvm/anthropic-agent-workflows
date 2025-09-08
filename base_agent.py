from abc import ABC, abstractmethod
from loguru import logger


class AgentBaseclass(ABC):
    def __init__(self,name,max_retries,system,client,output_class):
        self.name = name
        self.output_class = output_class
        self.max_retries = max_retries
        self.system = system
        self.messages = []
        self.client = client
        if self.system is not None:
            logger.info(f"appended system instruction to prompt")
            self.messages.append({"role":"system","content":self.system})
    @abstractmethod
    def execute(self,*args,**kwargs):
        pass
    def call_llm(self,messages):
        self.messages = messages
        retries = 0 
        while retries < self.max_retries:
            retries+=1
            try:
                logger.info("callig the llm...")
                response = self.client.responses.parse(
                    model= "gpt-5",
                    input = self.messages,
                    text_format = self.output_class
                )
                return response.output_text
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] error during llm call: {e}.Retry {retries}/{self.max_retries}")




    