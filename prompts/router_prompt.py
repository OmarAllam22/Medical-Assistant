from langchain_core.prompts import PromptTemplate

router_prompt = PromptTemplate(
    template="""You are an expert at routing a user question to either a vectorstore or web search. \n
        Use the 'vectorstore' for questions related to the following content: '{context}' \n
        You do not need to be stringent with the keywords in the question related to these topics. \n
        Use 'web-search' for questions needs to search the web.
        Use 'llm_knowledge' for easier question that don't need searching web (like: how are you?) or for questions that needs you to check your conversation history (like: could you explain more?, here is what you need...answer now, what was the previous question about?, could you answer the previous question?, please answer it ...etc)

        Return the a JSON with only one keys ['datasource'] and no premable or explanation. \n
        'datasource': one of ['vectorstore' or 'web_search' or 'llm_knowledge']. \n

        Question to route: {question}
        
        """,


    input_variables=["question","content"],
)
