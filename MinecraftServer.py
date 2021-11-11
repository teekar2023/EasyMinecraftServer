import os
import sys
import webbrowser
import time
import requests
import urllib
import ctypes
import pyautogui as kbm
from threading import Thread
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askinteger, askstring
from tkinter.filedialog import askdirectory
from shutil import copytree, rmtree


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    sys.exit(0)


def ngrok():
    os.chdir(f"{cwd}\\ngrok\\")
    os.system(f"ngrok authtoken {authtoken}")
    os.system("start cmd")
    time.sleep(1)
    kbm.typewrite(f"cd {cwd}\n")
    kbm.typewrite(f"cd ngrok\n")
    kbm.typewrite("ngrok tcp 25565\n")
    pass


def create_server_backup():
    backup_version_selection = askstring(title="Create Server Backup", prompt="Enter the version you want to backup! "
                                                                              "'1.8.9' or '1.12.2' or '1.16.5' "
                                                                              "or '1.17.1'")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\")
        pass
    else:
        pass
    if backup_version_selection == "1.8.9":
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.8.9\\"):
            replace_backup = askyesno(title="Backup Exists", message="A Backup For 1.8.9 Already Exists! Would You "
                                                                     "Like To Replace It?")
            if replace_backup:
                rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.8.9\\")
                copytree(f"{cwd}\\ServerFiles-1.8.9\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.8.9\\")
                showinfo(title="Backup Created", message="Backup Created Successfully!")
                print("Backup Created Successfully!")
                restart()
                sys.exit(0)
            else:
                showinfo(title="Backup Exists", message="Backup Not Created!")
                print("Backup Not Created!")
                restart()
                sys.exit(0)
        else:
            copytree(f"{cwd}\\ServerFiles-1.8.9\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.8.9\\")
            showinfo(title="Backup Created", message="Backup Created Successfully!")
            print("Backup Created Successfully!")
            restart()
            sys.exit(0)
    elif backup_version_selection == "1.12.2":
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2\\"):
            replace_backup = askyesno(title="Backup Exists",
                                      message="A Backup For 1.12.2 Already Exists! Would You Like To Replace It?")
            if replace_backup:
                rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2\\")
                copytree(f"{cwd}\\ServerFiles-1.12.2\\",
                         f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2\\")
                showinfo(title="Backup Created", message="Backup Created Successfully!")
                print("Backup Created Successfully!")
                restart()
                sys.exit(0)
            else:
                showinfo(title="Backup Exists", message="Backup Not Created!")
                print("Backup Not Created!")
                restart()
                sys.exit(0)
        else:
            copytree(f"{cwd}\\ServerFiles-1.12.2\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2\\")
            showinfo(title="Backup Created", message="Backup Created Successfully!")
            print("Backup Created Successfully!")
            restart()
            sys.exit(0)
    elif backup_version_selection == "1.16.5":
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5\\"):
            replace_backup = askyesno(title="Backup Exists",
                                      message="A Backup For 1.16.5 Already Exists! Would You Like To Replace It?")
            if replace_backup:
                rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5\\")
                copytree(f"{cwd}\\ServerFiles-1.16.5\\",
                         f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5\\")
                showinfo(title="Backup Created", message="Backup Created Successfully!")
                print("Backup Created Successfully!")
                restart()
                sys.exit(0)
            else:
                showinfo(title="Backup Exists", message="Backup Not Created!")
                print("Backup Not Created!")
                restart()
                sys.exit(0)
        else:
            copytree(f"{cwd}\\ServerFiles-1.16.5\\",
                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5\\")
            showinfo(title="Backup Created", message="Backup Created Successfully!")
            print("Backup Created Successfully!")
            restart()
            sys.exit(0)
    elif backup_version_selection == "1.17.1":
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1\\"):
            replace_backup = askyesno(title="Backup Exists",
                                      message="A Backup For 1.17.1 Already Exists! Would You Like To Replace It?")
            if replace_backup:
                rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1\\")
                copytree(f"{cwd}\\ServerFiles-1.17.1\\",
                         f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1\\")
                showinfo(title="Backup Created", message="Backup Created Successfully!")
                print("Backup Created Successfully!")
                restart()
                sys.exit(0)
            else:
                showinfo(title="Backup Exists", message="Backup Not Created!")
                print("Backup Not Created!")
                restart()
                sys.exit(0)
        else:
            copytree(f"{cwd}\\ServerFiles-1.17.1\\",
                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1\\")
            showinfo(title="Backup Created", message="Backup Created Successfully!")
            print("Backup Created Successfully!")
            restart()
            sys.exit(0)
    else:
        showerror(title="Backup Server", message="Invalid Version!")
        print("Invalid Version Selected! Please restart to use again!")
        restart()
        sys.exit(0)


def restore_server_backup():
    restore_version_selection = askstring(title="Restore Server",
                                          prompt="Please Select The Version You Would Like To Restore! '1.8.9' or "
                                                 "'1.12.2' or '1.16.5' "
                                                  "or '1.17.1'")
    if restore_version_selection == "1.8.9":
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.1.8"):
            showinfo(title="Backup Not Found", message="Backup Not Found!")
            print("Backup Not Found!")
            restart()
            sys.exit(0)
        else:
            rmtree(f"{cwd}\\ServerFiles-1.8.9\\")
            copytree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.8.9\\", f"{cwd}\\ServerFiles-1.8.9\\")
            showinfo(title="Restore Server", message="Restore Successful!")
            print("Restore Successful!")
            restart()
            sys.exit(0)
    elif restore_version_selection == "1.12.2":
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2"):
            showinfo(title="Backup Not Found", message="Backup Not Found!")
            print("Backup Not Found!")
            restart()
            sys.exit(0)
        else:
            rmtree(f"{cwd}\\ServerFiles-1.12.2\\")
            copytree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2\\", f"{cwd}\\ServerFiles-1.12.2\\")
            showinfo(title="Restore Server", message="Restore Successful!")
            print("Restore Successful!")
            restart()
            sys.exit(0)
    elif restore_version_selection == "1.16.5":
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5"):
            showinfo(title="Backup Not Found", message="Backup Not Found!")
            print("Backup Not Found!")
            restart()
            sys.exit(0)
        else:
            rmtree(f"{cwd}\\ServerFiles-1.16.5\\")
            copytree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5\\",
                     f"{cwd}\\ServerFiles-1.16.5\\")
            showinfo(title="Restore Server", message="Restore Successful!")
            print("Restore Successful!")
            restart()
            sys.exit(0)
    elif restore_version_selection == "1.17.1":
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1"):
            showinfo(title="Backup Not Found", message="Backup Not Found!")
            print("Backup Not Found!")
            restart()
            sys.exit(0)
        else:
            rmtree(f"{cwd}\\ServerFiles-1.17.1\\")
            copytree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1\\",
                     f"{cwd}\\ServerFiles-1.17.1\\")
            showinfo(title="Restore Server", message="Restore Successful!")
            print("Restore Successful!")
            restart()
            sys.exit(0)
    else:
        showerror(title="Restore Server", message="Invalid Version!")
        print("Invalid Version Selected! Please restart to use again!")
        restart()
        sys.exit(0)


def reset_server():
    reset_version_selection = askstring(title="Reset Server",
                                        prompt="Please Select The Version You Would Like To Reset! '1.8.9' or "
                                               "'1.12.2' or '1.16.5' "
                                                "or '1.17.1'")
    if reset_version_selection == "1.8.9":
        version = "1.8.9"
        os.remove(f"{cwd}\\ServerFiles-1.8.9\\ops.json")
        os.remove(f"{cwd}\\ServerFiles-1.8.9\\banned-ips.json")
        os.remove(f"{cwd}\\ServerFiles-1.8.9\\banned-players.json")
        os.remove(f"{cwd}\\ServerFiles-1.8.9\\whitelist.json")
        os.remove(f"{cwd}\\ServerFiles-1.8.9\\usercache.json")
        rmtree(f"{cwd}\\ServerFiles-1.8.9\\world\\")
        rmtree(f"{cwd}\\ServerFiles-1.8.9\\logs\\")
        showinfo(title="Reset Server", message="Reset Successful!")
        print("Reset Successful!")
        restart()
        sys.exit(0)
    elif reset_version_selection == "1.12.2":
        version = "1.12.2"
        os.remove(f"{cwd}\\ServerFiles-1.12.2\\ops.json")
        os.remove(f"{cwd}\\ServerFiles-1.12.2\\banned-ips.json")
        os.remove(f"{cwd}\\ServerFiles-1.12.2\\banned-players.json")
        os.remove(f"{cwd}\\ServerFiles-1.12.2\\whitelist.json")
        os.remove(f"{cwd}\\ServerFiles-1.12.2\\usercache.json")
        rmtree(f"{cwd}\\ServerFiles-1.12.2\\world\\")
        rmtree(f"{cwd}\\ServerFiles-1.12.2\\logs\\")
        showinfo(title="Reset Server", message="Reset Successful!")
        print("Reset Successful!")
        restart()
        sys.exit(0)
    elif reset_version_selection == "1.16.5":
        version = "1.16.5"
        os.remove(f"{cwd}\\ServerFiles-1.16.5\\ops.json")
        os.remove(f"{cwd}\\ServerFiles-1.16.5\\banned-ips.json")
        os.remove(f"{cwd}\\ServerFiles-1.16.5\\banned-players.json")
        os.remove(f"{cwd}\\ServerFiles-1.16.5\\whitelist.json")
        os.remove(f"{cwd}\\ServerFiles-1.16.5\\usercache.json")
        rmtree(f"{cwd}\\ServerFiles-1.16.5\\world\\")
        rmtree(f"{cwd}\\ServerFiles-1.16.5\\logs\\")
        showinfo(title="Reset Server", message="Reset Successful!")
        print("Reset Successful!")
        restart()
        sys.exit(0)
    elif reset_version_selection == "1.17.1":
        version = "1.17.1"
        os.remove(f"{cwd}\\ServerFiles-1.17.1\\ops.json")
        os.remove(f"{cwd}\\ServerFiles-1.17.1\\banned-ips.json")
        os.remove(f"{cwd}\\ServerFiles-1.17.1\\banned-players.json")
        os.remove(f"{cwd}\\ServerFiles-1.17.1\\whitelist.json")
        os.remove(f"{cwd}\\ServerFiles-1.17.1\\usercache.json")
        rmtree(f"{cwd}\\ServerFiles-1.17.1\\world\\")
        rmtree(f"{cwd}\\ServerFiles-1.17.1\\logs\\")
        showinfo(title="Reset Server", message="Reset Successful!")
        print("Reset Successful!")
        restart()
        sys.exit(0)
    else:
        showerror(title="Reset Server", message="Invalid Version!")
        print("Invalid Version Selected! Please restart to use again!")
        restart()
        sys.exit(0)


def inject_custom_map():
    version_select = askstring(title="Select Version",
                               prompt="Please Select The Version You Would Like To Use The Custom Map In! '1.8.9' or "
                                      "'1.12.2' or '1.16.5' "
                                     "or '1.17.1'")
    if version_select == "1.8.9":
        version = "1.8.9"
        pass
    elif version_select == "1.12.2":
        version = "1.12.2"
        pass
    elif version_select == "1.16.5":
        version = "1.16.5"
        pass
    elif version_select == "1.17.1":
        version = "1.17.1"
        pass
    else:
        showerror(title="Select Version", message="Invalid Version!")
        print("Invalid Version Selected! Please restart to use again!")
        restart()
        sys.exit(0)
    custom_map = str(askdirectory(title="Select Custom Map Folder"))
    if custom_map == None:
        showerror(title="Select Custom Map Folder", message="No Folder Selected!")
        print("No Folder Selected! Please restart to use again!")
        restart()
        sys.exit(0)
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\world\\"):
            backup_ask = askyesno(title="Backup Existing World?",
                                  message="Would You Like To Backup The Existing World?\n"
                                          "This Will Save The Current World To A Backup Folder!")
            if backup_ask:
                if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}"):
                    confirm_replace = askyesno(title="Existing Backup Found", message="An existing backup was found! "
                                                                                      "Would you like to replace this"
                                                                                      " backup?")
                    if confirm_replace:
                        copytree(f"{cwd}\\ServerFiles-{version}\\", f"{user_dir}\\Documents\\EasyMinecraftServer"
                                                                    f"\\Backups\\{version}\\")
                        showinfo(title="World Backup", message="Backup was successful. Please restart to use again!")
                        print("Backup Successful!")
                        pass
                    else:
                        showerror(title="World Backup", message="The existing world backup was not replaced! Please "
                                                                "restart to use again!")
                        print("The existing world backup was not replaced! Please restart to use again!")
                        restart()
                        sys.exit(0)
                else:
                    copytree(f"{cwd}\\ServerFiles-{version}\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\")
                    showinfo(title="World Backup", message="Backup was successful. Please restart to use again!")
                    print("Backup Successful!")
                    pass
        else:
            pass
        rmtree(f"{cwd}\\ServerFiles-{version}\\world\\")
        copytree(f"{custom_map}\\", f"{cwd}\\ServerFiles-{version}\\world\\")
        showinfo(title="Custom Map", message="Custom Map Successfully Copied!")
        print("Custom Map Successfully Copied!")
        restart()
        sys.exit(0)


def reset_dimension():
    dim_reset_version = askstring(title="Select Version",
                                  prompt="Please Select The Version You Would Like To Reset Dimension In! '1.8.9' or "
                                         "'1.12.2' or '1.16.5' "
                                         "or '1.17.1'")
    if dim_reset_version == "1.8.9":
        version = "1.8.9"
        pass
    elif dim_reset_version == "1.12.2":
        version = "1.12.2"
        pass
    elif dim_reset_version == "1.16.5":
        version = "1.16.5"
        pass
    elif dim_reset_version == "1.17.1":
        version = "1.17.1"
        pass
    else:
        showerror(title="Reset Dimension", message="Invalid Version!")
        print("Invalid Version Selected! Please restart to use again!")
        restart()
        sys.exit(0)
    dimension_reset = askstring(title="Select Dimension",
                                prompt="Please Select The Dimension You Would Like To Reset! 'OVERWORLD' or "
                                       "'NETHER' or 'END'")
    if dimension_reset.upper() == "OVERWORLD":
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\region\\")
            showinfo(title="Reset Dimension", message="Overworld Successfully Reset! Please Restart To Use Again!")
            print("Overworld Successfully Reset!")
            restart()
            sys.exit(0)
        except Exception as e:
            showerror(title="Reset Dimension", message=f"Error While Resetting {dimension_reset} On Server Version {version}! Error: {e}")
            print(f"Error While Resetting {dimension_reset} On Server Version{version}! Error: {e}")
            restart()
            sys.exit(0)
    elif dimension_reset.upper() == "NETHER":
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM-1\\region\\")
            showinfo(title="Reset Dimension", message="Nether Successfully Reset! Please Restart To Use Again!")
            print("Nether Successfully Reset!")
            restart()
            sys.exit(0)
        except Exception as e:
            showerror(title="Reset Dimension", message=f"Error While Resetting {dimension_reset} On Server Version {version}! Error: {e}")
            print(f"Error While Resetting {dimension_reset} On Server Version{version}! Error: {e}")
            restart()
            sys.exit(0)
    elif dimension_reset.upper() == "END":
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM1\\region\\")
            showinfo(title="Reset Dimension", message="End Successfully Reset! Please Restart To Use Again!")
            print("End Successfully Reset!")
            restart()
            sys.exit(0)
        except Exception as e:
            showerror(title="Reset Dimension", message=f"Error While Resetting {dimension_reset} On Server Version {version}! Error: {e}")
            print(f"Error While Resetting {dimension_reset} On Server Version{version}! Error: {e}")
            restart()
            sys.exit(0)
    else:
        showerror(title="Reset Dimension", message="Invalid Dimension!")
        print("Invalid Dimension Selected! Please restart to use again!")
        restart()
        sys.exit(0)



if is_admin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)
cwd = os.getcwd()
user_dir = os.path.expanduser("~")
print("EasyMinecraftServer Version: 1.5.0")
print("Created By: @teekar2023")
print(f"User Directory: {user_dir}")
print(f"Current Working Directory: {cwd}")
root = Tk()
root.withdraw()
if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\"):
    os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\")
    pass
else:
    pass
if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\"):
    os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\")
    pass
else:
    pass
try:
    url = "http://github.com/teekar2023/EasyMinecraftServer/releases/latest/"
    r = requests.get(url, allow_redirects=True)
    redirected_url = r.url
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v1.5.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        print(f"Updated Version Available: {new_version}")
        changelog_url = "https://raw.githubusercontent.com/teekar2023/EasyMinecraftServer/master/CHANGELOG.txt"
        changelog_download = urllib.request.urlopen(changelog_url)
        try:
            open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\changelog.txt", mode="w+", encoding="utf8").truncate()
        except Exception:
            pass
        changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\changelog.txt", mode="wb")
        try:
            while True:
                changelog_data = changelog_download.read()
                if not changelog_data:
                    break
                else:
                    changelog_file.write(changelog_data)
                    pass
        except Exception:
            changelog_file.write(str.encode("There Was An Error Downloading Changelog Information!"))
            pass
        changelog_file.close()
        changelog = str(open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\changelog.txt", mode="r", encoding="utf8").read())
        showwarning(title="Update Available", message="An update is available. Please update to the latest version to "
                                                      f"use this program.\nChangelog: {changelog}")
        print(changelog)
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
for i in range(3):
    print("")
    pass
print("-------------------------")
print("1. Start Server")
print("2. Create Server Backup")
print("3. Restore Server Backup")
print("4. Reset Server")
print("5. Use A Custom Map In Server")
print("6. Reset A Dimension In Server (BETA)")
print("7. Changelog")
print("8. Exit")
print("-------------------------")
main_input = input("What Would You Like To Do? Enter The Corresponding Number:")
if main_input == "1":
    pass
elif main_input == "2":
    create_server_backup()
elif main_input == "3":
    restore_server_backup()
elif main_input == "4":
    reset_server()
elif main_input == "5":
    inject_custom_map()
elif main_input == "6":
    reset_dimension()
elif main_input == "7":
    changelog = str(open(f"{cwd}\\CHANGELOG.txt", "r").read())
    showinfo(title="EasyMinecraftServer Changelog", message=changelog)
    print(changelog)
    restart()
    sys.exit(0)
elif main_input == "8":
    print("Exiting...")
    restart()
    sys.exit(0)
else:
    showerror(title="EasyMinecraftServer", message="Invalid Input! Please Restart To Use Again!")
    print("Invalid Input! Please restart to use again!")
    restart()
    sys.exit(0)
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
    showwarning(title="WARNING", message="DO NOT TOUCH ANYTHING FOR 3 SECONDS AFTER CLOSING THIS POPUP!")
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
print(f"Starting Minecraft Server On {version}")
os.system(f"java -Xmx{ram_input}M -Xms{ram_input}M -jar server.jar nogui")
time.sleep(1)
print("Server Stopped...")
showinfo(title="Minecraft Server", message="Server Stopped Successfully!")
print("Exiting...")
time.sleep(1)
sys.exit(0)
