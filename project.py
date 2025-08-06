import requests
import pyperclip
import keyboard
import os

def get_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {
        "usernames": [username],
        "excludeBannedUsers": False
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    
    if data["data"]:
        user_id = data["data"][0]["id"]
        print(f"\nUser ID: {user_id}")
        return str(user_id)
    else:
        print("❌ Username not found.")
        return None

def wait_for_key(user_id):
    print("\nPress ALT+C to copy User ID")
    print("Press ALT+X to restart the executable")
    print("Press SPACE to quit\n")

    while True:
        if keyboard.is_pressed('alt+c'):
            pyperclip.copy(user_id)
            print("✅ User ID copied to clipboard!")
            break
        elif keyboard.is_pressed('alt+x'):
            print("🔄 Restarting...\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            break
        elif keyboard.is_pressed('space'):
            print("👋 Quitting...")
            break

def main():
    username = input("Enter your Roblox username: ").strip()
    try:
        user_id = get_user_id(username)
        if user_id:
            wait_for_key(user_id)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
