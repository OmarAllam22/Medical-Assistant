import sys
if "../" not in sys.path:
    sys.path.append("../")

from prompts.check_hallucination_prompt import check_hallucination_prompt
from prompts.ReAct_system_template import ReAct_system_template
from utils.initialize_gemini import initialize_gemini

from langchain_core.output_parsers import JsonOutputParser

class hallucination_chain:
    def __call__(self, query, answer, ReAct_messages): 
        """
        helper function used to check if there is hallucination in the answer or not. 
        """
        model = initialize_gemini(api_config_path="config/api2.yaml")
        hallucination_grader = check_hallucination_prompt | model | JsonOutputParser()
        
        return hallucination_grader.invoke({"query": query, "answer": answer, "messages":ReAct_messages, "ReAct_system_template": ReAct_system_template})['is_hallucinating']
