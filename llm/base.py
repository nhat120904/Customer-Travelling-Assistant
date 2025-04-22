from abc import ABC, abstractmethod
 
class BaseLLM(ABC):
    def __init__(self):
        pass
   
    @abstractmethod
    def raw_gen(
        self,
        model, messages, stream, tools, *args, **kwargs
    ):
        pass
   
    @abstractmethod
    def stream_gen(
        self,
        model, messages, stream, tools, *args, **kwargs
    ):
        pass
   