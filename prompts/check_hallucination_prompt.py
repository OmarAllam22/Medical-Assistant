from langchain_core.prompts import PromptTemplate

check_hallucination_prompt = PromptTemplate(
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