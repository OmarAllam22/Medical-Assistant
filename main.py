from agent import ReActAgent

import warnings

warnings.filterwarnings("ignore", message="The function `loads` is in beta")


print("Welcome to our medical assistant.😊") 

chain = ReActAgent(verbose=True)

if __name__ == '__main__':
    chain.invoke()








