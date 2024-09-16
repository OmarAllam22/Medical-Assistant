import warnings
warnings.filterwarnings("ignore", message="The function `loads` is in beta")
from termcolor import colored
from main_agent import ReActAgent

print(colored("Welcome to our medical assistant.😊",'green')) # Introductory message to the user

medical_assistant = ReActAgent(verbose=True, grad_answer=False)

if __name__ == '__main__':
    medical_assistant.start()








