import warnings, argparse
warnings.filterwarnings("ignore", message="The function `loads` is in beta")
from termcolor import colored
from main_agent import ReActAgent

print(colored("Welcome to our medical assistant.😊",'green')) # Introductory message to the user

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A medical assistant using ReActLoop.")
    parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, required=True) # run the script as (python main.py --verbose  / python main.py --no-verbose)
    args = parser.parse_args()
    
    medical_assistant = ReActAgent(verbose=args.verbose)
    medical_assistant.start()








