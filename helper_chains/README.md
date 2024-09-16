### To break this directory down, there are three main chains:

1. **`check_hallucination.py`**: used in `main_agent.py` if the final answer is hallcination or not. 

2. **`ReAct_loop.py`**: used in `main_agent.py` to perform the ReAct Loop used at routing the intial query to the available tools exist in:
    - `vectorstore.py`
    - `web_search.py`
    - `llm_knowledge.py`

3. **`grad_answer.py`**: used in `main_agent.py` to check if the final answer is good or bad.

---------

**`summarization_chain.py`**: is used for memory purposes [summarize the content in `summmary.txt` before using it as chat_history]
