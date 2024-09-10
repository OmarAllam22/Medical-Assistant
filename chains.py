from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from termcolor import colored
from tools.search_web import WebSearch
from prompts.retriever_prompt import retriever_prompt
from prompts.web_search_prompt import web_search_prompt 
from prompts.summarization_prompt import summarization_prompt
from prompts.router_prompt import router_prompt
from prompts.ReAct_system_template import ReAct_system_temp
from langchain_core.prompts import ChatPromptTemplate
import re

class Agent:
    def __init__(self,
                 rag_model, 
                 summarization_model,
                 react_model,
                 tools:list, 
                 retriever
                 ):
        
        self.rag_model = rag_model
        self.summarization_model = summarization_model
        self.react_model = react_model
        self.tools = tools
        self.retriever = retriever
        self.router_prompt = router_prompt
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
    
    
    def _execute_rag_chain(self, query):
        chain = (
                {"context": self.retriever | self._format_docs, "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.retriever_prompt
                | self.rag_model
                | StrOutputParser()
        )
        return chain.invoke(query)
    
    def _execute_search_chain(self, query):
        object = WebSearch()
        chain = (
                {"context": object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.web_search_prompt
                | self.rag_model
                | StrOutputParser()
        )
        return chain.invoke(query)
    
    def _excute_summarization_chain(self, text):
        """
        this chain is used for memory purposes.
        """
        chain = self.summarization_prompt | self.summarization_model | StrOutputParser()
        return chain.invoke(text)

    def _execute_router_chain(self, query)->str:
        """
        returns the datasource to which will be routed a choice from ['vectorstore','web_search'].
        """
        with open('book_summaries_for_Agent.txt','r') as f:
            content = f.read()

        chain = (
            {"question": RunnablePassthrough(), "content": RunnableLambda(lambda x: content)} 
            | router_prompt 
            | self.rag_model 
            | JsonOutputParser()
        )
        return chain.invoke(query)['datasource']
    
    def _execute_ReAct(self, query):
        object = ReActAgent(self.react_model, self.tools, system=ReAct_system_temp)
        return object(query)

    def invoke(self):

        while True:
            query = input(colored("Input your query: ",'green'))
            if "exit" == query.lower().strip():
                break
            try:
                datasource = self._execute_router_chain(query)
                print(colored("Answer: ","green"), end="")
                if datasource == 'vectorstore':
                    response = self._execute_rag_chain(query)
                    print(colored(response,"magenta"), end="", flush=True)
                    with open("summary.txt", 'a') as f:
                        f.write("user query: " + query + "\n" + "llm response: "+ response)
                    with open("summary.txt", 'r') as f:  
                        self.history = f.read()
                    self.history = self._excute_summarization_chain(self.history)

                elif datasource == 'web_search':      
                    response = self._execute_ReAct(query)
                    print(colored(response,"magenta"), end="", flush=True)
                    with open("summary.txt", 'a') as f:
                        f.write("user query: " + query + "\n" + "llm response: "+ response)
                    with open("summary.txt", 'r') as f:  
                        self.history = f.read()
                    self.history = self._excute_summarization_chain(self.history)
                    
            except Exception as e: 
                print(colored(f"Error arises due to the following exception {e}", 'red'))

#####################################################################################

class ReActAgent:
    def __init__(self, model, tools, system:str=""):
        self.model = model
        self.tools = tools
        self.system = system
        
        self.messages = [] 
        if self.system:
            self.messages.append(("system", self.system))

        

    def _execute(self, message:str="", verbose=True):
        if message:
            self.messages.append(("user",message))
        result = self.model.invoke(ChatPromptTemplate(self.messages).invoke({}))
        if verbose:
            print(message)
            print(result.content)
        self.messages.append(("ai",result.content))
        return result.content

    
    def loop(self, Query, verbose=True):
        response = self._execute(Query, verbose=verbose)
        print(response)
        for i in range(20):
            if "PAUSE" in response and "Action" in response:
                match = re.findall(r'Action: ([a-z0-9_]+): "(.*?)"', response)
                if match:
                    tool, tool_input = match[0][0], match[0][1]
                else:
                    tool, tool_input = "None" , ""
                
                if tool == 'web_search':
                    tool_res = eval(f"{tool}('{tool_input}')")
                    response = f"Observation: {tool_res}"
                else:
                    response = f"Observation: Tool not found in accessed tools but I answered from my own knowledge with this answer: {tool_input}"
                print(response)
            elif "answer" in response.lower():
                response = "Answer: "+ re.findall(r"Answer: (.+)", response, re.IGNORECASE)[0]
                print(response)
                return response

            response = self._execute(response,verbose=verbose)
        return response
    
    def __call__(self, Query, verbose=True):
        self.loop(Query, verbose=verbose)