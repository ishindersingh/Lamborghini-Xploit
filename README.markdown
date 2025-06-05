# Lamborghini Xploit

## Overview
Lamborghini Xploit is a Python-based Tool designed to perform various remote operations on a Windows system, such as taking screenshots, capturing webcam photos, executing commands, and more. This project includes a setup script to configure the bot and convert it into an executable file.

**Warning**: This tool is for educational purposes only. Team IRA is not responsible for any misuse of this software. Ensure you have proper authorization before using it on any system.
https://github.com/ishindersingh/Lamborghini-Xploit/blob/main/lamborghini.JPG
## Features
- **Telegram Bot Commands**:
  - `/help`: Displays available commands.
  - `/ss`: Takes a screenshot and sends it.
  - `/wm`: Captures a webcam photo and sends it.
  - `/cmd <command>`: Executes a shell command and returns the output.
  - `/ds`: Disables security software (requires admin privileges).
  - `/sss`: Starts periodic screen sharing.
  - `/ssst`: Stops screen sharing.
  - `/creds`: Retrieves saved Chrome credentials.
  - `/ps`: Adds persistence to start the bot on system boot (Windows only).

- **Setup Script**:
  - Updates the Telegram bot token in `main.py`.
  - Installs required Python dependencies.
  - Converts `main.py` to a standalone executable (`igfxCUIService.exe`) using PyInstaller.

## Requirements
- **Operating System**: Windows (persistence and some features are Windows-specific).
- **Python**: Version 3.6 or higher.
- **Dependencies** (automatically installed by `setup.py`):
  - `requests`
  - `pyautogui`
  - `opencv-python`
  - `pycryptodome`
  - `pywin32`
  - `pyTelegramBotAPI`
  - `auto-py-to-exe`

## Installation
1. **Clone or Download the Repository**:
   ```bash
   git clone <repository-url>
   cd Lamborghini_Xploit
   ```

2. **Run the Setup Script**:
   ```bash
   python setup.py
   ```

3. **Follow the Setup Menu**:
   - **Option 1**: Enter your Telegram bot token URL to update `main.py`.
   - **Option 2**: Install required Python dependencies.
   - **Option 3**: Convert `main.py` to `igfxCUIService.exe`.
   - **Option 4**: Exit the setup.

4. **Run the Bot**:
   - If running as a Python script:
     ```bash
     python Lamborghini_Xploit/main.py
     ```
   - If converted to an executable:
     ```bash
     dist/igfxCUIService.exe
     ```

   **Note**: Some features (e.g., `/ds`, `/ps`) require administrative privileges.

## Usage
1. **Obtain a Telegram Bot Token**:
   - Create a bot using [BotFather](https://t.me/BotFather) on Telegram.
   - Copy the token and provide its URL during setup (Option 1).

2. **Interact with the Bot**:
   - Start the bot and send commands (e.g., `/help`, `/ss`) via Telegram.
   - Ensure the bot is running on the target system with appropriate permissions.

## File Structure
- `Lamborghini_Xploit/main.py`: The main bot script with Telegram command handlers.
- `setup.py`: Setup script to configure the token, install dependencies, and convert to an executable.
- `dist/igfxCUIService.exe`: Output executable (generated after conversion).

## Notes
- **Security**: The bot can disable security software and retrieve sensitive data (e.g., Chrome credentials). Use responsibly and only with explicit permission.
- **Persistence**: The `/ps` command adds the bot to Windows startup as a shortcut named "Intel Graphic Driver.lnk".
- **Screen Sharing**: The `/sss` command sends screenshots every second until stopped with `/ssst`.

## Disclaimer
This software is provided "as is" without warranty. The author and Team IRA are not liable for any damages or legal consequences resulting from its use. Always obtain proper authorization before deploying this tool.

## Author
- **Ishinder Singh**

## License
This project is for educational purposes and does not include a specific license. Use it responsibly and in compliance with applicable laws.
