from utils.initialize_gemini import initialize_gemini
from utils.prepare_retriever import prepare_retriever

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from termcolor import colored
from tools.search_web import WebSearch
from prompts.retriever_prompt import retriever_prompt
from prompts.web_search_prompt import web_search_prompt
from prompts.llm_knowledge_prompt import llm_knowledge_prompt
from prompts.ReAct_system_template import ReAct_system_template

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

import re

import warnings
warnings.filterwarnings("ignore", message="The function `loads` is in beta")


class ReActAgent:
    def __init__(self):
        self.system = ReAct_system_template
        self.ReAct_model = initialize_gemini(api_config_path="config/api1.yaml") 

        self.messages = []        
        if self.system:
            self.messages.append(("system", self.system))

        self.retriever = prepare_retriever()

        self.retriever_prompt = retriever_prompt
        self.web_search_prompt = web_search_prompt
        self.llm_knowledge_prompt = llm_knowledge_prompt

        self.history = ""
        # initialize the history file to empty string.
        with open("summary.txt", 'w') as f:
            f.write("")

    def web_search(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        self.web_model = initialize_gemini(api_config_path="config/api2.yaml") 
        self.web_search_prompt = web_search_prompt
        object = WebSearch()
        chain = (
                {"context": object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.web_search_prompt
                | self.web_model
                | StrOutputParser()
        )
        return chain.invoke(query)
    

    def _format_docs(self, docs):
        """
        helper function used in the chain to get the text from the retrieved docs 
        """
        return "\n\n".join(doc[0].page_content if len(doc)==2 else doc.page_content for doc in docs)
    
    def _check_relevance(self, model, retriever, query):
        """
        helper function used to check the relevance of the retrieved documents to the query asked. 
        """
        prompt = PromptTemplate(
            template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
            Here is the retrieved document: \n\n {documents} \n\n
            Here is the user question: {question} \n
            If the document contains keywords related to the user question, grade it as relevant. \n
            It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.and reason your answer \n
            Provide the answer as a JSON with a two  keys 'is_relevant' and 'reason' and no premable or explanation.""",
            input_variables=["question", "documents"],
        )
        retrieval_grader = prompt | model | JsonOutputParser()
        
        docs_txt = self._format_docs(retriever.invoke(query))        
        is_relevant = retrieval_grader.invoke({"question": query, "documents": docs_txt})['is_relevant']
        reason = retrieval_grader.invoke({"question": query, "documents": docs_txt})['reason']
        
        return is_relevant, reason, docs_txt

    def vectorstore(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        self.rag_model = initialize_gemini(api_config_path="config/api3.yaml") 

        is_relevant, reason, docs_txt = self._check_relevance(self.rag_model, self.retriever, query)

        while(True): 
            print("relevance: ",is_relevant)   
            if is_relevant:
                break
            else:
                query = self.rag_model.invoke(f"rewrite this query so that it is best suitable for retrieval purposes: {query} because this query wasn't relevant due to this reason:{reason}")
                is_relevant, reason, docs_txt = self._check_relevance(self.rag_model, self.retriever, query)   
        chain = (
                {"context": RunnableLambda(lambda x: docs_txt) , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.retriever_prompt
                | self.rag_model
                | StrOutputParser()
        )
        return chain.invoke(query)
    
    def llm_knowledge(self, query):
        with open("summary.txt", 'r') as f:  
            self.history = f.read()
        self.llm_knowledge_model = initialize_gemini(api_config_path="config/api4.yaml")
        
        chain = (
                {"question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | self.llm_knowledge_prompt
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
        ### Hallucination Grader
        llm = initialize_gemini(api_config_path="config/api4.yaml") 
        
        # Prompt
        prompt = PromptTemplate(
            template="""You are a grader assessing whether there is hallucination in the answer or not. You will have the "query" of the user and the "final answer". You check hallucination by:
            1. thouroughly and without any bias examine the (Thought, Action, Observation, Answer) loop that was formed to answer the query of the user. this will be given to you as "original_loop".
            2. Try to formulate your own loop of (Thought, Action, Observation, Answer) to answer the user "query" given to you.
            3. check if your formulated loop matches the original loop. (if they match, then there is no hallucination. otherwise, there is hallucination.) 
            
            Here are the "query" of the user: {query}
            Here is the final "answer" : {answer}
            Here is the previously formed "loop": {messages}
            Here is a helper examples to help you formulate your loop: {ReAct_system_template}
            ---------------------------------------------------------------------------
            Follow those instructions and output a json file contain one key: 'is_hallucinating' either yes or no:
            1. thouroughly and without any bias examine the (Thought, Action, Observation, Answer) loop that was formed to answer the query of the user. this will be given to you as "original_loop".
            2. Try to formulate your own loop of (Thought, Action, Observation, Answer) to answer the user "query" given to you.
            3. check if your formulated loop matches the original loop. (if they match, then there is no hallucination. otherwise, there is hallucination.) 
            
            Give a binary score 'yes' or 'no' score to indicate whether there is hallucination or not. \n
            Provide the binary score as a JSON with a single key 'is_hallucinating' and no preamble or explanation.""",
            input_variables=["query", "answer", "messages", "ReAct_system_template"],
        )

        hallucination_grader = prompt | llm | JsonOutputParser()
        return hallucination_grader.invoke({"query": query, "answer": answer, "messages":ReAct_messages, "ReAct_system_template": ReAct_system_template})['is_hallucinating']
    

    def _grad_answer(self, query, answer):
        ### Answer Grader

        llm = initialize_gemini(api_config_path="config/api4.yaml")

        # Prompt
        from langchain.prompts import PromptTemplate

        prompt = PromptTemplate(
            template="""You are a grader assessing whether an answer is useful to resolve a question.

            Here is the answer:
            \n ------- \n
            {answer} 
            \n ------- \n
            Here is the question: {query}

            Evaluate the answer based on these criteria:
            1. Completeness: Does the answer address all aspects of the question?
            2. Relevance: Is the information provided directly relevant to the query?
            3. Specificity: Does the answer provide specific details or examples?
            4. Clarity: Is the answer easy to understand and free from ambiguity?

            # Examples of good and bad answers:

            Good Answer Examples:
                1. Query: What are the symptoms of COVID-19?
                Answer: The primary symptoms of COVID-19 include fever, cough, and shortness of breath. Other common symptoms may include fatigue, muscle aches, headache, loss of taste or smell, sore throat, congestion or runny nose, nausea or vomiting, and diarrhea.   

                2. Query: Who was the first president of the United States?
                Answer: George Washington was the first president of the United States.

                3. Query: How do you calculate the area of a circle?
                Answer: The area of a circle is calculated using the formula: A = πr², where A is the area, π is a mathematical constant approximately equal to 3.14159, and r is the radius of the circle.

                4. Query: What is the capital of France?
                Answer: The capital of France is Paris.

                5. Query: Explain the concept of artificial intelligence.
                Answer: Artificial intelligence (AI) is a broad field of computer science that deals with creating intelligent agents, which are systems that can reason, learn, and act autonomously. AI applications include natural language processing, computer vision, and robotics.

            Bad Answer Examples
                1. Query: What are the symptoms of COVID-19?
                Answer: Wear a mask.

                2. Query: Who was the first president of the United States?
                Answer: Abraham Lincoln.

                3. Query: How do you calculate the area of a circle?
                Answer: The area of a circle is a mathematical equation.

                4. Query: What is the capital of France?
                Answer: Paris is a city in France.

                5. Query: Explain the concept of artificial intelligence.
                Answer: AI is a computer program.

                6. Query: How are you?
                Answer: I cannot answer.

            **Important Note:** Questions that primarily seek personal opinions, emotions, or subjective judgments (e.g., "How are you?", "How do you do?", "Which is older, you or Elon Musk?") are considered good answers regardless of their content.

            Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question.
            Provide the binary score as a JSON with a single key 'is_good_answer' and no preamble or explanation.""",
            input_variables=["answer", "query"],
        )

        answer_grader = prompt | llm | JsonOutputParser()
        return answer_grader.invoke({"query": query, "answer": answer})['is_good_answer']


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
    
