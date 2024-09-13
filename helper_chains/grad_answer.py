from langchain_core.output_parsers import JsonOutputParser

class grad_answer_chain:
    def __call__(self, prompt, model, query, answer):
        """
        helper function used to grad the answer as good answer or bad answer. 
        """
        answer_grader = prompt | model | JsonOutputParser()
        return answer_grader.invoke({"query": query, "answer": answer})['is_good_answer']
    