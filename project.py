import customtkinter as ctk
import requests
import pyperclip
import webbrowser
import sys
import os

# ----------- App Appearance -----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Roblox ID Finder")
app.geometry("450x300")

# ---------- Load Icon for GUI ----------
if getattr(sys, 'frozen', False):
    # PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

icon_path = os.path.join(base_path, "mon_logo.ico")
try:
    app.iconbitmap(icon_path)
except Exception:
    pass  # fallback si l'icône n'est pas trouvée

# ---------- UI Elements ----------
label = ctk.CTkLabel(app, text="Enter Roblox username:", font=("Roboto", 14))
label.pack(pady=15)

entry = ctk.CTkEntry(app, width=300, placeholder_text="Username")
entry.pack(pady=5)

result_label = ctk.CTkLabel(app, text="", font=("Roboto", 16))
result_label.pack(pady=15)

# ---------- Functions ----------
def find_id():
    username = entry.get().strip()
    if not username:
        result_label.configure(text="⚠ Invalid username.")
        return

    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}

    try:
        response = requests.post(url, json=payload, timeout=5)
        data = response.json()
        if data["data"]:
            user_id = data["data"][0]["id"]
            result_label.configure(text=f"ID: {user_id}")
        else:
            result_label.configure(text="❌ User not found.")
    except Exception:
        result_label.configure(text="⚠ Network error. Check your connection.")

def copy_id():
    text = result_label.cget("text")
    if text.startswith("ID:"):
        pyperclip.copy(text.split("ID: ")[1])
        result_label.configure(text="✅ ID copied!")

# ---------- Buttons ----------
btn_find = ctk.CTkButton(app, text="Find ID", command=find_id, width=200)
btn_find.pack(pady=10)

btn_copy = ctk.CTkButton(app, text="Copy ID to clipboard", command=copy_id, width=200)
btn_copy.pack(pady=10)

app.mainloop()
