from llm.openai import OpenAILLM, AzureOpenAILLM
from configs.config import LLMConfig
 
class LLMCreator:
   
    llm_creators = {
        "openai": OpenAILLM,
        "azure_openai": AzureOpenAILLM
    }
   
    @classmethod
    def create_llm(cls, llm_type, *args, **kwargs):
        llm_creator = cls.llm_creators.get(llm_type.lower())
        if llm_creator:
            return llm_creator(*args, **kwargs)
        else:
            raise ValueError(f"No LLM creator found for type {llm_type}")
       
llm = LLMCreator().create_llm(
    llm_type=LLMConfig.model_type
)
 
__all__ = ["LLMCreator", "llm"]