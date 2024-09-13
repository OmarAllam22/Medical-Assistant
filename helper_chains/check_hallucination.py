from langchain_core.output_parsers import JsonOutputParser

class hallucination_chain:
    def __call__(self, model, query, answer, check_hallucination_prompt, ReAct_messages, ReAct_prompt): 
        """
        helper function used to check if there is hallucination in the answer or not. 
        """
        hallucination_grader = check_hallucination_prompt | model | JsonOutputParser()
        
        return hallucination_grader.invoke({"query": query, "answer": answer, "messages":ReAct_messages, "ReAct_system_template": ReAct_prompt})['is_hallucinating']
