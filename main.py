from utils import initialize_gemini, prepare_retriever
from prompts import retriever_prompt, summarization_prompt, web_search_prompt
from chains import RagChain
import argparse

print("Welcome to our medical assistant.😊") 

rag_model = initialize_gemini(api_config_path="config/api1.yaml") # model used to rewrite the user query into multiple queries to get versatile retrieved context
summarization_model = initialize_gemini(api_config_path="config/api2.yaml")
retriever = prepare_retriever(is_multi_query=True, api_config_path="config/api3.yaml")

retriever_prompt = retriever_prompt
summarization_prompt = summarization_prompt

chain = RagChain(rag_model, summarization_model, retriever, retriever_prompt, summarization_prompt, web_search_prompt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the either rag or search model')
    parser.add_argument('mode', choices=['rag','search'], help='The mode to run the model in')
    args = parser.parse_args()

    chain.invoke(chain_type=args.mode)









