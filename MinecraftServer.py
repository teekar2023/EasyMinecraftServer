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
from tkinter.filedialog import askdirectory, asksaveasfile
from shutil import copytree, rmtree


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart():
    confirm_restart = askyesno(title="Restart", message="Restart EasyMinecraftServer?")
    if confirm_restart:
        os.system("clear")
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        sys.exit(0)
    else:
        print("Exiting...")
        time.sleep(1)
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
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.8.9\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.8.9\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.12.2\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.16.5\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.17.1\\")
        pass
    else:
        pass
    if backup_version_selection == "1.8.9":
        backup_version = "1.8.9"
        pass
    elif backup_version_selection == "1.12.2":
        backup_version = "1.12.2"
        pass
    elif backup_version_selection == "1.16.5":
        backup_version = "1.16.5"
        pass
    elif backup_version_selection == "1.17.1":
        backup_version = "1.17.1"
        pass
    else:
        showerror(title="Error", message="Invalid Version!")
        print("Invalid Version!")
        restart()
        sys.exit(0)
    backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
    if not backup_name:
        showerror(title="Error", message="Invalid Name!")
        print("Invalid Name!")
        restart()
        sys.exit(0)
    else:
        pass
    if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\"):
        showerror(title="Backup Error", message="Backup with the same name already exists! Please try again!")
        print("Backup with the same name already exists! Please try again!")
        restart()
        sys.exit(0)
    else:
        try:
            copytree(f"{cwd}\\ServerFiles-{backup_version}\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            showinfo(title="Backup Successful", message="Backup Successful!")
            print("Backup Successful!")
            restart()
            sys.exit(0)
        except Exception as e:
            showerror(title="Backup Error", message=f"Error while performing backup: {e}")
            print(f"Error while performing backup: {e}")
            restart()
            sys.exit(0)


def restore_server_backup():
    backup_version_selection = askstring(title="Create Server Backup", prompt="Enter the version you want to backup! "
                                                                              "'1.8.9' or '1.12.2' or '1.16.5' "
                                                                              "or '1.17.1'")
    if backup_version_selection == "1.8.9":
        backup_version = "1.8.9"
        pass
    elif backup_version_selection == "1.12.2":
        backup_version = "1.12.2"
        pass
    elif backup_version_selection == "1.16.5":
        backup_version = "1.16.5"
        pass
    elif backup_version_selection == "1.17.1":
        backup_version = "1.17.1"
        pass
    else:
        showerror(title="Error", message="Invalid Version!")
        print("Invalid Version!")
        restart()
        sys.exit(0)
    backup_path = str(askdirectory(title="Restore Server Backup", initialdir=f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"))
    if not os.path.exists(f"{backup_path}\\server.jar"):
        showerror(title="Backup Restore Error", message="This backup is invalid and wont work!")
        print("This backup is invalid and wont work!")
        restart()
        sys.exit(0)
    else:
        confirm_restore = askyesno(title="Restore Server Backup", message="Are you sure you want to restore this "
                                                                          "backup? It will replace any current data "
                                                                          "in the server!")
        if confirm_restore:
            if os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\ops.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\banned-players.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\banned-ips.json\\"):
                backup_current_server = askyesno(title="Restore Server Backup", message="You have current data in the server! Would you like "
                                                                "to perform a backup?")
                if backup_current_server:
                    backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
                    if not backup_name:
                        showerror(title="Error", message="Invalid Name!")
                        print("Invalid Name!")
                        restart()
                        sys.exit(0)
                    else:
                        pass
                    if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\"):
                        showerror(title="Backup Error", message="Backup with the same name already exists! Please try again!")
                        print("Backup with the same name already exists! Please try again!")
                        restart()
                        sys.exit(0)
                    else:
                        try:
                            copytree(f"{cwd}\\ServerFiles-{backup_version}\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
                            showinfo(title="Backup Successful", message="Backup Successful!")
                            print("Backup Successful!")
                            pass
                        except Exception as e:
                            showerror(title="Backup Error", message=f"Error while performing backup: {e}")
                            print(f"Error while performing backup: {e}")
                            restart()
                            sys.exit(0)
                        pass
                else:
                    showwarning(title="Restore Server Backup", message="You have chosen not to backup the current "
                                                                       "server! Current server data will be "
                                                                       "overwritten!")
                    pass
                pass
            else:
                pass
            try:
                rmtree(f"{cwd}\\ServerFiles-{backup_version}\\")
                copytree(f"{backup_path}\\", f"{cwd}\\ServerFiles-{backup_version}\\")
                showinfo(title="Restore Successful", message="Restore Successful!")
                print("Restore Successful!")
                restart()
                sys.exit(0)
            except Exception as e:
                showerror(title="Backup Restore Error", message=f"Error while restoring backup: {e}")
                print(f"Error while restoring backup: {e}")
                restart()
                sys.exit(0)
        else:
            showinfo(title="Restore Cancelled", message="Restore Cancelled!")
            print("Restore Cancelled!")
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
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\ops.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-players.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-ips.json\\"):
            backup_current_server = askyesno(title="Restore Server Backup", message="You have current data in the server! Would you like "
                                                            "to perform a backup?")
            if backup_current_server:
                backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
                if not backup_name:
                    showerror(title="Error", message="Invalid Name!")
                    print("Invalid Name!")
                    restart()
                    sys.exit(0)
                else:
                    pass
                if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
                    showerror(title="Backup Error", message="Backup with the same name already exists! Please try again!")
                    print("Backup with the same name already exists! Please try again!")
                    restart()
                    sys.exit(0)
                else:
                    try:
                        copytree(f"{cwd}\\ServerFiles-{version}\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
                        showinfo(title="Backup Successful", message="Backup Successful!")
                        print("Backup Successful!")
                        pass
                    except Exception as e:
                        showerror(title="Backup Error", message=f"Error while performing backup: {e}")
                        print(f"Error while performing backup: {e}")
                        restart()
                        sys.exit(0)
                    pass
            else:
                showwarning(title="Restore Server Backup", message="You have chosen not to backup the current "
                                                                       "server! Current server data will be "
                                                                       "overwritten!")
                pass
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
            showerror(title="Reset Dimension",
                      message=f"Error While Resetting {dimension_reset} On Server Version {version}! Error: {e}")
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
            showerror(title="Reset Dimension",
                      message=f"Error While Resetting {dimension_reset} On Server Version {version}! Error: {e}")
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
            showerror(title="Reset Dimension",
                      message=f"Error While Resetting {dimension_reset} On Server Version {version}! Error: {e}")
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
    print("Admin access not granted!")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)
os.system("clear")
cwd = os.getcwd()
user_dir = os.path.expanduser("~")
print("EasyMinecraftServer Version: 1.8.0")
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
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v1.8.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        print(f"Updated Version Available: {new_version}")
        changelog_url = "https://raw.githubusercontent.com/teekar2023/EasyMinecraftServer/master/CHANGELOG.txt"
        changelog_download = urllib.request.urlopen(changelog_url)
        try:
            open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\changelog.txt", mode="w+",
                 encoding="utf8").truncate()
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
        except Exception as e:
            changelog_file.write(str.encode(f"There Was An Error Downloading Changelog Information! Error: {e}"))
            pass
        changelog_file.close()
        changelog = str(
            open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\changelog.txt", mode="r", encoding="utf8").read())
        showwarning(title="Update Available", message="An update is available. Please update to the latest version to "
                                                      f"use this program.\nChangelog: {changelog}")
        print(changelog)
        download_local = askyesno(title="Download Update", message="Press 'YES' to download the update from the "
                                                                   "program or press 'NO' to download the update from"
                                                                   " a web browser!")
        if download_local:
            new_url = str(redirected_url) + "/ChikkooAI-Setup.exe"
            download_url = new_url.replace("tag", "download")
            print("------------------------------")
            print(f"Downloading Update From: {download_url}...")
            print("Please do not exit the program while downloading...")
            f = asksaveasfile(mode="wb", defaultextension=".exe", initialfile="MinecraftServerInstaller.exe")
            f2 = urllib.request.urlopen(download_url)
            while True:
                data = f2.read()
                if not data:
                    break
                else:
                    pass
                f.write(data)
            file_string = str(f)
            installed_file1 = file_string.replace("<_io.BufferedWriter name='", "")
            installed_file2 = installed_file1.replace("'>", "")
            f.close()
            install_confirmation = askyesno(title="Update",
                                            message=f"Update Completed! Would You Like To Install? Installer Location: {installed_file2}.exe")
            if install_confirmation:
                os.startfile(f"{installed_file2}.exe")
                sys.exit(0)
            else:
                showinfo(title="Update Installer", message="Update Installer Downloaded To: {"
                                                           "installed_file2}.exe\n\nPlease run this installer to "
                                                           "update EasyMinecraftServer!")
                sys.exit(0)
        else:
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
print("6. Reset A Dimension In Server")
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
    time.sleep(1)
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
    showwarning(title="WARNING", message="DO NOT TOUCH ANYTHING FOR AT LEAST 3 SECONDS AFTER CLOSING THIS POPUP!")
    ngrok_process = Thread(target=ngrok)
    ngrok_process.start()
    time.sleep(3)
    pass
ram_input = askinteger(title="Minecraft Server RAM", prompt="How many mb of ram would you like in the server? Please "
                                                            "enter an "
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
server_properties = str(open(f"{cwd}\\ServerFiles-{version}\\server.properties", "r").read())
print("---SERVER PROPERTIES---")
print(server_properties)
os.system(f"java -Xmx{ram_input}M -Xms{ram_input}M -jar server.jar nogui")
time.sleep(1)
print("Server Stopped...")
showinfo(title="Minecraft Server", message="Server Stopped Successfully!")
print("Exiting...")
time.sleep(1)
sys.exit(0)
