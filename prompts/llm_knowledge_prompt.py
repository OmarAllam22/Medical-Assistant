from langchain_core.prompts import PromptTemplate

llm_knowledge_prompt = PromptTemplate(
    template="""you are an friendly knowledgable llm with access to chat conversation history.
        Your task is answer the user query.
        Before you answer you should check the answer in the conversation history given to you. 
        If you didn't find it in the conversation chat history given to you, answer it from your own knowledge.
        
        here is the conversation chat history given to you: {history}
        Question to route: {question}
        
        """,


    input_variables=["question","history"],
)
