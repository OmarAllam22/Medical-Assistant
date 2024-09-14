import sys
if "../" not in sys.path:
    sys.path.append("../")

from prompts.llm_knowledge_prompt import llm_knowledge_prompt
from utils.initialize_gemini import initialize_gemini

from langchain_core.output_parsers import StrOutputParser
from termcolor import colored
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

class llm_knowledge_chain:
    def __call__(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        self.llm_knowledge_model = initialize_gemini(api_config_path="config/api4.yaml")
        chain = (
                {"question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | llm_knowledge_prompt
                | self.llm_knowledge_model
                | StrOutputParser()
        )
        return chain.invoke(query)
        