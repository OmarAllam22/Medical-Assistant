import sys
if "../" not in sys.path:
    sys.path.append("../")

from tools.search_web import WebSearch
from prompts.web_search_prompt import web_search_prompt
from utils.initialize_gemini import initialize_gemini

from langchain_core.output_parsers import StrOutputParser
from termcolor import colored
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

class web_search_chain:
    def __call__(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        self.web_model = initialize_gemini(api_config_path="config/api2.yaml")
        search_object = WebSearch()
        chain = (
                {"context": search_object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | web_search_prompt
                | self.web_model
                | StrOutputParser()
        )
        return chain.invoke(query)
