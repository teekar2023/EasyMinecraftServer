import os
import sys
import webbrowser
import time
import pyautogui as kbm
from threading import Thread
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askinteger, askstring


def ngrok():
    os.chdir(f"{cwd}\\ServerFiles\\")
    os.system(f"ngrok authtoken {authtoken}")
    os.system("start cmd")
    time.sleep(1)
    kbm.typewrite(f"cd {cwd}\n")
    kbm.typewrite("cd ServerFiles\n")
    kbm.typewrite("ngrok tcp 25565\n")
    pass


cwd = os.getcwd()
print(f"Current Working Directory: {cwd}")
print("Minecraft Version: 1.17.1")
root = Tk()
root.withdraw()
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
os.chdir(f"{cwd}\\ServerFiles\\")
showinfo(title="Minecraft Server 1.17.11", message="Server will be created/started after closing this popup! Type "
                                                   "'STOP' and press 'ENTER' in the console window to shutdown the "
                                                   "server! Also, your server's ip can be found in the ngrok window "
                                                   "next to 'Forwarding' and should follow the format '("
                                                   "numbers).tcp.ngrok.io:(more_numbers)! Have Fun!")
os.system(f"java -Xmx{ram_input}M -Xms{ram_input}M -jar server.jar nogui")
sys.exit(0)
