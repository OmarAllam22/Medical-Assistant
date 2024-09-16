import sys
if "../" not in sys.path:
    sys.path.append("../")

from tools.search_web import WebSearch
from prompts.web_search_prompt import web_search_prompt
from utils.initialize_gemini import initialize_gemini
from helper_chains.summarization_chain import SummarizationChain

from langchain_core.output_parsers import StrOutputParser
from termcolor import colored
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

class web_search_chain:
    """
    This class performs has chain to extract knowledge got from the web_search tool found at `tools.search_web`.
    """

    def __init__(self):
        self.summarization_object = SummarizationChain() # for memory purposes.

    def __call__(self, query):
        """
        Processes a query using a web search chain.

        Args:
            query (str): The input query.

        Returns:
            str: The retrieved answer.
        """
        # Load conversation history (if any) for chat-memory purposes
        self.history = self.summarization_object.get_summary()

        # Initialize the model and web_search tool    
        self.web_model = initialize_gemini(api_config_path="config/api2.yaml")
        search_object = WebSearch()

        # Build the chain that gets the answer from the retrieved text by web_search tool
        chain = (
                {"context": search_object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | web_search_prompt
                | self.web_model
                | StrOutputParser()
        )
        # Execute the web search chain and return the answer
        return chain.invoke(query)
