import tkinter as tk
from tkinter import simpledialog, messagebox
from utils import check_strength, check_breach
import requests

def main():
    root = tk.Tk()
    #Hide main window
    root.withdraw()  

    while True:
        pwd = simpledialog.askstring(
            "Password Checker",
            "Type in you password:",
            #Hide password
            show="•"  
        )
        if pwd is None or pwd.strip() == "":
            break  

        #Use check_strength of pwd 
        strength = check_strength(pwd)

        #Use check_breach on pwd 
        try:
            count = check_breach(pwd)
            if count > 0:
                breach_msg = f"Found in leak {count} times"
            else:
                breach_msg = "Not found in known leaks"
        except requests.RequestException:
            breach_msg = "Not able to contact HIBP"

        messagebox.showinfo(
            "Result",
            f"Strength: {strength}\n{breach_msg}"
        )

    root.destroy()

if __name__ == "__main__":
    main()