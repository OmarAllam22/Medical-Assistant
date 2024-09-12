from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from termcolor import colored
from tools.search_web import WebSearch
from prompts.retriever_prompt import retriever_prompt
from prompts.web_search_prompt import web_search_prompt 
from prompts.summarization_prompt import summarization_prompt
from prompts.router_prompt import router_prompt
from prompts.ReAct_system_template import ReAct_system_temp
from prompts.llm_knowledge_prompt import llm_knowledge_prompt
from utils.initialize_gemini import initialize_gemini
from utils.prepare_retriever import prepare_retriever
from langchain_core.prompts import ChatPromptTemplate
import re


class ReActAgent:
    def __init__(self, model, system:str=""):
        self.model = model
        self.system = system
        
        self.messages = []        
        if self.system:
            self.messages.append(("system", self.system))

    def web_search(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        self.rag_model = initialize_gemini(api_config_path="config/api1.yaml") # model used to rewrite the user query into multiple queries to get versatile retrieved context
        self.web_search_prompt = web_search_prompt
        object = WebSearch()
        chain = (
                {"context": object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.web_search_prompt
                | self.rag_model
                | StrOutputParser()
        )
        return chain.invoke(query)

    def _execute(self, message:str="", verbose=True):
        if message:
            self.messages.append(("user",message))
        result = self.model.invoke(ChatPromptTemplate(self.messages).invoke({}))
        if verbose:
            print(message)
        self.messages.append(("ai",result.content))
        return result.content

    
    def loop(self, Query, verbose=True):
        response = self._execute(Query, verbose=verbose)
        print(response)
        for i in range(20):
            print("@@@@@@@@@@@response$$$$$$", response,"@@@@@@@@@@@response$$$$$$" )
            if "PAUSE" in response and "answer:" not in response.lower():
                match = re.findall(r'Action: ([a-z0-9_]+): "(.*?)"', response)
                if match:
                    tool, tool_input = match[0][0], match[0][1]
                else:
                    tool = "None" 
                
                if tool == 'web_search':
                    tool = 'self.web_search'
                    tool_res = eval(f"{tool}('{tool_input}')")
                    response = f"Observation: {tool_res}"
                elif tool == 'None':
                    response = f"Observation: I cannot answer using my available tools. so will answer this question from my own knowledge"
            
            else:
                try:
                    response = "Answer: "+ re.findall(r"Answer: (.+)", response, re.IGNORECASE)[0]
                except:
                    try:
                        response = "Answer: "+ re.findall(r"Thought: (.+)", response, re.IGNORECASE)[0]
                    except:
                        response = "Answer: Please ask me again as There is an Error displaying the results."
                return response
            
            response = self._execute(response,verbose=verbose)
        return response
    
    def __call__(self, Query, verbose=True):
        return self.loop(Query, verbose=verbose)

############################################################################################################


class Agent:
    def __init__(self):
        self.react_model = initialize_gemini(api_config_path="config/api4.yaml")
        self.rag_model = initialize_gemini(api_config_path="config/api1.yaml") # model used to rewrite the user query into multiple queries to get versatile retrieved context     
        self.summarization_model = initialize_gemini(api_config_path="config/api2.yaml")
        self.retriever = prepare_retriever()
        self.router_prompt = router_prompt
        self.retriever_prompt = retriever_prompt
        self.summarization_prompt = summarization_prompt
        self.web_search_prompt = web_search_prompt
        self.llm_knowledge_prompt = llm_knowledge_prompt
        self.history = ""
        # initialize the history file to empty string.
        with open("summary.txt", 'w') as f:
            f.write("")

    def _format_docs(self, docs):
        """
        helper function used in the chain to get the text from the retrieved docs 
        """
        return "\n\n".join(doc[0].page_content if len(doc)==2 else doc.page_content for doc in docs)

    
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

    def _execute_router_chain(self,query)->str:
        """
        returns the datasource to which will be routed a choice from ['vectorstore','web_search','llm_knowledge'].
        """
        try:
            with open('book_summaries_for_Agent.txt','r') as f:
                content = f.read()
        except FileNotFoundError:
            print(colored("Error: 'book_summaries_for_Agent.txt' not found.", 'red'))
            return None  # Handle the case where the file is missing

        chain = (
            {"question": RunnablePassthrough(), "context": RunnableLambda(lambda x: content),"history":  RunnableLambda(lambda x: self.history)} 
            | router_prompt 
            | self.rag_model 
            | JsonOutputParser()
        )
        return chain.invoke(query)['datasource']
    
    def _execute_ReAct(self, query):
        object = ReActAgent(self.react_model, system=ReAct_system_temp)
        return object(query)
    
    def _execute_llm_chain(self, query):
        chain = (
                {"question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.llm_knowledge_prompt
                | self.rag_model
                | StrOutputParser()
        )
        return chain.invoke(query)

    def invoke(self):

        while True:
            query = input(colored("Input your query: ",'green'))
            if "exit" == query.lower().strip():
                break
            try:
                datasource = self._execute_router_chain(query)
                
                print(colored(f"Answer from '{datasource}': ","green"), end="")
                if datasource == 'vectorstore':
                    print(colored("Optimizing the answer from our databases...🛢️📂","light_green"), flush=True)
                    response = self._execute_rag_chain(query)
                    print(colored(response,"magenta"), flush=True)
                    with open("summary.txt", 'a') as f:
                        f.write("user query: " + query + "\n" + "llm response: "+ response)
                    with open("summary.txt", 'r') as f:  
                        self.history = f.read()
                    self.history = self._excute_summarization_chain(self.history)

                elif datasource == 'web_search':      
                    print(colored("Preparing the best answer for you...🌐🤖","light_green"), flush=True) 
                    response = self._execute_ReAct(query)
                    print(colored(response,"magenta"), flush=True)
                    with open("summary.txt", 'a') as f:
                        f.write("user query: " + query + "\n" + "llm response: "+ response)
                    with open("summary.txt", 'r') as f:  
                        self.history = f.read()
                    self.history = self._excute_summarization_chain(self.history)
                elif datasource == 'llm_knowledge':
                    response = self._execute_llm_chain(query)
                    print(colored(response,"magenta"), flush=True)
                    with open("summary.txt", 'a') as f:
                        f.write("user query: " + query + "\n" + "llm response: "+ response)
                    with open("summary.txt", 'r') as f:  
                        self.history = f.read()
                    self.history = self._excute_summarization_chain(self.history)

            except Exception as e: 
                print(colored(f"Error arises due to the following exception {e}", 'red'))

#####################################################################################

