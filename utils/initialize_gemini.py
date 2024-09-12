import os, yaml
from langchain_google_genai import ChatGoogleGenerativeAI

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
