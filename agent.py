from helper_chains.check_relevance import relevance_chain
from helper_chains.check_hallucination import hallucination_chain
from helper_chains.grad_answer import grad_answer_chain

from utils.initialize_gemini import initialize_gemini
from utils.prepare_retriever import prepare_retriever


from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from termcolor import colored
from tools.search_web import WebSearch

from prompts.retriever_prompt import retriever_prompt
from prompts.web_search_prompt import web_search_prompt
from prompts.llm_knowledge_prompt import llm_knowledge_prompt
from prompts.ReAct_system_template import ReAct_system_template
from prompts.grade_answer_prompt import grade_answer_prompt
from prompts.check_docs_relevance_prompt import check_docs_relevance_prompt
from prompts.check_hallucination_prompt import check_hallucination_prompt

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

import re

import warnings
warnings.filterwarnings("ignore", message="The function `loads` is in beta")


class ReActAgent:
    general_verbosity = True

    def __init__(self, verbose=True):
        ReActAgent.general_verbosity = verbose
        self.system = ReAct_system_template
        
        self.ReAct_model = initialize_gemini(api_config_path="config/api1.yaml") 
        self.web_model = initialize_gemini(api_config_path="config/api2.yaml") 
        self.rag_model = initialize_gemini(api_config_path="config/api3.yaml") 
        self.llm_knowledge_model = initialize_gemini(api_config_path="config/api4.yaml")
        self.retriever = prepare_retriever()

        self.check_hallucination_object = hallucination_chain()
        self.check_relevance_object = relevance_chain()
        self.grad_answer_object = grad_answer_chain()

        self.messages = []        
        if self.system:
            self.messages.append(("system", self.system))

        self.history = ""
        with open("summary.txt", 'w') as f:
            f.write("")

    def web_search(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        search_object = WebSearch()
        chain = (
                {"context": search_object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | web_search_prompt
                | self.web_model
                | StrOutputParser()
        )
        return chain.invoke(query)
    

    def vectorstore(self, query, verbose=general_verbosity):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        is_relevant, reason, docs_txt = self.check_relevance_object(prompt=check_docs_relevance_prompt,
                                                                model=self.rag_model, 
                                                                retriever=self.retriever, 
                                                                query=query)
        while(True):
            if verbose: 
                print(colored("[Logged Message] Relevance of docs to the query: " + is_relevant,'light_grey'))   
            if is_relevant:
                break
            else:
                query = self.rag_model.invoke(f"rewrite this query so that it is best suitable for retrieval purposes: {query} because this query wasn't relevant due to this reason:{reason}")
                is_relevant, reason, docs_txt = self.check_relevance_object(prompt=check_docs_relevance_prompt,
                                                                model=self.rag_model, 
                                                                retriever=self.retriever, 
                                                                query=query)   
        chain = (
                {"context": RunnableLambda(lambda x: docs_txt) , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | retriever_prompt
                | self.rag_model
                | StrOutputParser()
        )
        return chain.invoke(query)
    


    def llm_knowledge(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        chain = (
                {"question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | llm_knowledge_prompt
                | self.llm_knowledge_model
                | StrOutputParser()
        )
        return chain.invoke(query)

    def _execute(self, message:str="", verbose=True):
        if message:
            self.messages.append(("user",message))
        result = self.ReAct_model.invoke(ChatPromptTemplate(self.messages).invoke({}))
        if verbose:
            print(message)
        self.messages.append(("ai",result.content))
        return result.content

    
    def loop(self, Query, verbose=True):
        response = self._execute(Query, verbose=verbose)
        print(response)
        tool = 'None'
        for i in range(20):
            if "PAUSE" in response and "answer:" not in response.lower():
                match = re.findall(r'Action: ([a-z0-9_]+): "(.*?)"', response)
                if match:
                    tool, tool_input = match[0][0], match[0][1]
            
                if tool != 'None':
                    tool_res = eval(f"self.{tool}(\"{tool_input}\")")
                    response = f"Observation: {tool_res}"
                else:
                    response = "Observation: I cannot answer using my available actions. so I will inform the user to explain more its query as I cannot answer it"
            
            elif "answer:" in response.lower():
                try:
                    response = f"From {tool} --> "+ re.findall("Answer: .*", response, re.DOTALL)[0] if tool != 'None' else re.findall("Answer: .*", response, re.DOTALL)[0]
                except Exception as e:
                    print("---",e)
                    try:
                        response = f"From {tool} --> "+ re.findall(r"Thought: (.+)", response, re.IGNORECASE)[0] if tool != 'None' else re.findall(r"Thought: (.+)", response, re.IGNORECASE)[0]
                    except Exception as e:
                        print("---- while giving asnwer, we recieved this ---", e)
                        response = "Answer: Please ask me again as There is an Error displaying the results."
                return response
            
            response = self._execute(response,verbose=verbose)
        return response
    
    def __call__(self, Query, verbose=True):
        return self.loop(Query, verbose=verbose)
    
    

    def _check_hallucination(self, query, answer, ReAct_messages):
        return self.check_hallucination_object(model=self.llm_knowledge_model,
                                query=query,
                                answer=answer, 
                                check_hallucination_prompt=check_hallucination_prompt, 
                                ReAct_messages= ReAct_messages, 
                                ReAct_prompt=ReAct_system_template)

        
    

    def _grad_answer(self, query, answer):

        return self.grad_answer_object(prompt= grade_answer_prompt,
                           model= self.rag_model,
                           query=query,
                           answer=answer)
        


agent = ReActAgent()
while True:
    query = input("Input your query:")
    if query == 'exit':
        break
    else:
        answer = agent(query)
        ReAct_messages = agent.messages
        is_hallucinating =  agent._check_hallucination(query, answer, ReAct_messages)
        while True:
            print("Is there hallucination? ", is_hallucinating)
            if is_hallucinating.lower() == 'yes':
                print(colored("we are correcting hallucination...","red"),flush=True)
                answer = agent(query+". Please be aware of hallucinating")
                ReAct_messages = agent.messages
                is_hallucinating =  agent._check_hallucination(query, answer, ReAct_messages)
            else:
                break
        is_good_answer = agent._grad_answer(query, answer)
        while True:
            if is_good_answer.lower() == 'no':
                print(colored("we are optimizing your answer...","red"),flush=True)
                answer = agent("rewrite the following query to give a better answer. "+query)
                is_good_answer =  agent._grad_answer(query, answer)
            else:
                break        
        print(colored(answer,"cyan"),flush=True)
    