import sys
if "../" not in sys.path:
    sys.path.append("../")

from utils.initialize_gemini import initialize_gemini
from prompts.summarization_prompt import summarization_prompt
from langchain_core.output_parsers import StrOutputParser

class SummarizationChain:
    def get_summary(self):        
        with open("summary.txt","r") as f:
            self.chat_history = f.read()
        summarization_model = initialize_gemini(api_config_path="config/api2.yaml")
        chain = summarization_prompt | summarization_model | StrOutputParser()
        return chain.invoke({"text":self.chat_history})
    
    def add_current_query_response(self, query, response):
        with open("summary.txt","a") as f:
            f.write("user query: " + query + "\n" + "llm response: "+ response)
        