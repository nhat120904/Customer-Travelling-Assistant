from openai import OpenAI, AzureOpenAI
from llm.base import BaseLLM
from configs.config import LLMConfig
 
class OpenAILLM(BaseLLM):
    def __init__(self):
        super().__init__()
        if LLMConfig.openai_api_key:
            self.client = OpenAI(
                api_key=LLMConfig.openai_api_key,
                base_url=None
            )
        else:
            self.client = None
       
       
    def raw_gen(self, model, messages, stream, tools, *args, **kwargs):
        if tools:
            response = self.client.chat.completions.create(
                model=model, messages=messages, stream=stream, tools=tools, **kwargs
            )
            return response.choices[0]
        else:
            response = self.client.chat.completions.create(
                model=model, messages=messages, stream=stream, **kwargs
            )
            return response.choices[0].message.content
   
    def stream_gen(self, model, messages, stream, tools, *args, **kwargs):
        if tools:
            raise RuntimeError(f"Tools call are not supported in Streaming mode")
        response = self.client.chat.completions.create(
            model=model, messages=messages, stream=stream, **kwargs
        )
        for line in response:
            if line.choices[0].delta.content is not None:
                yield line.choices[0].delta.content
   
class AzureOpenAILLM(OpenAILLM):
    def __init__(self):
        super().__init__()
        self.client = AzureOpenAI(
            api_key=LLMConfig.azure_openai_key,
            api_version=LLMConfig.azure_openai_version,
            azure_deployment=LLMConfig.azure_openai_deployment,
            azure_endpoint=LLMConfig.azure_openai_endpoint,
        )