from utils import initialize_gemini, prepare_retriever
from chains import Agent
import argparse

print("Welcome to our medical assistant.😊") 

chain = Agent()

if __name__ == '__main__':
    chain.invoke()








