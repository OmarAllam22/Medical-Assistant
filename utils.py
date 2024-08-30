import os, yaml
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever


def initialize_gemini(api_config_path:str, model_version:str = "gemini-1.5-flash", temperature:float=0.6):
    """
    Purpose:
    Initializes a Gemini language model instance using the provided API key and configuration.
    
    Parameters:
    api_config_path: The path to the YAML file containing the API key.
    model_version: The desired Gemini model version (default: "gemini-1.5-flash").
    temperature: The temperature hyperparameter controlling the randomness of the model's output (default: 0.6).
    
    Returns:
    A ChatGoogleGenerativeAI object representing the initialized Gemini model.
    """

    with open(api_config_path, 'r') as f:
        data = yaml.safe_load(f)
    os.environ["GOOGLE_API_KEY"] = data.get("GOOGLE_API_KEY",None) 
    model = ChatGoogleGenerativeAI(model= model_version, temperature=temperature)
    return model

def prepare_retriever(retrieved_docs_per_query=5, is_multi_query=True, api_config_path="config/api1.yaml"):
    """
    Purpose:
    Creates a retriever object for retrieving relevant documents from a vector store based on user queries.
    
    Parameters:
    retrieved_docs_per_query: The number of query-related documents to retrieve for each query.
    is_multi_query: Indicates whether the retriever should handle multiple queries in a single prompt.
    api_config_path: (used only in case of multi-query) the api for the model used in multi-query retrieving.
    Returns:
    A Retriever object (either a single-query or multi-query retriever).
    """
 
    loader = PyPDFDirectoryLoader("books")
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(pages)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": retrieved_docs_per_query})

    if is_multi_query:
        llm = initialize_gemini(api_config_path=api_config_path)
        retriever = MultiQueryRetriever.from_llm(retriever=retriever, llm=llm)

    return retriever