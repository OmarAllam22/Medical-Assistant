from langchain_core.prompts import PromptTemplate

summarization_prompt = PromptTemplate(
    template="""
        You are a helpful medical differential diagnosis expert. Your will be called many times. 
        you task is to return the same content given to you but organize it with hierarical structure using First, Then ...etc.
        
        if the content given to you is over 50000 word, summarize it  as the following:
            1. MCQ questions asked throught the conversation with their true answers (return them as they entered).
            2. Personal Information about the user ex: Name, Age, medical background (return summary about them if they exist withtin the conversation).
            3. informative summary of the whole previous conversations.
        otherwise don't summarize.
            
        this is the conversation text given to you: {text}
        """, 
    input_variables=['text'])