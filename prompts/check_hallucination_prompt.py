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
            
            Note: It's mandatory to note that, some answeres may contains answeres that is not similar in content but the general workflow is similar, as an example:
                question: how can I best study differntial diagnosis?
                original loop:
                    Thought: I need to find good resources to study differential diagnosis. I cannot answer from my own knowledge, I will search web
                    Action: web_search: resources to study differential diagnosis
                    PAUSE
                    you will be called again with this
                    Observation: there are many books like: Symptom to Diagnosis by Scott D. C. Stern, Differential Diagnosis in Internal Medicine by Walter Siegenthaler
                    Answer: there are some books like: Symptom to Diagnosis by Scott D. C. Stern, Differential Diagnosis in Internal Medicine by Walter Siegenthaler
                when you formulate your own loop you may follow the same logic but content may be different. by this hallucination doesn't exist because the same logic in the two loops is similar.


            Give a binary score 'yes' or 'no' score to indicate whether there is hallucination or not. \n
            Provide the binary score as a JSON with a single key 'is_hallucinating' and no preamble or explanation.""",
            input_variables=["query", "answer", "messages", "ReAct_system_template"],
        )