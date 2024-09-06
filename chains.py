from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from termcolor import colored
from tools.search_web import WebSearch

class RagChain:
    def __init__(self,
                 rag_model, 
                 summarization_model, 
                 retriever, 
                 retriever_prompt, 
                 summarization_prompt,
                 web_search_prompt):
        
        self.rag_model = rag_model
        self.summarization_model = summarization_model
        self.retriever = retriever
        self.retriever_prompt = retriever_prompt
        self.summarization_prompt = summarization_prompt
        self.web_search_prompt = web_search_prompt
        self.history = ""
        # initialize the history file to empty string.
        with open("summary.txt", 'w') as f:
            f.write("")

    def _format_docs(self, docs):
        """
        helper function used in the chain to get the text from the retrieved docs 
        """
        return "\n\n".join(doc.page_content for doc in docs)
    
    
    def _get_rag_chain(self):
        return (
                {"context": self.retriever | self._format_docs, "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.retriever_prompt
                | self.rag_model
                | StrOutputParser()
        )
    
    def _get_search_chain(self):
        object = WebSearch()
        return (
                {"context": object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.web_search_prompt
                | self.rag_model
                | StrOutputParser()
        )
    
    def _get_summarization_chain(self):
        """
        this chain is used for memory purposes.
        """
        return self.summarization_prompt | self.summarization_model | StrOutputParser()


    def invoke(self, chain_type='rag'):
        if chain_type == 'rag':
            main_chain = self._get_rag_chain()
        elif chain_type == 'search':
            main_chain = self._get_search_chain()
        summarization_chain = self._get_summarization_chain()
        while True:
            query = input(colored("Input your query: ",'green'))
            if "exit" == query.lower().strip():
                break
            chunks = main_chain.stream(query)
            response = ""
            print(colored("Answer: ","green"), end="")
            for chunk in chunks:
                print(colored(chunk,"magenta"), end="", flush=True)
                response += chunk
            with open("summary.txt", 'a') as f:
                f.write("user query: " + query + "\n" + "llm response: "+ response)
            with open("summary.txt", 'r') as f:  
                self.history = f.read()

            self.history = summarization_chain.invoke(self.history)