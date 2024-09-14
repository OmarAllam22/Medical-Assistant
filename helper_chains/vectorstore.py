import sys
if "../" not in sys.path:
    sys.path.append("../")

from utils.initialize_gemini import initialize_gemini
from helper_chains.check_relevance import relevance_chain
from prompts.retriever_prompt import retriever_prompt

from langchain_core.output_parsers import StrOutputParser
from termcolor import colored
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


class vectorstore_chain:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def __call__(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()

        rag_model = initialize_gemini(api_config_path="config/api3.yaml") 
        check_relevance_object = relevance_chain()
        is_relevant, reason, docs_txt = check_relevance_object(query=query)
        
        while(True):
            if self.verbose: 
                print(colored("[Logged Message] Relevance of docs to the query: " + is_relevant,'light_grey'))   
            if is_relevant:
                break
            else:
                query = rag_model.invoke(f"rewrite this query so that it is best suitable for retrieval purposes: {query} because this query wasn't relevant due to this reason:{reason}")
                is_relevant, reason, docs_txt = check_relevance_object(query=query)   
        
        chain = (
                {"context": RunnableLambda(lambda x: docs_txt) , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | retriever_prompt
                | rag_model
                | StrOutputParser()
        )
        return chain.invoke(query)
