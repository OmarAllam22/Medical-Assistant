import sys
if "../" not in sys.path:
    sys.path.append("../")

from prompts.grade_answer_prompt import grade_answer_prompt
from utils.initialize_gemini import initialize_gemini

from langchain_core.output_parsers import JsonOutputParser

class grad_answer_chain:
    def __call__(self, query, answer):
        """
        helper function used to grad the answer as good answer or bad answer. 
        """
        model = initialize_gemini(api_config_path="config/api4.yaml")
        answer_grader = grade_answer_prompt | model | JsonOutputParser()
        return answer_grader.invoke({"query": query, "answer": answer})['is_good_answer']
    