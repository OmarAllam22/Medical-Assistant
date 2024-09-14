import sys
if "../" not in sys.path:
    sys.path.append("../")

from utils.initialize_gemini import initialize_gemini
from prompts.ReAct_system_template import ReAct_system_template
from langchain_core.prompts import ChatPromptTemplate

from helper_chains.vectorstore import vectorstore_chain
from helper_chains.web_search import web_search_chain
from helper_chains.llm_knowledge import llm_knowledge_chain

import re
from termcolor import colored
class ReActLoop:
    general_verbosity = True
    def __init__(self, verbose):
        ReActLoop.general_verbosity = verbose
        self.system = ReAct_system_template
        self.ReAct_model = initialize_gemini(api_config_path="config/api1.yaml") 
        self.messages = []        
        if self.system:
            self.messages.append(("system", self.system))

    def _execute(self, message:str="", verbose=general_verbosity):
        if message:
            self.messages.append(("user",message))
        result = self.ReAct_model.invoke(ChatPromptTemplate(self.messages).invoke({}))
        if verbose:
            print(colored(message,"cyan"))
        self.messages.append(("ai",result.content))
        return result.content

    
    def loop(self, Query, verbose=general_verbosity):
        web_search =  web_search_chain()
        vectorstore = vectorstore_chain()
        llm_knowledge = llm_knowledge_chain()
        response = self._execute(Query, verbose=verbose)
        print(colored(response,"cyan")) if verbose else None
        tool = 'None'
        for i in range(20):
            if "PAUSE" in response and "answer:" not in response.lower():
                match = re.findall(r'Action: ([a-z0-9_]+): "(.*?)"', response)
                if match:
                    tool, tool_input = match[0][0], match[0][1]
            
                if tool != 'None':
                    tool_res = eval(f"{tool}(\"{tool_input}\")")
                    response = f"Observation: {tool_res}"
                else:
                    response = "Observation: I cannot answer using my available actions. so I will inform the user to explain more its query as I cannot answer it"
            
            elif "answer:" in response.lower():
                try:
                    response = f"From {tool} --> "+ re.findall("Answer: .*", response, re.DOTALL)[0] if tool != 'None' else re.findall("Answer: .*", response, re.DOTALL)[0]
                except Exception as e:
                    try:
                        response = f"From {tool} --> "+ re.findall(r"Thought: (.+)", response, re.IGNORECASE)[0] if tool != 'None' else re.findall(r"Thought: (.+)", response, re.IGNORECASE)[0]
                    except Exception as e:
                        print("---- while giving asnwer, we recieved this ---", e)
                        response = "Answer: Please ask me again as There is an Error displaying the results."
                return response
            print(colored(response,"cyan")) if verbose else None
            response = self._execute(response,verbose=verbose)
        return response
    
    def __call__(self, Query, verbose=general_verbosity):
        return self.loop(Query, verbose=verbose)