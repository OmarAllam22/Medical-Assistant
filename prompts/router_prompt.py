from langchain_core.prompts import PromptTemplate

router_prompt = PromptTemplate(
    template="""You are an expert at routing a user question to a vectorstore or web search. \n
        Use the vectorstore for questions related to the following content: '{content}' \n

        You do not need to be stringent with the keywords in the question related to these topics. \n
        Otherwise, use web-search. Give a binary choice 'web_search' or 'vectorstore' based on the question. \n
        Return the a JSON with a single key 'datasource' and no premable or explanation. \n
        Question to route: {question}""",
    input_variables=["question"],
)
