from helper_chains.check_hallucination import hallucination_chain
from helper_chains.grad_answer import grad_answer_chain
from helper_chains.vectorstore import vectorstore_chain
from helper_chains.llm_knowledge import llm_knowledge_chain
from helper_chains.web_search import web_search_chain
from helper_chains.ReAct_loop import ReActLoop

from termcolor import colored

import warnings
warnings.filterwarnings("ignore", message="The function `loads` is in beta")

class ReActAgent:
    general_verbosity = True
    
    def __init__(self, verbose=True):
        ReActAgent.general_verbosity = verbose
        self.ReAct_loop_object = ReActLoop(verbose=ReActAgent.general_verbosity)
        self.check_hallucination_object = hallucination_chain()
        self.grad_answer_object = grad_answer_chain()
        self.vectorstore_object = vectorstore_chain()
        self.web_search_object = web_search_chain()
        self.llm_knowledge_object = llm_knowledge_chain()
        self.messages = []
        self.history = ""
        with open("summary.txt", 'w') as f:
            f.write("")

    def web_search(self, query):
        return self.web_search_object(query)
        
    def vectorstore(self, query, verbose=general_verbosity):
        return self.vectorstore_object(query,verbose)
        
    def llm_knowledge(self, query):
        return self.llm_knowledge_object(query)
    
    def _check_hallucination(self, query, answer, ReAct_messages):
        return self.check_hallucination_object(query=query, answer=answer, ReAct_messages= ReAct_messages)

    def _grad_answer(self, query, answer):

        return self.grad_answer_object(query=query, answer=answer)

    def __call__(self, Query, verbose=general_verbosity):
        result = self.ReAct_loop_object(Query, verbose=verbose)
        self.messages = self.ReAct_loop_object.messages
        return result
    
    def invoke(self):
        agent = ReActAgent()
        while True:
            query = input(colored("Input your query: ",'green'))
            if query == 'exit':
                break
            else:
                answer = agent(query)
                ReAct_messages = agent.messages
                is_hallucinating =  agent._check_hallucination(query, answer, ReAct_messages)
                while True:
                    print(colored("Is there hallucination? ",'cyan'), is_hallucinating)
                    if is_hallucinating.lower() == 'yes':
                        print(colored("we are correcting hallucination...","cyan"),flush=True)
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
                print(colored(answer,"magenta"),flush=True)
            