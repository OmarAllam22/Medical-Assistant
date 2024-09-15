from helper_chains.check_hallucination import hallucination_chain
from helper_chains.grad_answer import grad_answer_chain
from helper_chains.ReAct_loop import ReActLoop

from termcolor import colored

import warnings
warnings.filterwarnings("ignore", message="The function `loads` is in beta")

class ReActAgent:
    """
    ReActAgent class encapsulates the ReAct loop, hallucination checking, and answer grading functionalities.

    Args:
        verbose (bool, optional): Whether to print verbose output. Defaults to True.
        grad_answer (bool, optional): Whether to grade and improve the final answer. Defaults to True.
    """
    general_verbosity = True
    general_grading_option = True

    def __init__(self, verbose=True, grad_answer=general_grading_option):
        ReActAgent.general_verbosity = verbose
        ReActAgent.general_grading_option = grad_answer
        self.ReAct_loop_object = ReActLoop(verbose=ReActAgent.general_verbosity)
        self.check_hallucination_object = hallucination_chain()
        self.grad_answer_object = grad_answer_chain()
        self.messages = []
        self.history = ""
        with open("summary.txt", 'w') as f:
            f.write("")
    
    def __call__(self, Query, verbose=general_verbosity):
        """
        Processes a query using the ReAct loop.

        Args:
            Query (str): The input query.
            verbose (bool, optional): Whether to print verbose output. Defaults to `general_verbosity` class variable.

        Returns:
            str: The generated response.
        """
        result = self.ReAct_loop_object(Query, verbose=verbose)
        self.messages = self.ReAct_loop_object.messages
        return result
    
    def correct_hallucination(self, query, answer, ReAct_messages):
        """
        Checks for hallucinations in the generated answer and corrects them if necessary.

        Args:
            query (str): The original query.
            answer (str): The generated answer.
            ReAct_messages (list): The messages formed during the ReAct loop.

        Returns:
            str: The corrected answer.
        """
        is_hallucinating =  self.check_hallucination_object(query, answer, ReAct_messages)
        print(colored("Is there hallucination? ",'cyan'), colored(is_hallucinating,"cyan")) if ReActAgent.general_verbosity else None
        while True:
            if is_hallucinating.lower() == 'yes':
                print(colored("we are correcting hallucination...","cyan"),flush=True) if ReActAgent.general_verbosity else None
                answer = self.__call__(query+". Please be aware of hallucinating")
                ReAct_messages = self.messages
                is_hallucinating =  self.check_hallucination_object(query, answer, ReAct_messages)
            else:
                return answer

    def correct_final_answer(self, query, answer, ReAct_messages):
        """
        Grades the final answer and improves it if necessary.

        Args:
            query (str): The original query.
            answer (str): The generated answer.
            ReAct_messages (list): The messages formed during the ReAct loop.

        Returns:
            str: The improved answer.
        """
        is_good_answer = self.grad_answer_object(query=query, answer=answer)
        while True:
            if is_good_answer.lower() == 'no':
                print(colored("we are optimizing your answer...","red"),flush=True)
                answer = self.__call__("rewrite the following query to give a better answer. "+query)
                answer = self.correct_hallucination(query, answer, ReAct_messages)
                is_good_answer =  self.grad_answer_object(query=query, answer=answer)
            else:
                return answer

    def start(self, grad_answer=general_grading_option):
        """
        Starts the interactive query-response loop.

        Args:
            grad_answer (bool, optional): Whether to grade and improve the final answer. Defaults to general_grading_option.
        """
        while True:
            query = input(colored("Input your query: ",'green'))
            if query == 'exit':
                break
            else:
                answer = self.__call__(query)
                ReAct_messages = self.messages
                answer = self.correct_hallucination(query, answer, ReAct_messages)
                if grad_answer:
                    answer = self.correct_final_answer(query, answer, ReAct_messages)
                print(colored(answer,"magenta"),flush=True)
            