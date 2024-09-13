from langchain_core.prompts import PromptTemplate

check_docs_relevance_prompt = PromptTemplate(
            template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
            Here is the retrieved document: \n\n {documents} \n\n
            Here is the user question: {question} \n
            If the document contains keywords related to the user question, grade it as relevant. \n
            It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.and reason your answer \n
            Provide the answer as a JSON with a two  keys 'is_relevant' and 'reason' and no premable or explanation.""",
            input_variables=["question", "documents"],
        )