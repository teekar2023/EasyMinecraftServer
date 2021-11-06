import os
import sys
import webbrowser
import time
import requests
import pyautogui as kbm
from threading import Thread
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askinteger, askstring


def ngrok():
    os.chdir(f"{cwd}\\ngrok\\")
    os.system(f"ngrok authtoken {authtoken}")
    os.system("start cmd")
    time.sleep(1)
    kbm.typewrite(f"cd {cwd}\n")
    kbm.typewrite(f"cd ngrok\n")
    kbm.typewrite("ngrok tcp 25565\n")
    pass


cwd = os.getcwd()
print("EasyMinecraftServer Version: 1.1.0")
print(f"Current Working Directory: {cwd}")
root = Tk()
root.withdraw()
try:
    url = "http://github.com/teekar2023/EasyMinecraftServer/releases/latest/"
    r = requests.get(url, allow_redirects=True)
    redirected_url = r.url
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v1.1.0":
        showwarning(title="Update Available", message="An update is available. Please update to the latest version to "
                                                      "use this program. None of your data will be lost.")
        webbrowser.open(redirected_url)
        sys.exit(0)
    else:
        pass
except Exception as e:
    print(f"Error while checking for updates: {e}")
if not os.path.exists("C:\\Program Files\\Java\\jdk-17.0.1\\bin"):
    install_jdk_ask = askyesno(title="JDK Required", message="Java Development Kit 17 Is Required! Would You Like To "
                                                             "Install It Now?")
    if install_jdk_ask:
        os.chdir(f"{cwd}\\JDK\\")
        os.system("start jdk-17_windows-x64_bin.exe")
        pass
    else:
        showerror(title="JDK Required", message="Java Development Kit 17 Is Required! Please Install It And Restart "
                                                "The Program!")
        sys.exit(0)
    pass
else:
    pass
version_selection = askstring("Minecraft Server", "Enter the version you want to use! '1.8.9' or '1.12.2' or '1.16.5' "
                                                  "or '1.17.1'")
if version_selection == "1.8.9":
    version = "1.8.9"
    pass
elif version_selection == "1.12.2":
    version = "1.12.2"
    pass
elif version_selection == "1.16.5":
    version = "1.16.5"
    pass
elif version_selection == "1.17.1":
    version = "1.17.1"
    pass
else:
    showerror("Minecraft Server", "You have entered an invalid version!")
    sys.exit(0)
port_forward_prompt = askyesno(title="Port Forwarded?", message="Is port 25565 port forwarded on your network? Press "
                                                                "'NO' if you are not sure!")
if port_forward_prompt:
    pass
else:
    if not os.path.exists(f"{cwd}\\Data\\"):
        os.mkdir(f"{cwd}\\Data\\")
        pass
    else:
        pass
    if not os.path.exists(f"{cwd}\\Data\\authtoken.txt"):
        open(f"{cwd}\\Data\\authtoken.txt", "w+")
        webbrowser.open("https://dashboard.ngrok.com/get-started/setup")
        showinfo(title="NGROK", message="Makeshift port-forwarding requires a ngrok account. Please navigate to "
                                        "https://dashboard.ngrok.com/get-started/setup after making an account and "
                                        "get your authtoken!")
        authtoken = askstring(title="Ngrok Authtoken", prompt="Enter your ngrok authtoken")
        open(f"{cwd}\\Data\\authtoken.txt", "w").write(str(authtoken))
        pass
    else:
        authtoken = str(open(f"{cwd}\\Data\\authtoken.txt", "r").read())
        pass
    ngrok_process = Thread(target=ngrok)
    ngrok_process.start()
    time.sleep(3)
    pass
ram_input = askinteger(title="Server RAM", prompt="How many mb of ram would you like in the server? Please enter an "
                                                  "integer number! Minimum Recommended: 2000")
os.chdir(f"{cwd}\\ServerFiles-{version}\\")
showinfo(title="Minecraft Server", message="Server will be created/started after closing this popup! Type "
                                           "'STOP' and press 'ENTER' in the console window to shutdown the "
                                           "server! Also, if you are using ngrok, your server's ip can be found in "
                                           "the ngrok window "
                                           "next to 'Forwarding' and should follow the format: '("
                                           "numbers).tcp.ngrok.io:(more_numbers)! If you are not using ngrok "
                                           "and are port forwarded, the server ip will be your computer's ip with the "
                                           "port '25565'! Have Fun!")
os.system(f"java -Xmx{ram_input}M -Xms{ram_input}M -jar server.jar nogui")
time.sleep(1)
sys.exit(0)
