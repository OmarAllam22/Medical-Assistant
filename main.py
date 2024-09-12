from chains import Agent

import warnings

warnings.filterwarnings("ignore", message="The function `loads` is in beta")


print("Welcome to our medical assistant.😊") 

chain = Agent()

if __name__ == '__main__':
    chain.invoke()








