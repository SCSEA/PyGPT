import time
import os
import requests
import json
import random
from pyfiglet import Figlet
from termcolor import colored
from colorama import init
import platform
try:
    import openai
except ImportError:
    os.system("pip install openai")

init()

# Function to set up OpenAI API credentials
def setup_openai_api():
    # Set up the OpenAI API credentials
    os.system("clear")
    keys_directory = 'chatgpt_config'
    api_key_file = os.path.join(keys_directory, 'openai.api_key.txt')

    # Create the config directory if it doesn't exist
    if not os.path.exists(keys_directory):
        os.mkdir(keys_directory)

    # Check if the API key file exists
    if os.path.exists(api_key_file):
        # Read the API key from the file
        with open(api_key_file, 'r') as f:
            openai.api_key = f.readline().strip()
    else:
        print(colored("="*59, "green"))
        print("\033[1;36;40m 1. Go to >> \033[1;31mhttps://platform.openai.com \033[1;36;40m<< and click on the sign up button.")
        print(" If you already have an account, skip this option. I advise you to use a temporary email to register instead of your actual email.\n")

        print("\033[1;36;40m 2. After you login/signup, go to >> \033[1;31mhttps://platform.openai.com/account/api-keys \033[1;36;40m<<")
        print(" and click on the create new secret key button, copy your API key, tap on done then paste it below.\n")
        print(colored("="*59, "green"))

        openai.api_key = input("\n Provide your OpenAI API key: ")
        while len(openai.api_key) != 51:
            print(colored("\n Oops!!! Invalid API key. Please provide a valid OpenAI API key.", "red"))
            openai.api_key = input("\n Provide your OpenAI API key: ")

        with open(api_key_file, 'w') as f:
            f.write(openai.api_key)
        for char in "\nAPI key successfully saved.":
            print(colored(char, "green"), end='', flush=True)
            time.sleep(0.05)

    time.sleep(1.1)

# Function to display the main menu
def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    custom_fig = Figlet(font='graffiti')
    print(colored(custom_fig.renderText('   ChatGPT'), color='cyan'))
    print(colored("version 1.2", "yellow").center(110))
      
    Author = "Saif Ullah | Yousuf Shafii Muhammad"
    Github = "SCSEA"
    Telegram = "t.me/Programmerboy1"
    
    print(colored("="*59, "green"))
    print(colored("Author: ", "white") + colored(Author, "cyan"))
    print(colored("Github: ", "white") + colored(Github, "green"))
    print(colored("Telegram: ", "white") + colored(Telegram, "magenta"))
    print(colored("="*59, "green"))
    time.sleep(1)

    print(colored("\n  1. Text To Image", "yellow"))
    print(colored("  2. Chat With AI", "yellow"))
    print(colored("  3. Change Api Key", "yellow"))
    print(colored("  4. Exit", "red"))

    try:
        choice = int(input(colored("\n What would you like to do? ", "cyan")))
        if choice == 1:
            text_to_image()
        elif choice == 2:
            chat_with_ai()
        elif choice == 3:
            os.remove("chatgpt_config/openai.api_key.txt")
            setup_openai_api()
        elif choice == 4:
            exit_program()
        else:
            raise ValueError()
    except ValueError:
        print(colored("\n Please choose a valid option!", "red"))
        input("\n\n Press Enter to continue...")
        main_menu()

# Function to convert text to image
def text_to_image():
    os.system("clear")
    print(colored("="*59, "green"))
    print("""\033[36m
      _______        _   ___  _
     |__   __|      | | |__ \(_)
        | | _____  _| |_   ) |_ _ __ ___   __ _
        | |/ _ \ \/ / __| / /| | '_ ` _ \ / _` |
        | |  __/>  <| |_ / /_| | | | | | | (_| |
        |_|\___/_/\_\\__|____|_|_| |_| |_|\__, |
                                           __/ |
                                           |___/
                                      \033[0m""")
    print(colored("="*59, "green"))

    text = input("\n \033[1;34mEnter the text to generate an image from: \033[0m")
    num_images = int(input(colored("\n How many images do you want to generate? ", "cyan")))

    if num_images > 0:
        print("\n \033[1;33mMay take a while depending on your network speed so please wait..\n\033[0m")

    for i in range(num_images):
        filename = f"result_{i+1}_{random.randint(1000,9999)}.jpg"
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="1024x1024",
            response_format="url"
        )

        image_url = response['data'][0]['url']
        response = requests.get(image_url)
        with open(f"/sdcard/Text2Image/{filename}", 'wb') as f:
            f.write(response.content)

        print(colored("="*59, "green"))
        print(f"\033[1;32mImage {i+1} saved as \033[1;36m{filename}\033[1;32m in \033[1;35ma folder called Text2Image inside your storage\033[1;32m directory.\033[0m")
        print(colored("="*59, "green"))

# Function to chat with AI
def chat_with_ai():
    prompt = "Hello, how can I help you today ?"
    conversation_history = ""
    os.system("clear")
    print(colored("="*59, "green"))
    print(colored(Figlet(font='graffiti').renderText('      Ask_AI'), color='cyan'))
    print(colored("\n Start chatting with AI","green"))
    print(colored("\n You can type 'exit', 'quit', or 'bye'\n to end the conversation.","green"))
    print(colored("="*59, "green"))

    while True:
        try:
            user_input = input(colored("\n\n You >>  ", "cyan"))
            if user_input == "":
                raise ValueError()

            conversation_history += f"User: {user_input}\n"
            model_engine = "text-davinci-005"  # Updated to a supported model
            prompt_with_history = f"{prompt}\n{conversation_history}\nAI:"

            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_history,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
                timeout=10
            )

            ai_response = response.choices[0].text.strip()
            print(colored("\n AI: ", "green"), end="")
            for char in ai_response:
                typing_speed = 0.05
                time.sleep(typing_speed)
                print(char, end="", flush=True)

            conversation_history += f"AI: {ai_response}\n"

            if user_input.lower() in ["exit", "quit", "bye"]:
                break

        except ValueError:
            print(colored("\n Please enter a valid input!", "red"))

# Function to exit the program
def exit_program():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    print(colored(Figlet(font='graffiti').renderText('ChatGPT'), color='cyan'))
    for letter in list(colored("\n Thank you for using ChatGPT. Goodbye!\n\n", "yellow")):
        print(letter, end='', flush=True)
        time.sleep(0.05)
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

# Main function to run the program
def main():
    setup_openai_api()
    main_menu()

if __name__ == "__main__":
    main()

