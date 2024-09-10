from langchain_core.prompts import PromptTemplate

summarization_prompt = PromptTemplate(
    template="""
        You are a helpful medical differential diagnosis expert. Your will be called many times. 
        you task is to summarize the conversation text given to you and keep the important information.
        your summary should be structured in the following three components:
        1. MCQ questions asked throught the conversation with their true answers (return them as they entered).
        2. Personal Information about the user ex: Name, Age, medical background (return summary about them if they exist withtin the conversation).
        3. informative summary of the whole previous conversations.

        this is the conversation text given to you: {text}
        """, 
    input_variables=['text'])