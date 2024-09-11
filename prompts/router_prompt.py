from langchain_core.prompts import PromptTemplate

router_prompt = PromptTemplate(
    template="""You are an expert at routing a user question to either a vectorstore or web search. \n
        Use the vectorstore for questions related to the following content: '{context}' \n
        You do not need to be stringent with the keywords in the question related to these topics. \n
        Otherwise, use web-search.

        Return the a JSON with only one keys ['datasource'] and no premable or explanation. \n
        'datasource': either ['vectorstore' or 'web_search']. \n

        Note: before your choose which datasource to route, keep this in mind that:
        if the question is related to retrieving previous knowledge from conversation history (like: could you explain more?, here is what you need...answer now, what was the previous question about?, could you answer the previous question? ...etc) if such this or similar was asked, check your full history to determine which datasource this question is relevant.
        
        here is your chat_history: {history}

        Question to route: {question}
        
        """,


    input_variables=["question","content"],
)
