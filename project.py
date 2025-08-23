import requests
import pyperclip
import keyboard
import os
import socket
import subprocess
import webbrowser
from colorama import Fore, init

init(autoreset=True)

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def check_wifi_capability():
    if os.name == "nt":
        try:
            output = subprocess.check_output("netsh wlan show drivers", shell=True, encoding="utf-8")
            return "Wireless LAN" in output or "Wi-Fi" in output
        except Exception:
            return False
    return False

def wifi_enable():
    try:
        os.system("netsh interface set interface name=\"Wi-Fi\" admin=enabled")
        print(f"{Fore.GREEN}📶 Wi-Fi adapter enabled.")
    except Exception as e:
        print(f"{Fore.RED}⚠️ Could not enable Wi-Fi: {e}")

def internet_check_screen():
    print(f"{Fore.RED}Your PC is not connected to Internet.")
    print("This software requires Internet to work, because it contacts Roblox's official API to get your UserID.\n")
    print(f"{Fore.YELLOW}Press ALT + F4 to close the window")

    if check_wifi_capability():
        print(f"{Fore.CYAN}Press ALT + K to enable Wi-Fi")

    while True:
        if keyboard.is_pressed("alt+f4"):
            print(f"{Fore.MAGENTA}👋 Closing...")
            exit()
        if keyboard.is_pressed("alt+k") and check_wifi_capability():
            wifi_enable()

def get_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data["data"]:
            user_id = data["data"][0]["id"]
            print(f"{Fore.GREEN}✅ {username}: {user_id}")
            return str(user_id)
        else:
            print(f"{Fore.RED}❌ Username not found: {username}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}⚠️ Network error: {e}")
        return None

def wait_for_key(user_id):
    print(f"\n{Fore.CYAN}Press ALT+C to copy User ID")
    print(f"{Fore.YELLOW}Press ALT+X to restart")
    print(f"{Fore.MAGENTA}Press ALT+D to join Discord server")
    print(f"{Fore.RED}Press SPACE to quit\n")

    while True:
        if keyboard.is_pressed('alt+c'):
            pyperclip.copy(user_id)
            print(f"{Fore.GREEN}📋 Copied to clipboard!")
            break
        elif keyboard.is_pressed('alt+x'):
            print(f"{Fore.CYAN}🔄 Restarting...\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            break
        elif keyboard.is_pressed('alt+d'):
            webbrowser.open("https://discord.gg/gxwEa4fGBf")
            print(f"{Fore.BLUE}🌐 Opening Discord server...")
        elif keyboard.is_pressed('space'):
            print(f"{Fore.MAGENTA}👋 Quitting...")
            break

def main():
    while True:
        username = input("Enter Roblox username: ").strip()
        if len(username) < 3 or len(username) > 20:
            continue
        user_id = get_user_id(username)
        if user_id:
            wait_for_key(user_id)
            break

if __name__ == "__main__":
    if not check_internet():
        internet_check_screen()
    else:
        print(f"{Fore.GREEN}✅ Internet OK, launching Roblox ID Finder...\n")
        main()
