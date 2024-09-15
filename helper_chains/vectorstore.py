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
    """
    This class handles processing queries using a retrieval-based approach.

    Args:
        verbose (bool, optional): Whether to print verbose output. Defaults to True.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def __call__(self, query):
        """
        Processes a query using a retrieval approach.

        Args:
            query (str): The input query.

        Returns:
            str: The retrieved answer.
        """
        # Load conversation history (if any) for chat-memory purposes
        with open("summary.txt", 'r') as f:  
            self.history = f.read()

        # Initialize the RAG model and check-documents-relevance chain
        rag_model = initialize_gemini(api_config_path="config/api3.yaml") 
        check_relevance_object = relevance_chain()

        # Check relevance of retrieved documents to the query
        is_relevant, reason, docs_txt = check_relevance_object(query=query)
        
        # Iterate until relevant documents are found
        while(True):
            if self.verbose: 
                print(colored("[Logged Message] Relevance of docs to the query: " + is_relevant,'light_grey'))   
            if is_relevant:
                break
            else:
                # Reformulate query if not relevant 
                query = rag_model.invoke(f"rewrite this query so that it is best suitable for retrieval purposes: {query} because this query wasn't relevant due to this reason:{reason}")
                is_relevant, reason, docs_txt = check_relevance_object(query=query)   
        # Build the retrieval chain
        chain = (
                {"context": RunnableLambda(lambda x: docs_txt) , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | retriever_prompt
                | rag_model
                | StrOutputParser()
        )
        # Execute the retrieval chain and return the answer
        return chain.invoke(query)
