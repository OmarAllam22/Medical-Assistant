from utils import initialize_gemini, prepare_retriever
from prompts import retriever_prompt, summarization_prompt
from chains import RagChain

print("Initializing the environment for you 😊...") # print this message untill initializin the retriever and models.

rag_model = initialize_gemini(api_config_path="config/api1.yaml")
summarization_model = initialize_gemini(api_config_path="config/api2.yaml")
retriever = prepare_retriever(is_multi_query=True, api_config_path="config/api3.yaml")
retriever_prompt = retriever_prompt
summarization_prompt = summarization_prompt

chain = RagChain(rag_model, summarization_model, retriever, retriever_prompt, summarization_prompt)

if __name__ == '__main__':
    chain.invoke()







