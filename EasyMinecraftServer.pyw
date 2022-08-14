#  Copyright (c) 2022. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

import ctypes
import glob
import json
import logging
import os
import subprocess
import sv_ttk
import darkdetect
import sys
import time
import urllib
import webbrowser
import psutil
import pyautogui as kbm
import requests
from shutil import rmtree, copytree, copy, which, make_archive
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.simpledialog import askstring
from jproperties import Properties
from win10toast import ToastNotifier


def start_server():
    start_server_window = Toplevel(root)
    start_server_window.title("Start Server")
    start_server_window.geometry("315x315")
    start_server_label = ttk.Label(start_server_window,
                                   text="Select The Version You Would Like To Start\nOr Enter A New Version To Create A Server!")
    start_server_label.pack()
    server_version_variable = StringVar()
    start_server_version_list = ttk.Combobox(start_server_window, values=get_server_versions(),
                                             textvariable=server_version_variable)
    start_server_version_list.pack()
    try:
        start_server_version_list.current(0)
        pass
    except Exception as e:
        pass
    ram_allocation_amount_label = ttk.Label(start_server_window, text="RAM Allocation Amount In MB")
    ram_allocation_amount_label.pack()
    ram_allocation_amount_setting = settings_json["ram_allocation_amount"]
    ram_allocation_variable = StringVar()
    ram_allocation_variable.set(ram_allocation_amount_setting)
    ram_allocation_amount_entry = ttk.Entry(start_server_window, textvariable=ram_allocation_variable, width=10)
    ram_allocation_amount_entry.pack()
    gui_variable = StringVar()
    current_gui_setting = settings_json["server_gui"]
    gui_variable.set(current_gui_setting)
    server_gui_label = ttk.Label(start_server_window, text="Server GUI")
    server_gui_label.pack()
    start_server_gui_true = ttk.Radiobutton(start_server_window, text="True", variable=gui_variable, value="True")
    start_server_gui_true.pack()
    start_server_gui_false = ttk.Radiobutton(start_server_window, text="False", variable=gui_variable, value="False")
    start_server_gui_false.pack()
    server_backup_variable = StringVar()
    current_server_backup = settings_json["auto_server_backup"]
    server_backup_variable.set(current_server_backup)
    server_backup_label = ttk.Label(start_server_window, text="Auto Server Backup")
    server_backup_label.pack()
    start_server_backup_true = ttk.Radiobutton(start_server_window, text="True", variable=server_backup_variable,
                                               value="True")
    start_server_backup_true.pack()
    start_server_backup_false = ttk.Radiobutton(start_server_window, text="False", variable=server_backup_variable,
                                                value="False")
    start_server_backup_false.pack()
    wait_var = IntVar()
    start_button = ttk.Button(start_server_window, text="Start Server", command=lambda: wait_var.set(1),
                              style="Accent.TButton")
    start_button.pack()
    start_button.wait_variable(wait_var)
    start_server_window.destroy()
    version_selection = server_version_variable.get()
    server_download_url = f"https://serverjars.com/api/fetchJar/vanilla/vanilla/{version_selection}/"
    logging.info("Server download url: " + server_download_url)
    if not os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\"):
        logging.info(f"New server version entered: {version_selection}")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\"):
            if len(get_all_backups(version_selection)) == 0:
                pass
            else:
                logging.info("Found server backups")
                restore_ask = askyesno("Restore Server Backup",
                                       "Server backups for this version were found! Would you like to restore one?")
                if restore_ask:
                    wait_var.set(0)
                    restore_backup_window = Toplevel(root)
                    restore_backup_window.title("Restore Backup")
                    restore_backup_window.geometry("315x315")
                    restore_backup_label = ttk.Label(restore_backup_window,
                                                     text="Select The Backup You Would Like To Restore")
                    restore_backup_label.pack()
                    backup_name_var = StringVar()
                    restore_backup_list = ttk.Combobox(restore_backup_window, values=get_all_backups(version_selection),
                                                       textvariable=backup_name_var)
                    restore_backup_list.pack()
                    restore_backup_list.current(0)
                    restore_backup_button = ttk.Button(restore_backup_window, text="Restore Backup",
                                                       style="Accent.TButton", command=lambda: wait_var.set(1))
                    restore_backup_button.pack()
                    restore_backup_button.wait_variable(wait_var)
                    restore_backup_window.destroy()
                    backup_files = backup_name_var.get()
                    if not os.path.exists(
                            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\{backup_files}\\server.jar"):
                        logging.error("Invalid Backup Selected In start_server()")
                        showerror(title="Error", message="Invalid Backup Selected!")
                        return
                    else:
                        logging.info("Valid Backup Selected In start_server()")
                        logging.info(
                            "Copying from " + f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\{backup_files}\\" + " to " + f"{cwd}\\ServerFiles-{version_selection}\\")
                        copytree(
                            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\{backup_files}\\",
                            f"{cwd}\\ServerFiles-{version_selection}\\")
                        logging.info("Restore Successful")
                        showinfo(title="Restore Successful",
                                 message="Restore successful! Server is ready to be started!")
                        return
                else:
                    logging.info("Server restore cancelled")
                    pass
                pass
            pass
        else:
            pass
        logging.info(f"Setting up new server version: {version_selection}")
        os.mkdir(f"{cwd}\\ServerFiles-{version_selection}\\")
        logging.info("Created server directory")
        logging.info(f"Creating ServerFiles Exclusion Path for version {version_selection}")
        subprocess.Popen(["powershell.exe", "-Command", "Add-MpPreference", "-ExclusionPath",
                          f"'{cwd}\\ServerFiles-{version_selection}\\'"], startupinfo=info)
        logging.info("Created server files exclusion path")
        logging.info(f"Downloading server version {version_selection}")
        try:
            f = open(f"{cwd}\\ServerFiles-{version_selection}\\server.jar", 'wb')
            showwarning(title="Downloading Server File",
                        message="To create a new server version, the server files will need to be downloaded! This may take a minute!")
            logging.info("Downloading server jar file")
            f2 = urllib.request.urlopen(server_download_url)
            while True:
                data = f2.read()
                if not data:
                    break
                else:
                    f.write(data)
                    pass
                pass
            f.close()
            logging.info("Server jar file downloaded")
            eula_check = askyesno(title="Minecraft Server EULA",
                                  message="Do you agree to the minecraft server EULA? https://account.mojang.com/documents/minecraft_eula")
            if eula_check:
                logging.info("EULA Accepted")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\eula.txt",
                     f"{cwd}\\ServerFiles-{version_selection}\\eula.txt")
                pass
            else:
                logging.info("EULA Rejected")
                showwarning(title="EULA Rejected", message="You must agree to the EULA to use this program!")
                rmtree(f"{cwd}\\ServerFiles-{version_selection}\\")
                return
            list_one = ["1.7", "1.7.1", "1.7.2", "1.7.3", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9",
                        "1.7.10", "1.8", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8",
                        "1.8.9", "1.9", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.10", "1.10.1", "1.10.2", "1.11",
                        "1.11.1", "1.11.2"]
            list_two = ["1.12", "1.12.1", "1.12.2", "1.13", "1.13.1", "1.13.2", "1.14", "1.14.1", "1.14.2", "1.14.3",
                        "1.14.4", "1.15", "1.15.1", "1.15.2", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.16.5"]
            if version_selection in list_one:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_17-111.xml",
                     f"{cwd}\\ServerFiles-{version_selection}\\log4j2_17-111.xml")
                pass
            elif version_selection in list_two:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_112-116.xml",
                     f"{cwd}\\ServerFiles-{version_selection}\\log4j2_112-116.xml")
                pass
            else:
                pass
            if settings_json["ngrok_authtoken"] == ngrok_secret:
                logging.info("Injecting Chimpanzee222 as an operator")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\ops.json",
                     f"{cwd}\\ServerFiles-{version_selection}\\ops.json")
                logging.info("Copied ops.json")
                pass
            else:
                pass
            logging.info("Server files set up")
            pass
        except Exception as e:
            logging.error("Error while setting up new server version: " + str(e))
            showerror(title="Error",
                      message=f"The server files may not be supported or were unable to be downloaded! Error while downloading new server files: {e}")
            f.close()
            rmtree(f"{cwd}\\ServerFiles-{version_selection}\\")
            return
        pass
    else:
        logging.info("Server version already exists")
        pass
    logging.info("Version Selected In start_server(): " + version_selection)
    if os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\server.properties"):
        server_prop_check = open(f"{cwd}\\ServerFiles-{version_selection}\\server.properties", 'r')
        if "port" in str(server_prop_check.read()):
            server_prop_check.close()
            logging.info("Reading Server Properties File For Server Port")
            p = Properties()
            with open(f"{cwd}\\ServerFiles-{version_selection}\\server.properties", "rb") as f:
                p.load(f)
            port = str(p.get("server-port").data)
            pass
        else:
            server_prop_check.close()
            logging.info("Defaulting To Port 25565")
            port = "25565"
            pass
        pass
    else:
        port = "25565"
        pass
    port_forwarded = askyesno(title="Minecraft Server",
                              message=f"Is tcp port {port} forwarded on your network? Press 'NO' if you are not sure!")
    if port_forwarded:
        logging.info("Port Forward Confirmed In start_server()")
        port_forward_status = "True"
        pass
    else:
        logging.info("Port Forward Not Confirmed In start_server()")
        port_forward_status = "False"
        showwarning(title="WARNING",
                    message="DO NOT TOUCH ANYTHING FOR AT LEAST 5 SECONDS AFTER CLOSING THIS POPUP IN ORDER TO LET NGROK PROCESS SUCCESSFULLY START!")
        logging.info("Connecting To NGROK For Port Forwarding")
        authtoken = settings_json["ngrok_authtoken"]
        os.system("start cmd")
        time.sleep(1)
        kbm.typewrite("cd ngrok\n")
        kbm.typewrite(f"ngrok config add-authtoken {authtoken}\n")
        kbm.typewrite(f"ngrok tcp {port}\n")
        time.sleep(1)
        pass
    server_gui_setting = gui_variable.get()
    logging.info("Server GUI " + server_gui_setting)
    ram_amount = ram_allocation_variable.get()
    logging.info("RAM Allocation Amount " + ram_amount)
    server_backup = server_backup_variable.get()
    logging.info("Auto Server Backup " + server_backup)
    launch_version_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt", 'w+')
    try:
        launch_version_file.truncate(0)
        pass
    except Exception:
        pass
    launch_version_file.write(f"{version_selection}")
    launch_version_file.close()
    backup_interval = settings_json["backup_interval"]
    logging.info("Backup Interval " + backup_interval)
    showwarning(title="WARNING",
                message="DO NOT TOUCH ANYTHING FOR AT LEAST 10 SECONDS AFTER CLOSING THIS POPUP IN ORDER TO LET SERVER SUCCESSFULLY START!")
    if server_gui_setting == "True":
        logging.info("Starting Powershell Process")
        os.system("start powershell")
        time.sleep(1)
        logging.info("Starting Minecraft Server With GUI")
        logging.info(
            f"Executing System Command In Powershell: MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}")
        kbm.typewrite(
            f"MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}\n")
        kbm.typewrite("exit\n")
        time.sleep(1)
        logging.info("Moving To exit_program_force()")
        exit_program_force()
        sys.exit(0)
    else:
        logging.info("Starting Powershell Process")
        os.system("start powershell")
        time.sleep(1)
        logging.info("Starting Minecraft Server Without GUI")
        logging.info(
            f"Executing System Command In Powershell: MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}")
        kbm.typewrite(
            f"MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}\n")
        time.sleep(1)
        logging.info("Moving To exit_program_force()")
        exit_program_force()
        sys.exit(0)


def start_server_event(event):
    start_server_window = Toplevel(root)
    start_server_window.title("Start Server")
    start_server_window.geometry("315x315")
    start_server_label = ttk.Label(start_server_window,
                                   text="Select The Version You Would Like To Start\nOr Enter A New Version To Create A Server!")
    start_server_label.pack()
    server_version_variable = StringVar()
    start_server_version_list = ttk.Combobox(start_server_window, values=get_server_versions(),
                                             textvariable=server_version_variable)
    start_server_version_list.pack()
    try:
        start_server_version_list.current(0)
        pass
    except Exception as e:
        pass
    ram_allocation_amount_label = ttk.Label(start_server_window, text="RAM Allocation Amount In MB")
    ram_allocation_amount_label.pack()
    ram_allocation_amount_setting = settings_json["ram_allocation_amount"]
    ram_allocation_variable = StringVar()
    ram_allocation_variable.set(ram_allocation_amount_setting)
    ram_allocation_amount_entry = ttk.Entry(start_server_window, textvariable=ram_allocation_variable, width=10)
    ram_allocation_amount_entry.pack()
    gui_variable = StringVar()
    current_gui_setting = settings_json["server_gui"]
    gui_variable.set(current_gui_setting)
    server_gui_label = ttk.Label(start_server_window, text="Server GUI")
    server_gui_label.pack()
    start_server_gui_true = ttk.Radiobutton(start_server_window, text="True", variable=gui_variable, value="True")
    start_server_gui_true.pack()
    start_server_gui_false = ttk.Radiobutton(start_server_window, text="False", variable=gui_variable, value="False")
    start_server_gui_false.pack()
    server_backup_variable = StringVar()
    current_server_backup = settings_json["auto_server_backup"]
    server_backup_variable.set(current_server_backup)
    server_backup_label = ttk.Label(start_server_window, text="Auto Server Backup")
    server_backup_label.pack()
    start_server_backup_true = ttk.Radiobutton(start_server_window, text="True", variable=server_backup_variable,
                                               value="True")
    start_server_backup_true.pack()
    start_server_backup_false = ttk.Radiobutton(start_server_window, text="False", variable=server_backup_variable,
                                                value="False")
    start_server_backup_false.pack()
    wait_var = IntVar()
    start_button = ttk.Button(start_server_window, text="Start Server", command=lambda: wait_var.set(1),
                              style="Accent.TButton")
    start_button.pack()
    start_button.wait_variable(wait_var)
    start_server_window.destroy()
    version_selection = server_version_variable.get()
    server_download_url = f"https://serverjars.com/api/fetchJar/vanilla/vanilla/{version_selection}/"
    logging.info("Server download url: " + server_download_url)
    if not os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\"):
        logging.info(f"New server version entered: {version_selection}")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\"):
            if len(get_all_backups(version_selection)) == 0:
                pass
            else:
                logging.info("Found server backups")
                restore_ask = askyesno("Restore Server Backup",
                                       "Server backups for this version were found! Would you like to restore one?")
                if restore_ask:
                    wait_var.set(0)
                    restore_backup_window = Toplevel(root)
                    restore_backup_window.title("Restore Backup")
                    restore_backup_window.geometry("315x315")
                    restore_backup_label = ttk.Label(restore_backup_window,
                                                     text="Select The Backup You Would Like To Restore")
                    restore_backup_label.pack()
                    backup_name_var = StringVar()
                    restore_backup_list = ttk.Combobox(restore_backup_window, values=get_all_backups(version_selection),
                                                       textvariable=backup_name_var)
                    restore_backup_list.pack()
                    restore_backup_list.current(0)
                    restore_backup_button = ttk.Button(restore_backup_window, text="Restore Backup",
                                                       style="Accent.TButton", command=lambda: wait_var.set(1))
                    restore_backup_button.pack()
                    restore_backup_button.wait_variable(wait_var)
                    restore_backup_window.destroy()
                    backup_files = backup_name_var.get()
                    if not os.path.exists(
                            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\{backup_files}\\server.jar"):
                        logging.error("Invalid Backup Selected In start_server()")
                        showerror(title="Error", message="Invalid Backup Selected!")
                        return
                    else:
                        logging.info("Valid Backup Selected In start_server()")
                        logging.info(
                            "Copying from " + f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\{backup_files}\\" + " to " + f"{cwd}\\ServerFiles-{version_selection}\\")
                        copytree(
                            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\{backup_files}\\",
                            f"{cwd}\\ServerFiles-{version_selection}\\")
                        logging.info("Restore Successful")
                        showinfo(title="Restore Successful",
                                 message="Restore successful! Server is ready to be started!")
                        return
                else:
                    logging.info("Server restore cancelled")
                    pass
                pass
            pass
        else:
            pass
        logging.info(f"Setting up new server version: {version_selection}")
        os.mkdir(f"{cwd}\\ServerFiles-{version_selection}\\")
        logging.info("Created server directory")
        logging.info(f"Creating ServerFiles Exclusion Path for version {version_selection}")
        subprocess.Popen(["powershell.exe", "-Command", "Add-MpPreference", "-ExclusionPath",
                          f"'{cwd}\\ServerFiles-{version_selection}\\'"], startupinfo=info)
        logging.info("Created server files exclusion path")
        logging.info(f"Downloading server version {version_selection}")
        try:
            f = open(f"{cwd}\\ServerFiles-{version_selection}\\server.jar", 'wb')
            showwarning(title="Downloading Server File",
                        message="To create a new server version, the server files will need to be downloaded! This may take a minute!")
            logging.info("Downloading server jar file")
            f2 = urllib.request.urlopen(server_download_url)
            while True:
                data = f2.read()
                if not data:
                    break
                else:
                    f.write(data)
                    pass
                pass
            f.close()
            logging.info("Server jar file downloaded")
            eula_check = askyesno(title="Minecraft Server EULA",
                                  message="Do you agree to the minecraft server EULA? https://account.mojang.com/documents/minecraft_eula")
            if eula_check:
                logging.info("EULA Accepted")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\eula.txt",
                     f"{cwd}\\ServerFiles-{version_selection}\\eula.txt")
                pass
            else:
                logging.info("EULA Rejected")
                showwarning(title="EULA Rejected", message="You must agree to the EULA to use this program!")
                rmtree(f"{cwd}\\ServerFiles-{version_selection}\\")
                return
            list_one = ["1.7", "1.7.1", "1.7.2", "1.7.3", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9",
                        "1.7.10", "1.8", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8",
                        "1.8.9", "1.9", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.10", "1.10.1", "1.10.2", "1.11",
                        "1.11.1", "1.11.2"]
            list_two = ["1.12", "1.12.1", "1.12.2", "1.13", "1.13.1", "1.13.2", "1.14", "1.14.1", "1.14.2", "1.14.3",
                        "1.14.4", "1.15", "1.15.1", "1.15.2", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.16.5"]
            if version_selection in list_one:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_17-111.xml",
                     f"{cwd}\\ServerFiles-{version_selection}\\log4j2_17-111.xml")
                pass
            elif version_selection in list_two:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_112-116.xml",
                     f"{cwd}\\ServerFiles-{version_selection}\\log4j2_112-116.xml")
                pass
            else:
                pass
            if settings_json["ngrok_authtoken"] == ngrok_secret:
                logging.info("Injecting Chimpanzee222 as an operator")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\ops.json",
                     f"{cwd}\\ServerFiles-{version_selection}\\ops.json")
                logging.info("Copied ops.json")
                pass
            else:
                pass
            logging.info("Server files set up")
            pass
        except Exception as e:
            logging.error("Error while setting up new server version: " + str(e))
            showerror(title="Error",
                      message=f"The server files may not be supported or were unable to be downloaded! Error while downloading new server files: {e}")
            f.close()
            rmtree(f"{cwd}\\ServerFiles-{version_selection}\\")
            return
        pass
    else:
        logging.info("Server version already exists")
        pass
    logging.info("Version Selected In start_server(): " + version_selection)
    if os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\server.properties"):
        server_prop_check = open(f"{cwd}\\ServerFiles-{version_selection}\\server.properties", 'r')
        if "port" in str(server_prop_check.read()):
            server_prop_check.close()
            logging.info("Reading Server Properties File For Server Port")
            p = Properties()
            with open(f"{cwd}\\ServerFiles-{version_selection}\\server.properties", "rb") as f:
                p.load(f)
            port = str(p.get("server-port").data)
            pass
        else:
            server_prop_check.close()
            logging.info("Defaulting To Port 25565")
            port = "25565"
            pass
        pass
    else:
        port = "25565"
        pass
    port_forwarded = askyesno(title="Minecraft Server",
                              message=f"Is tcp port {port} forwarded on your network? Press 'NO' if you are not sure!")
    if port_forwarded:
        logging.info("Port Forward Confirmed In start_server()")
        port_forward_status = "True"
        pass
    else:
        logging.info("Port Forward Not Confirmed In start_server()")
        port_forward_status = "False"
        showwarning(title="WARNING",
                    message="DO NOT TOUCH ANYTHING FOR AT LEAST 5 SECONDS AFTER CLOSING THIS POPUP IN ORDER TO LET NGROK PROCESS SUCCESSFULLY START!")
        logging.info("Connecting To NGROK For Port Forwarding")
        authtoken = settings_json["ngrok_authtoken"]
        os.system("start cmd")
        time.sleep(1)
        kbm.typewrite("cd ngrok\n")
        kbm.typewrite(f"ngrok config add-authtoken {authtoken}\n")
        kbm.typewrite(f"ngrok tcp {port}\n")
        time.sleep(1)
        pass
    server_gui_setting = gui_variable.get()
    logging.info("Server GUI " + server_gui_setting)
    ram_amount = ram_allocation_variable.get()
    logging.info("RAM Allocation Amount " + ram_amount)
    server_backup = server_backup_variable.get()
    logging.info("Auto Server Backup " + server_backup)
    launch_version_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt", 'w+')
    try:
        launch_version_file.truncate(0)
        pass
    except Exception:
        pass
    launch_version_file.write(f"{version_selection}")
    launch_version_file.close()
    backup_interval = settings_json["backup_interval"]
    logging.info("Backup Interval " + backup_interval)
    showwarning(title="WARNING",
                message="DO NOT TOUCH ANYTHING FOR AT LEAST 10 SECONDS AFTER CLOSING THIS POPUP IN ORDER TO LET SERVER SUCCESSFULLY START!")
    if server_gui_setting == "True":
        logging.info("Starting Powershell Process")
        os.system("start powershell")
        time.sleep(1)
        logging.info("Starting Minecraft Server With GUI")
        logging.info(
            f"Executing System Command In Powershell: MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}")
        kbm.typewrite(
            f"MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}\n")
        kbm.typewrite("exit\n")
        time.sleep(1)
        logging.info("Moving To exit_program_force()")
        exit_program_force()
        sys.exit(0)
    else:
        logging.info("Starting Powershell Process")
        os.system("start powershell")
        time.sleep(1)
        logging.info("Starting Minecraft Server Without GUI")
        logging.info(
            f"Executing System Command In Powershell: MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}")
        kbm.typewrite(
            f"MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port} {backup_interval}\n")
        time.sleep(1)
        logging.info("Moving To exit_program_force()")
        exit_program_force()
        sys.exit(0)


def create_server_backup():
    server_backup_window = Toplevel(root)
    server_backup_window.title("Minecraft Server Backup")
    server_backup_window.geometry("300x300")
    backup_version_label = ttk.Label(server_backup_window, text="Select Server Version To Backup")
    backup_version_label.pack()
    backup_version_variable = StringVar()
    backup_version_check = ttk.Combobox(server_backup_window, values=get_server_versions(),
                                        textvariable=backup_version_variable)
    backup_version_check.pack()
    try:
        backup_version_check.current(0)
        pass
    except Exception as e:
        pass
    backup_name_variable = StringVar()
    backup_name_label = ttk.Label(server_backup_window, text="Enter A Name For The Backup")
    backup_name_label.pack()
    backup_name_entry = ttk.Entry(server_backup_window, textvariable=backup_name_variable)
    backup_name_entry.pack()
    overwrite_backup_name_exists_variable = StringVar()
    overwrite_backup_name_exists_variable.set("False")
    overwrite_backup_name_exists_check = ttk.Checkbutton(server_backup_window,
                                                         variable=overwrite_backup_name_exists_variable, onvalue="True",
                                                         offvalue="False", text="Overwrite Backup If It Already Exists")
    overwrite_backup_name_exists_check.pack()
    backup_wait_var = IntVar()
    backup_button = ttk.Button(server_backup_window, text="Backup Server", command=lambda: backup_wait_var.set(1),
                               style="Accent.TButton")
    backup_button.pack()
    backup_button.wait_variable(backup_wait_var)
    server_backup_window.destroy()
    backup_version = backup_version_variable.get()
    backup_name = backup_name_variable.get()
    overwrite_backup_name_exists = overwrite_backup_name_exists_variable.get()
    logging.info("Version Selected In create_server_backup(): " + str(backup_version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\"):
        logging.error(f"Server version does not exist in create_server_backup(): {backup_version}")
        showerror(title="Error", message="The server version you are trying to backup does not exist!")
        return
    else:
        pass
    if not backup_name or backup_name == "" or backup_name.isspace():
        showerror(title="Error", message="Invalid Name!")
        logging.error("Invalid Name Selected In create_server_backup()")
        return
    else:
        pass
    logging.info("Name Selected In create_server_backup(): " + backup_name)
    if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\"):
        logging.error("Backup With Same Name Already Exists")
        if overwrite_backup_name_exists == "True":
            replace_ask = True
        else:
            replace_ask = askyesno(title="Create Server Backup",
                                   message="A backup with the same name already exists! Do you want to replace it?")
            pass
        if replace_ask:
            logging.info("User Selected To Replace Backup")
            logging.info("Removing Old Backup")
            rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            logging.info("Deleted Old Backup")
            logging.info("Creating New Backup")
            if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"):
                logging.info(f"Creating new backup direcotry for version {backup_version}")
                os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\")
                pass
            else:
                pass
                logging.info("Performing Server Backup")
                logging.info(
                    "Copying from " + f"{cwd}\\ServerFiles-{backup_version}\\" + " to " + f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
                copytree(f"{cwd}\\ServerFiles-{backup_version}\\",
                         f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
                logging.info("Backup Successful")
                showinfo(title="Backup Successful", message="Backup Successful!")
                return
        else:
            logging.info("User Selected Not To Replace Backup")
            showinfo(title="Minecraft Server Backup", message="A backup was NOT created!")
            return
    else:
        try:
            if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"):
                logging.info(f"Creating new backup direcotry for version {backup_version}")
                os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\")
                pass
            else:
                pass
            logging.info("Performing Server Backup")
            logging.info(
                "Copying from " + f"{cwd}\\ServerFiles-{backup_version}\\" + " to " + f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            copytree(f"{cwd}\\ServerFiles-{backup_version}\\",
                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            logging.info("Backup Successful")
            showinfo(title="Backup Successful", message="Backup Successful!")
            return
        except Exception as e:
            logging.error("Error In create_server_backup(): " + str(e))
            showerror(title="Backup Error", message=f"Error while performing backup: {e}")
            return


def get_all_backups(version):
    logging.info("Getting All Backups For Version: " + version)
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\"):
        logging.info(f"No Backups Found For Version: {version}")
        return []
    else:
        pass
    backups = []
    for backup in os.listdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\"):
        backups.append(backup)
    logging.info("Backups Found: " + str(backups))
    return backups


def get_all_backup_versions():
    logging.info("Getting All Backup Versions")
    backup_versions = []
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\"):
        logging.info("No Backups Found")
        return backup_versions
    else:
        for version in os.listdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\"):
            if version == "Data":
                pass
            else:
                backup_versions.append(version)
                pass
            pass
        logging.info("Backup Versions Found: " + str(backup_versions))
        return backup_versions


def restore_server_backup():
    restore_backup_window = Toplevel(root)
    restore_backup_window.title("Restore Minecraft Server Backup")
    restore_backup_window.geometry("300x300")
    backup_version_label = ttk.Label(restore_backup_window, text="Select Server Version To Restore")
    backup_version_label.pack()
    backup_version_variable = StringVar()
    backup_version_check = ttk.Combobox(restore_backup_window, textvariable=backup_version_variable,
                                        values=get_server_versions())
    backup_version_check.pack()
    while True:
        version_wait_var = IntVar()
        restore_backup_window.after(100, lambda: version_wait_var.set(1))
        restore_backup_window.wait_variable(version_wait_var)
        backup_version = backup_version_variable.get()
        if backup_version not in get_server_versions():
            pass
        else:
            break
    backup_version_check.config(state="disabled")
    backup_name_label = ttk.Label(restore_backup_window, text="Select Backup Name")
    backup_name_label.pack()
    backup_name_variable = StringVar()
    backup_name_check = ttk.Combobox(restore_backup_window, textvariable=backup_name_variable,
                                     values=get_all_backups(backup_version))
    backup_name_check.pack()
    backup_current_server_variable = StringVar()
    backup_current_server_variable.set("False")
    backup_current_server_check = ttk.Checkbutton(restore_backup_window, text="Backup Current Server",
                                                  variable=backup_current_server_variable, onvalue="True",
                                                  offvalue="False")
    backup_current_server_check.pack()
    restore_wait_var = IntVar()
    restore_button = ttk.Button(restore_backup_window, text="Restore Server Backup",
                                command=lambda: restore_wait_var.set(1), style="Accent.TButton")
    restore_button.pack()
    restore_button.wait_variable(restore_wait_var)
    restore_backup_window.destroy()
    backup_name = backup_name_variable.get()
    backup_current_server = backup_current_server_variable.get()
    logging.info("Version Selected In restore_server_backup(): " + str(backup_version))
    backup_path = f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}"
    if backup_version not in backup_path:
        showerror(title="Restore Server Backup", message="Those files are unusable in this server version!")
        logging.error(
            "Those files are unusable in this server version! Backup Version: " + backup_version + " Backup Path: " + backup_path)
        return
    else:
        pass
    if not os.path.exists(f"{backup_path}\\server.jar"):
        logging.error("server.jar Not Found In restore_server_backup()")
        showerror(title="Backup Restore Error", message="This backup is invalid and wont work!")
        logging.error("Invalid Backup In restore_server_backup()")
        return
    else:
        confirm_restore = True
        if confirm_restore:
            if os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\server.jar"):
                logging.info("Current Server Files Found")
                if backup_current_server == "True":
                    backup_server = True
                    pass
                else:
                    backup_server = False
                    pass
                if backup_server:
                    logging.info("Performing New Server Backup in restore_server_backup()")
                    backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
                    if not backup_name:
                        showerror(title="Error", message="Invalid Name!")
                        return
                    else:
                        pass
                    if os.path.exists(
                            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\"):
                        showerror(title="Backup Error",
                                  message="Backup with the same name already exists! Please try again!")
                        return
                    else:
                        try:
                            copytree(f"{cwd}\\ServerFiles-{backup_version}\\",
                                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
                            showinfo(title="Backup Successful", message="Backup Successful!")
                            pass
                        except Exception as e:
                            showerror(title="Backup Error", message=f"Error while performing backup: {e}")
                            return
                        pass
                else:
                    showwarning(title="Restore Server Backup", message="You have chosen not to backup the current "
                                                                       "server! Current server data will be "
                                                                       "overwritten!")
                    logging.warning("User Chose Not To Backup Current Server In restore_server_backup()")
                    pass
                pass
            else:
                pass
            try:
                logging.info("Performing Server Restore")
                rmtree(f"{cwd}\\ServerFiles-{backup_version}\\")
                logging.info("Removed Old Server Files")
                copytree(f"{backup_path}\\", f"{cwd}\\ServerFiles-{backup_version}\\")
                logging.info("Copied Backup Files")
                showinfo(title="Restore Successful", message="Restore Successful!")
                logging.info("Restore Successful")
                return
            except Exception as e:
                showerror(title="Backup Restore Error", message=f"Error while restoring backup: {e}")
                logging.error("Error In restore_server_backup(): " + str(e))
                return
        else:
            showinfo(title="Restore Cancelled", message="Restore Cancelled!")
            logging.info("Server Restore Cancelled")
            return


def reset_server():
    reset_server_window = Toplevel(root)
    reset_server_window.title("Reset Server")
    reset_server_window.geometry("250x250")
    reset_server_version_variable = StringVar()
    reset_server_version_label = ttk.Label(reset_server_window, text="Select Server Version To Reset")
    reset_server_version_label.pack(padx=10, pady=5)
    reset_server_version_check = ttk.Combobox(reset_server_window, textvariable=reset_server_version_variable,
                                              values=get_server_versions())
    reset_server_version_check.pack(padx=10, pady=5)
    backup_before_reset_var = StringVar()
    backup_before_reset_var.set("False")
    backup_before_reset_check = ttk.Checkbutton(reset_server_window, text="Backup Server Before Reset",
                                                variable=backup_before_reset_var, onvalue="True", offvalue="False")
    backup_before_reset_check.pack(padx=10, pady=5)
    reset_server_wait_var = IntVar()
    reset_server_button = ttk.Button(reset_server_window, text="Reset Server",
                                     command=lambda: reset_server_wait_var.set(1), style="Accent.TButton")
    reset_server_button.pack(pady=5, padx=10)
    reset_server_window.wait_variable(reset_server_wait_var)
    reset_server_window.destroy()
    reset_version = reset_server_version_variable.get()
    if backup_before_reset_var.get() == "True":
        backup_current_server = True
        pass
    else:
        backup_current_server = False
        pass
    if backup_current_server:
        backup_name = askstring(title="Create Server Backup", prompt="Enter a name for new server backup!")
        pass
    else:
        pass
    logging.info("Version Selected In reset_server(): " + str(reset_version))
    if os.path.exists(f"{cwd}\\ServerFiles-{reset_version}\\"):
        if backup_current_server:
            logging.warning("Performing Server Backup Before Resetting")
            if not backup_name or backup_name == "" or backup_name.isspace() or backup_name is None:
                showerror(title="Error", message="Invalid Backup Name! Cancelling server reset!")
                return
            else:
                pass
            if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\"):
                os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\")
                pass
            else:
                pass
            if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\{backup_name}\\"):
                showerror(title="Backup Error",
                          message="Backup with the same name already exists! Please try again!")
                return
            else:
                try:
                    copytree(f"{cwd}\\ServerFiles-{reset_version}\\",
                             f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\{backup_name}\\")
                    logging.info("Server Backup Successful")
                    showinfo(title="Backup Successful", message="Backup Successful!")
                    pass
                except Exception as e:
                    showerror(title="Backup Error", message=f"Error while performing backup: {e}")
                    logging.error("Error when performing backup: " + str(e))
                    return
                pass
            pass
        else:
            logging.warning("User Has Chosen Not To Backup Current Server")
            pass
        try:
            reset_confirm = askyesno(title="Reset Server",
                                     message="Are you sure you want to reset the server? This will remove all server files from your device!")
            if reset_confirm:
                logging.warning("Performing Server Reset")
                logging.info(f"Removing ExclusionPath for ServerFiles-{reset_version}")
                subprocess.Popen(["powershell.exe", "-Command", "Remove-MpPreference", "-ExclusionPath",
                          f"'{cwd}\\ServerFiles-{reset_version}\\'"], startupinfo=info)
                logging.info("Removed ExclusionPath")
                rmtree(f"{cwd}\\ServerFiles-{reset_version}\\")
                logging.info(f"Removed ServerFiles-{reset_version} directory")
                showinfo("Server Reset", "Server Reset Successful!")
                return
            else:
                showinfo("Server Reset", "Server Reset Cancelled!")
                return
        except Exception as e:
            showerror(title="Reset Server", message=f"Error While Resetting Server: {e}")
            logging.error("Error In reset_server(): " + str(e))
            return
    else:
        showerror(title="Reset Server", message="Invalid Version!")
        logging.error("Invalid Version Selected In reset_server()")
        return


def reset_server_event(event):
    reset_server_window = Toplevel(root)
    reset_server_window.title("Reset Server")
    reset_server_window.geometry("250x250")
    reset_server_version_variable = StringVar()
    reset_server_version_label = ttk.Label(reset_server_window, text="Select Server Version To Reset")
    reset_server_version_label.pack(padx=10, pady=5)
    reset_server_version_check = ttk.Combobox(reset_server_window, textvariable=reset_server_version_variable,
                                              values=get_server_versions())
    reset_server_version_check.pack(padx=10, pady=5)
    backup_before_reset_var = StringVar()
    backup_before_reset_var.set("False")
    backup_before_reset_check = ttk.Checkbutton(reset_server_window, text="Backup Server Before Reset",
                                                variable=backup_before_reset_var, onvalue="True", offvalue="False")
    backup_before_reset_check.pack(padx=10, pady=5)
    reset_server_wait_var = IntVar()
    reset_server_button = ttk.Button(reset_server_window, text="Reset Server",
                                     command=lambda: reset_server_wait_var.set(1), style="Accent.TButton")
    reset_server_button.pack(pady=5, padx=10)
    reset_server_window.wait_variable(reset_server_wait_var)
    reset_server_window.destroy()
    reset_version = reset_server_version_variable.get()
    if backup_before_reset_var.get() == "True":
        backup_current_server = True
        pass
    else:
        backup_current_server = False
        pass
    if backup_current_server:
        backup_name = askstring(title="Create Server Backup", prompt="Enter a name for new server backup!")
        pass
    else:
        pass
    logging.info("Version Selected In reset_server(): " + str(reset_version))
    if os.path.exists(f"{cwd}\\ServerFiles-{reset_version}\\"):
        if backup_current_server:
            logging.warning("Performing Server Backup Before Resetting")
            if not backup_name or backup_name == "" or backup_name.isspace() or backup_name is None:
                showerror(title="Error", message="Invalid Backup Name! Cancelling server reset!")
                return
            else:
                pass
            if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\"):
                os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\")
                pass
            else:
                pass
            if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\{backup_name}\\"):
                showerror(title="Backup Error",
                          message="Backup with the same name already exists! Please try again!")
                return
            else:
                try:
                    copytree(f"{cwd}\\ServerFiles-{reset_version}\\",
                             f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\{backup_name}\\")
                    logging.info("Server Backup Successful")
                    showinfo(title="Backup Successful", message="Backup Successful!")
                    pass
                except Exception as e:
                    showerror(title="Backup Error", message=f"Error while performing backup: {e}")
                    logging.error("Error when performing backup: " + str(e))
                    return
                pass
            pass
        else:
            logging.warning("User Has Chosen Not To Backup Current Server")
            pass
        try:
            reset_confirm = askyesno(title="Reset Server",
                                     message="Are you sure you want to reset the server? This will remove all server files from your device!")
            if reset_confirm:
                logging.warning("Performing Server Reset")
                logging.info(f"Removing ExclusionPath for ServerFiles-{reset_version}")
                subprocess.Popen(["powershell.exe", "-Command", "Remove-MpPreference", "-ExclusionPath",
                          f"'{cwd}\\ServerFiles-{reset_version}\\'"], startupinfo=info)
                logging.info("Removed ExclusionPath")
                rmtree(f"{cwd}\\ServerFiles-{reset_version}\\")
                logging.info(f"Removed ServerFiles-{reset_version} directory")
                showinfo("Server Reset", "Server Reset Successful!")
                return
            else:
                showinfo("Server Reset", "Server Reset Cancelled!")
                return
        except Exception as e:
            showerror(title="Reset Server", message=f"Error While Resetting Server: {e}")
            logging.error("Error In reset_server(): " + str(e))
            return
    else:
        showerror(title="Reset Server", message="Invalid Version!")
        logging.error("Invalid Version Selected In reset_server()")
        return


def folder_selection(title_text: str):
    selected_folder = askdirectory(title=title_text)
    logging.info("Folder Selected In folder_selection(): " + str(selected_folder))
    return str(selected_folder)


def inject_custom_map():
    inject_custom_map_window = Toplevel(root)
    inject_custom_map_window.title("Inject Custom Map")
    inject_custom_map_window.geometry("325x325")
    inject_custom_map_version_variable = StringVar()
    inject_custom_map_version_label = ttk.Label(inject_custom_map_window, text="Select Server Version To Inject Map")
    inject_custom_map_version_label.grid(row=0, column=0, columnspan=2, pady=5)
    inject_custom_map_version_check = ttk.Combobox(inject_custom_map_window,
                                                   textvariable=inject_custom_map_version_variable,
                                                   values=get_server_versions())
    inject_custom_map_version_check.grid(row=1, column=0, columnspan=2, pady=5)
    folder_select_label = ttk.Label(inject_custom_map_window, text="Select Map Folder")
    folder_select_label.grid(row=2, column=0, columnspan=2, pady=5)
    selected_folder_variable = StringVar()
    selected_folder_entry = ttk.Entry(inject_custom_map_window, textvariable=selected_folder_variable, width=40,
                                      state="readonly")
    selected_folder_entry.grid(row=3, column=0, columnspan=1, pady=5, padx=5)
    folder_select_button = ttk.Button(inject_custom_map_window, text="Select Map Folder",
                                      command=lambda: selected_folder_variable.set(
                                          folder_selection("Select Map Folder")), width=25)
    folder_select_button.grid(row=4, column=0, columnspan=1, pady=5)
    backup_before_inject_var = StringVar()
    backup_before_inject_var.set("False")
    backup_before_inject_check = ttk.Checkbutton(inject_custom_map_window, text="Backup Current Server",
                                                 variable=backup_before_inject_var, onvalue="True", offvalue="False")
    backup_before_inject_check.grid(row=5, column=0, columnspan=2, pady=5)
    inject_custom_map_wait_var = IntVar()
    inject_custom_map_button = ttk.Button(inject_custom_map_window, text="Inject Map",
                                          command=lambda: inject_custom_map_wait_var.set(1), width=25,
                                          style="Accent.TButton")
    inject_custom_map_button.grid(row=6, column=0, columnspan=2, pady=5)
    inject_custom_map_window.wait_variable(inject_custom_map_wait_var)
    inject_custom_map_window.destroy()
    version = inject_custom_map_version_variable.get()
    custom_map = selected_folder_variable.get()
    backup_before_inject = backup_before_inject_var.get()
    logging.info("Version Selected In inject_custom_map(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version In inject_custom_map()")
        return
    else:
        pass
    if custom_map is None:
        showerror(title="Select Custom Map Folder", message="No Folder Selected!")
        logging.error("No Folder Selected In inject_custom_map()")
        return
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\ops.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-players.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-ips.json\\"):
            logging.warning("Current Server Files Detected")
            if backup_before_inject == "True":
                backup_current_server = True
                pass
            else:
                backup_current_server = False
                pass
            if backup_current_server:
                logging.warning("Performing Server Backup Before Injecting Custom Map")
                backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
                if not backup_name:
                    showerror(title="Error", message="Invalid Name!")
                else:
                    pass
                if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\"):
                    os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\")
                    pass
                else:
                    pass
                if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
                    showerror(title="Backup Error",
                              message="Backup with the same name already exists! Please try again!")
                    logging.error("Backup with the same name already exists In inject_custom_map()")
                    return
                else:
                    try:
                        copytree(f"{cwd}\\ServerFiles-{version}\\",
                                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
                        logging.info("Server Backup Successful")
                        showinfo(title="Backup Successful", message="Backup Successful!")
                        pass
                    except Exception as e:
                        showerror(title="Backup Error", message=f"Error while performing backup: {e}")
                        logging.error("Error In inject_custom_map(): " + str(e))
                        return
                    pass
                pass
            else:
                showwarning(title="Server Backup", message="You have chosen not to backup the current "
                                                           "server! Current server data will be "
                                                           "overwritten!")
                logging.warning("User Has Chosen Not To Backup Current Server")
                pass
            pass
        else:
            pass
        try:
            logging.warning("Performing Custom Map Injection")
            server_prop = open(f"{cwd}\\ServerFiles-{version}\\server.properties", "r")
            if "level-name" in str(server_prop.read()):
                p = Properties()
                p.load(open(f"{cwd}\\ServerFiles-{version}\\server.properties", "rb"))
                level_name = p.get("level-name").data
                pass
            else:
                level_name = "world"
                pass
            server_prop.close()
            rmtree(f"{cwd}\\ServerFiles-{version}\\{level_name}\\")
            copytree(f"{custom_map}\\", f"{cwd}\\ServerFiles-{version}\\{level_name}\\")
            showinfo(title="Custom Map", message="Custom Map Successfully Injected!")
            logging.info("Custom Map Injection Successful")
            pass
        except Exception as e:
            showerror(title="Custom Map", message=f"Error while injecting custom map: {e}")
            logging.error("Error In inject_custom_map(): " + str(e))
            pass
        return


def reset_overworld(version, backup, window):
    window.destroy()
    if backup == "True":
        backup_ask = True
        pass
    else:
        backup = False
        pass
    logging.info("Version Selected In reset_overworld(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Entered")
        return
    else:
        pass
    if backup_ask:
        logging.info("User Has Chosen To Backup Server Before Resetting Dimension")
        backup_name = askstring("Backup", "Please enter a name for your backup!")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
            showerror(title="Backup", message="Backup with that name already exists!")
            logging.error("Backup with that name already exists In reset_overworld()")
            return
        else:
            pass
        logging.info("Performing Backup Before Resetting Overworld")
        copytree(f"{cwd}\\ServerFiles-{version}\\",
                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
        showinfo("Backup", "Backup Complete!")
        logging.info("Backup Complete In reset_overworld()")
        pass
    else:
        pass
    reset_ask = askyesno("Reset", "Are you sure you want to reset the dimension?")
    if reset_ask:
        logging.info("User Has Chosen To Reset Dimension")
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\world\\region\\"):
            pass
        else:
            showerror(title="Dimension Reset", message="The overworld files do not exist!")
            logging.error("The overworld files do not exist In reset_overworld()")
            return
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\region\\")
            showinfo(title="Dimension Reset", message="Overworld Successfully Reset!")
            logging.info("Overworld Successfully Reset In reset_overworld()")
            return
        except Exception as e:
            showerror(title="Dimension Reset", message=f"Error while resetting dimension: {e}")
            logging.error("Error In reset_overworld(): " + str(e))
            return
    else:
        showinfo("Dimension Reset", "Dimension Reset Cancelled!")
        logging.info("Dimension Reset Cancelled In reset_overworld()")
        return


def reset_nether(version, backup_ask, window):
    window.destroy()
    if backup_ask == "True":
        backup_ask = True
        pass
    else:
        backup_ask = False
        pass
    logging.info("Version Selected In reset_nether(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Entered")
        return
    else:
        pass
    if backup_ask:
        backup_name = askstring("Backup", "Please enter a name for your backup!")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
            showerror(title="Backup", message="Backup with that name already exists!")
            logging.error("Backup with that name already exists In reset_nether()")
            return
        else:
            pass
        logging.info("Performing Backup Before Resetting Nether")
        copytree(f"{cwd}\\ServerFiles-{version}\\",
                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
        showinfo("Backup", "Backup Complete!")
        logging.info("Backup Complete In reset_nether()")
        pass
    else:
        pass
    reset_ask = askyesno("Reset", "Are you sure you want to reset the dimension?")
    if reset_ask:
        logging.info("User Has Chosen To Reset Dimension")
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\world\\DIM-1\\region\\"):
            pass
        else:
            showerror(title="Dimension Reset", message="The nether files do not exist!")
            logging.error("Nether Files Do Not Exist In reset_nether()")
            return
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM-1\\region\\")
            showinfo(title="Dimension Reset", message="Nether Successfully Reset!")
            logging.info("Nether Successfully Reset In reset_nether()")
            return
        except Exception as e:
            showerror(title="Dimension Reset", message=f"Error while resetting dimension: {e}")
            logging.error("Error In reset_nether(): " + str(e))
            return
    else:
        showinfo("Dimension Reset", "Dimension Reset Cancelled!")
        logging.info("Dimension Reset Cancelled In reset_nether()")
        return


def reset_end(version, backup_ask, window):
    window.destroy()
    if backup_ask == "True":
        backup_ask = True
        pass
    else:
        backup_ask = False
        pass
    logging.info("Version Selected In reset_end(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Entered")
        return
    else:
        pass
    if backup_ask:
        backup_name = askstring("Backup", "Please enter a name for your backup!")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
            showerror(title="Backup", message="Backup with that name already exists!")
            logging.error("Backup with that name already exists In reset_end()")
            return
        else:
            pass
        logging.info("Performing Backup Before Resetting End")
        copytree(f"{cwd}\\ServerFiles-{version}\\",
                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
        showinfo("Backup", "Backup Complete!")
        logging.info("Backup Complete In reset_end()")
        pass
    else:
        pass
    reset_ask = askyesno("Reset", "Are you sure you want to reset the dimension?")
    if reset_ask:
        logging.info("User Has Chosen To Reset Dimension")
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\world\\DIM1\\region\\"):
            pass
        else:
            showerror(title="Dimension Reset", message="The end files do not exist!")
            logging.error("End Files Do Not Exist In reset_end()")
            return
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM1\\region\\")
            showinfo(title="Dimension Reset", message="End Successfully Reset!")
            logging.info("End Successfully Reset In reset_end()")
            return
        except Exception as e:
            showerror(title="Dimension Reset", message=f"Error while resetting dimension: {e}")
            logging.error("Error In reset_end(): " + str(e))
            return
    else:
        showinfo("Dimension Reset", "Dimension Reset Cancelled!")
        logging.info("Dimension Reset Cancelled In reset_end()")
        return


def reset_dimension_main():
    logging.info("reset_dimension_main() Called")
    dim_reset_window = Toplevel(root)
    dim_reset_window.title("Reset Dimension")
    dim_reset_window.geometry("300x300")
    version_selection_var = StringVar()
    version_selection_label = Label(dim_reset_window, text="Select Version To Reset Dimension")
    version_selection_label.pack(padx=10, pady=5)
    version_selection_menu = ttk.Combobox(dim_reset_window, textvariable=version_selection_var,
                                          values=get_server_versions())
    version_selection_menu.pack(padx=10, pady=5)
    backup_before_reset_var = StringVar()
    backup_before_reset_var.set("False")
    backup_before_reset_check = ttk.Checkbutton(dim_reset_window, text="Backup Before Resetting Dimension",
                                                variable=backup_before_reset_var, onvalue="True", offvalue="False")
    backup_before_reset_check.pack(padx=10, pady=5)
    dim_reset_label = ttk.Label(dim_reset_window, text="Select The Dimension To Reset")
    overworld_button = ttk.Button(dim_reset_window, text="Overworld",
                                  command=lambda: reset_overworld(version=version_selection_var.get(),
                                                                  backup=backup_before_reset_var.get(),
                                                                  window=dim_reset_window), width="25")
    nether_button = ttk.Button(dim_reset_window, text="Nether",
                               command=lambda: reset_nether(version=version_selection_var.get(),
                                                            backup=backup_before_reset_var.get(),
                                                            window=dim_reset_window), width="25")
    end_button = ttk.Button(dim_reset_window, text="End", command=lambda: reset_end(version=version_selection_var.get(),
                                                                                    backup=backup_before_reset_var.get(),
                                                                                    window=dim_reset_window),
                            width="25")
    dim_reset_label.pack(padx=10, pady=5)
    overworld_button.pack(padx=10, pady=5)
    nether_button.pack(padx=10, pady=5)
    end_button.pack(padx=10, pady=5)


def change_server_properties():
    logging.info("change_server_properties() Called")
    properties_window = Toplevel(root)
    properties_window.title("Change Server Properties")
    properties_window.geometry("300x300")
    properties_version_var = StringVar()
    properties_version_label = Label(properties_window, text="Select Version To Change Properties")
    properties_version_label.pack(padx=10, pady=5)
    properties_version_menu = ttk.Combobox(properties_window, textvariable=properties_version_var,
                                           values=get_server_versions())
    properties_version_menu.pack(padx=10, pady=5)
    try:
        properties_version_menu.current(0)
        pass
    except:
        pass
    backup_before_launching_var = StringVar()
    backup_before_launching_var.set("False")
    backup_before_launching_check = ttk.Checkbutton(properties_window, text="Backup Before Launching Editor",
                                                    variable=backup_before_launching_var, onvalue="True",
                                                    offvalue="False")
    backup_before_launching_check.pack(padx=10, pady=5)
    properties_wait_var = IntVar()
    properties_button = ttk.Button(properties_window, text="Change Server Properties",
                                   command=lambda: properties_wait_var.set(1), style="Accent.TButton")
    properties_button.pack(padx=10, pady=5)
    properties_window.wait_variable(properties_wait_var)
    properties_window.destroy()
    properties_version = properties_version_var.get()
    backup_before_launching = backup_before_launching_var.get()
    if os.path.exists(f"{cwd}\\ServerFiles-{properties_version}\\server.properties"):
        pass
    else:
        showerror(title="Change Server Properties", message="Server with this version does not exist!")
        logging.error("Server with this version does not exist In change_server_properties()")
        return
    if backup_before_launching == "True":
        logging.info("User Has Chosen To Backup Before Launching Properties Editor")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{properties_version}\\"):
            pass
        else:
            showerror(title="Backup", message="No backups were found for that server version!")
            logging.error("No Backups Were Found In change_server_properties()")
            return
        backup_name = askstring("Backup", "Enter a name for the backup:")
        if backup_name is None:
            showinfo("Backup", "Backup Cancelled!")
            logging.info("Backup Cancelled In change_server_properties()")
            return
        else:
            pass
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{properties_version}\\{backup_name}"):
            showerror(title="Backup", message="A backup with that name already exists!")
            logging.error("A Backup With That Name Already Exists In change_server_properties()")
            return
        else:
            pass
        try:
            copytree(f"{cwd}\\ServerFiles-{properties_version}\\",
                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{properties_version}\\{backup_name}\\")
            logging.info("Backup Successfully Created In change_server_properties()")
            pass
        except Exception as e:
            showerror(title="Backup", message=f"Error while creating backup: {e}")
            logging.error("Error In change_server_properties(): " + str(e))
            return
        pass
    else:
        logging.info("User Has Chosen Not To Backup Server Before Launching Properties Editor")
        pass
    try:
        os.startfile(f"{cwd}\\ServerFiles-{properties_version}\\server.properties")
        logging.info(f"Launching {cwd}\\ServerFiles-{properties_version}\\server.properties")
        return
    except Exception as e:
        logging.error(f"Error launching server properties: {e}")
        showerror(title="Error", message=f"Error Opening server.properties: {e}")
        return


def import_external_server():
    import_external_server_window = Toplevel(root)
    import_external_server_window.title("Import External Server")
    import_external_server_window.geometry("300x300")
    import_version_selection_var = StringVar()
    version_selection_label = ttk.Label(import_external_server_window, text="Select Version To Import External Server")
    version_selection_label.pack(padx=10, pady=5)
    version_selection_menu = ttk.Combobox(import_external_server_window, textvariable=import_version_selection_var,
                                          values=get_server_versions())
    version_selection_menu.pack(padx=10, pady=5)
    try:
        version_selection_menu.current(0)
        pass
    except Exception as e:
        pass
    folder_selection_label = ttk.Label(import_external_server_window, text="Select The Folder To Import")
    folder_selection_label.pack(padx=10, pady=5)
    selected_folder_variable = StringVar()
    selected_folder_variable.set("Select Folder With Button Below")
    selected_folder_entry = ttk.Entry(import_external_server_window, textvariable=selected_folder_variable, width=40,
                                      state="readonly")
    selected_folder_entry.pack(padx=10, pady=5)
    folder_select_button = ttk.Button(import_external_server_window, text="Select Server Folder",
                                      command=lambda: selected_folder_variable.set(
                                          folder_selection("Select Server Folder")), width=25)
    folder_select_button.pack(padx=10, pady=5)
    backup_before_import_var = StringVar()
    backup_before_import_var.set("False")
    backup_before_import_check = ttk.Checkbutton(import_external_server_window, text="Backup Current Server",
                                                 variable=backup_before_import_var, onvalue="True", offvalue="False")
    backup_before_import_check.pack(padx=10, pady=5)
    import_external_server_wait_var = IntVar()
    import_external_server_button = ttk.Button(import_external_server_window, text="Import External Server",
                                               command=lambda: import_external_server_wait_var.set(1),
                                               style="Accent.TButton")
    import_external_server_button.pack(padx=10, pady=5)
    import_external_server_window.wait_variable(import_external_server_wait_var)
    import_external_server_window.destroy()
    version = import_version_selection_var.get()
    import_files = selected_folder_variable.get()
    if backup_before_import_var == "True":
        backup_current_server = True
        pass
    else:
        backup_current_server = True
        pass
    if not os.path.exists(f"{import_files}\\world\\") or not os.path.exists(
            f"{import_files}\\server.properties") or not os.path.exists(
        f"{import_files}\\eula.txt") or not os.path.exists(f"{import_files}\\ops.json") or not os.path.exists(
        f"{import_files}\\banned-ips.json") or not os.path.exists(
        f"{import_files}\\banned-players.json") or not os.path.exists(
        f"{import_files}\\whitelist.json"):
        showerror(title="Error", message="Invalid Folder Selected!")
        logging.error("Invalid Folder Selected!")
        return
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\ops.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-players.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-ips.json\\"):
            if backup_current_server:
                logging.info("User opted to backup server before importing external server")
                backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
                if not backup_name:
                    showerror(title="Error", message="Invalid Name!")
                    logging.error("Invalid backup name")
                    return
                else:
                    pass
                if not os.path.exist(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\"):
                    os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\")
                    pass
                else:
                    pass
                if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
                    showerror(title="Backup Error",
                              message="Backup with the same name already exists! Please try again!")
                    logging.error("Backup with the same name already exists")
                    return
                else:
                    try:
                        copytree(f"{cwd}\\ServerFiles-{version}\\",
                                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
                        showinfo(title="Backup Successful", message="Backup Successful!")
                        logging.info("Backup successful before importing external server")
                        pass
                    except Exception as e:
                        showerror(title="Backup Error", message=f"Error while performing backup: {e}")
                        logging.error(f"Error while performing backup: {e}")
                        return
                    pass
            else:
                showwarning(title="Restore Server Backup", message="You have chosen not to backup the current "
                                                                   "server! Current server data will be "
                                                                   "overwritten!")
                logging.warning("User opted to not backup server before importing external server")
                pass
            pass
        else:
            pass
        try:
            logging.warning("Importing external server")
            if os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
                rmtree(f"{cwd}\\ServerFiles-{version}\\")
                pass
            else:
                pass
            copytree(f"{import_files}\\", f"{cwd}\\ServerFiles-{version}\\")
            showinfo(title="Import External Server", message="Server Successfully Imported!")
            logging.info("Server successfully imported")
            return
        except Exception as e:
            showerror(title="Import Error", message=f"Error while performing import: {e}")
            logging.error(f"Error while performing import: {e}")
            return


def manage_server_backups():
    manage_server_backups_window = Toplevel(root)
    manage_server_backups_window.title("Manage Server Backups")
    manage_server_backups_window.geometry("350x275")
    manage_server_backups_text = ttk.Label(manage_server_backups_window,
                                           text="Select a version, backup, intent, then press continue!")
    manage_server_backups_text.pack(padx=10, pady=5)
    server_version_entry = ttk.Combobox(manage_server_backups_window, values=get_all_backup_versions(), width=40)
    server_version_entry.pack(padx=10, pady=5)
    while True:
        version_wait_var = IntVar()
        manage_server_backups_window.after(100, lambda: version_wait_var.set(1))
        manage_server_backups_window.wait_variable(version_wait_var)
        backup_version = server_version_entry.get()
        if backup_version not in get_server_versions():
            pass
        else:
            break
    server_version_entry.config(state="disabled")
    backup_entry = ttk.Combobox(manage_server_backups_window, values=get_all_backups(backup_version), width=40)
    backup_entry.pack(padx=10, pady=5)
    backup_intent_var = StringVar()
    backup_rename_radio = ttk.Radiobutton(manage_server_backups_window, text="Rename", variable=backup_intent_var,
                                          value="Rename")
    backup_rename_radio.pack(padx=10, pady=5)
    backup_delete_radio = ttk.Radiobutton(manage_server_backups_window, text="Remove", variable=backup_intent_var,
                                          value="Remove")
    backup_delete_radio.pack(padx=10, pady=5)
    backup_export_radio = ttk.Radiobutton(manage_server_backups_window, text="Export", variable=backup_intent_var,
                                          value="Export")
    backup_export_radio.pack(padx=10, pady=5)
    manage_backup_wait_var = IntVar()
    continue_button = ttk.Button(manage_server_backups_window, text="Continue",
                                 command=lambda: manage_backup_wait_var.set(1), style="Accent.TButton")
    continue_button.pack(padx=10, pady=5)
    manage_server_backups_window.wait_variable(manage_backup_wait_var)
    backup_intent = backup_intent_var.get()
    backup_name = backup_entry.get()
    manage_server_backups_window.destroy()
    if backup_intent == "Rename":
        new_backup_name = askstring(title="Rename Backup", prompt="Enter the new name of the backup!")
        if not new_backup_name:
            showerror(title="Error", message="Invalid Name!")
            logging.error("Invalid backup name")
            return
        else:
            pass
        logging.info("User opted to rename server backup")
        if "AutomaticBackup-" in backup_name:
            os.rename(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\",
                      f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{new_backup_name}\\")
            os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{backup_version}.txt")
            showinfo(title="Rename Backup", message="Backup Successfully Renamed!")
            logging.info("Auto Backup renamed")
            return
        else:
            pass
        if not new_backup_name:
            showerror(title="Error", message="Invalid Name!")
            logging.error("Invalid backup name")
            return
        else:
            pass
        if os.path.exists(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{new_backup_name}\\"):
            showerror(title="Backup Error",
                      message="Backup with the same name already exists! Please try again!")
            logging.error("Backup with the same name already exists")
            return
        else:
            try:
                os.rename(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\",
                          f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{new_backup_name}\\")
                showinfo(title="Backup Renamed", message="Backup Successfully Renamed!")
                logging.info("Backup successfully renamed")
                return
            except Exception as e:
                showerror(title="Backup Error", message=f"Error while renaming the backup: {e}")
                logging.error(f"Error while performing rename: {e}")
                return
    elif backup_intent == "Remove":
        logging.info("User opted to remove server backup")
        if "AutomaticBackup-" in backup_name:
            confirm_auto_backup_removal = askyesno(title="Remove Server Backup",
                                                   message="Are you sure you want to remove the automatic backup: " + backup_name.replace("AutomaticBackup-", "") + "?")
            if confirm_auto_backup_removal:
                try:
                    rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
                    os.remove(
                        f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{backup_version}.txt")
                    showinfo(title="Backup Removed", message="Backup Successfully Removed!")
                    logging.info("Automatic backup successfully removed")
                    return
                except Exception as e:
                    showerror(title="Backup Error", message=f"Error while removing the backup: {e}")
                    logging.error(f"Error while performing remove: {e}")
                    return
            else:
                showinfo(title="Backup Removal", message="Backup Removal Cancelled!")
                logging.info("User cancelled automatic backup removal")
                return
        else:
            confirm_backup_removal = askyesno(title="Remove Server Backup",
                                              message="Are you sure you want to remove the backup: " + backup_name + "?")
            if confirm_backup_removal:
                try:
                    rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
                    showinfo(title="Backup Removal", message="Backup Successfully Removed!")
                    logging.info("Backup successfully removed")
                    return
                except Exception as e:
                    showerror(title="Backup Error", message=f"Error while removing the backup: {e}")
                    logging.error(f"Error while performing remove: {e}")
                    return
            else:
                showinfo(title="Backup Removal", message="Backup Removal Cancelled!")
                logging.info("User cancelled backup removal")
                return
    elif backup_intent == "Export":
        logging.info("User opted to export server backup")
        export_server_backup(backup_version, backup_name)
        return
    else:
        showerror(title="Manage Server Backups", message="You did not select an intent! Nothing will be done!")
        return


def export_server():
    export_server_window = Toplevel(root)
    export_server_window.title("Export Server")
    export_server_window.geometry("300x300")
    export_server_label = ttk.Label(export_server_window,
                                    text="Select the version you would like to export\nand set the destination!")
    export_server_label.pack(padx=10, pady=5)
    export_version_var = StringVar()
    export_server_version_selection = ttk.Combobox(export_server_window, values=get_server_versions(), textvariable=export_version_var)
    export_version_var.set(get_server_versions()[0])
    export_server_version_selection.pack(padx=10, pady=5)
    export_server_destination_var = StringVar()
    export_server_destination_entry = ttk.Entry(export_server_window, width=50, state="readonly",
                                                textvariable=export_server_destination_var)
    export_server_destination_entry.pack(padx=10, pady=5)
    export_server_destination_button = ttk.Button(export_server_window, text="Select Destination",
                                                  command=lambda: export_server_destination_var.set(folder_selection("Select Destination Folder")))
    export_server_destination_button.pack(padx=10, pady=5)
    compress_server_var = StringVar()
    compress_server_var.set("False")
    compress_server_check = ttk.Checkbutton(export_server_window, text="Compress Server Folder Into .zip File",
                                            variable=compress_server_var, onvalue="True", offvalue="False")
    compress_server_check.pack(padx=10, pady=5)
    export_server_wait_var = IntVar()
    export_server_btn = ttk.Button(export_server_window, text="Export Server",
                                   command=lambda: export_server_wait_var.set(1), style="Accent.TButton")
    export_server_btn.pack(padx=10, pady=5)
    export_server_window.wait_variable(export_server_wait_var)
    export_server_version = export_version_var.get()
    export_server_destination = export_server_destination_var.get()
    export_server_window.destroy()
    if not export_server_destination:
        logging.error("User did not select an export destination")
        showerror(title="Export Server", message="You did not select a destination! Nothing will be done!")
        return
    else:
        pass
    logging.info(f"Export Destination: {export_server_destination}")
    if compress_server_var.get() == "True":
        logging.info("User opted to compress server folder")
        try:
            make_archive(base_name=f"EasyMinecraftServer-Export-{export_server_version}", format="zip",
                        root_dir=f"{cwd}\\ServerFiles-{export_server_version}\\")
            copy(f"{cwd}\\EasyMinecraftServer-Export-{export_server_version}.zip", f"{export_server_destination}\\EasyMinecraftServer-Export-{export_server_version}.zip")
            os.remove(f"{cwd}\\EasyMinecraftServer-Export-{export_server_version}.zip")
            logging.info(
                "Server successfully exported to:\n" + f"{export_server_destination}\\EasyMinecraftServer-Export-{export_server_version}.zip")
            showinfo(title="Export Server",
                    message="Server successfully exported to:\n" + f"{export_server_destination}\\EasyMinecraftServer"
                                                                    f"-Export-{export_server_version}.zip")
            return
        except Exception as e:
            logging.error(f"Error while exporting server: {e}")
            showerror(title="Export Server", message=f"Error while exporting server: {e}")
            return
    else:
        logging.info("User opted to not compress server folder")
        try:
            copytree(f"{cwd}\\ServerFiles-{export_server_version}\\",
                    f"{export_server_destination}\\EasyMinecraftServer-Export-{export_server_version}\\")
            logging.info(
                "Server successfully exported to:\n" + f"{export_server_destination}\\EasyMinecraftServer-Export-{export_server_version}")
            showinfo(title="Export Server",
                    message="Server successfully exported to:\n" + f"{export_server_destination}\\EasyMinecraftServer-Export-{export_server_version}")
            return
        except Exception as e:
            logging.error(f"Error while exporting server: {e}")
            showerror(title="Export Server", message=f"Error while exporting server: {e}")
            return


def export_server_backup(version: str, name: str):
    export_server_backup_window = Toplevel(root)
    export_server_backup_window.title("Export Server Backup")
    export_server_backup_window.geometry("300x300")
    export_server_backup_window_label = ttk.Label(export_server_backup_window, text="Select the destination and decide\nto compress backup or not!")
    export_server_backup_window_label.pack(padx=10, pady=5)
    export_server_backup_destination_var = StringVar()
    export_server_backup_destination_entry = ttk.Entry(export_server_backup_window, width=50, state="readonly", textvariable=export_server_backup_destination_var)
    export_server_backup_destination_entry.pack(padx=10, pady=5)
    export_server_backup_destination_button = ttk.Button(export_server_backup_window, text="Select Destination", command=lambda: export_server_backup_destination_var.set(folder_selection("Select Destination Folder")))
    export_server_backup_destination_button.pack(padx=10, pady=5)
    compress_server_backup_var = StringVar()
    compress_server_backup_var.set("False")
    compress_server_backup_check = ttk.Checkbutton(export_server_backup_window, text="Compress Server Backup Into .zip File", variable=compress_server_backup_var, onvalue="True", offvalue="False")
    compress_server_backup_check.pack(padx=10, pady=5)
    export_server_backup_wait_var = IntVar()
    export_server_backup_btn = ttk.Button(export_server_backup_window, text="Export Server Backup", command=lambda: export_server_backup_wait_var.set(1), style="Accent.TButton")
    export_server_backup_btn.pack(padx=10, pady=5)
    export_server_backup_window.wait_variable(export_server_backup_wait_var)
    export_server_backup_destination = export_server_backup_destination_var.get()
    compress_backup = compress_server_backup_var.get()
    export_server_backup_window.destroy()
    if not export_server_backup_destination:
        logging.error("User did not select an export destination")
        showerror(title="Export Server Backup", message="You did not select a destination! Nothing will be done!")
        return
    else:
        pass
    logging.info(f"Export Destination: {export_server_backup_destination}")
    if compress_backup == "True":
        logging.info("User opted to compress server backup folder")
        try:
            make_archive(base_name=f"EasyMinecraftServer-BackupExport-{version}-{name}", format="zip",
                        root_dir=f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\")
            copy(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\EasyMinecraftServer-BackupExport-{version}-{name}.zip", f"{export_server_backup_destination}\\EasyMinecraftServer-BackupExport-{version}-{name}.zip")
            os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\EasyMinecraftServer-BackupExport-{version}-{name}.zip")
            logging.info("Server backup successfully exported to:\n" + f"{export_server_backup_destination}\\EasyMinecraftServer-BackupExport-{version}-{name}.zip")
            showinfo(title="Export Server Backup", message="Server backup successfully exported to:\n" + f"{export_server_backup_destination}\\EasyMinecraftServer-BackupExport-{version}-{name}.zip")
            return
        except Exception as e:
            logging.error(f"Error while exporting server backup: {e}")
            showerror(title="Export Server Backup", message=f"Error while exporting server backup: {e}")
            return
    else:
        logging.info("User opted to not compress server backup folder")
        try:
            copytree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{name}\\", f"{export_server_backup_destination}\\EasyMinecraftServer-BackupExport-{version}-{name}\\")
            logging.info("Server backup successfully exported to:\n" + f"{export_server_backup_destination}\\EasyMinecraftServer-BackupExport-{version}-{name}")
            showinfo(title="Export Server Backup", message="Server backup successfully exported to:\n" + f"{export_server_backup_destination}\\EasyMinecraftServer-BackupExport-{version}-{name}")
            return
        except Exception as e:
            logging.error(f"Error while exporting server backup: {e}")
            showerror(title="Export Server Backup", message=f"Error while exporting server backup: {e}")
            return


def folders_in(path_to_parent: str):
    for fname in os.listdir(path_to_parent):
        if os.path.isdir(os.path.join(path_to_parent, fname)):
            yield os.path.join(path_to_parent, fname)


def has_folders(path_to_parent: str):
    folders = list(folders_in(path_to_parent))
    return folders


def setup(arg: str):
    showinfo(title="Setup", message="Setup for EasyMinecraftServer is required! Please follow the instructions!")
    if arg == "all":
        settings_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "r")
        try:
            settings_json = json.load(settings_file)
            pass
        except:
            pass
        subdirectories = has_folders(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\")
        if len(subdirectories) == 0:
            pass
        else:
            restore_backup = askyesno(title="Restore Program Backup",
                                      message="You have a backup of EasyMinecraftServer! Would you like to restore it?")
            if restore_backup:
                backup_files = str(askdirectory(title="Select Backup Folder",
                                                initialdir=f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\"))
                if not os.path.exists(f"{backup_files}\\settings.json"):
                    showerror(title="Error", message="Invalid Backup Folder!")
                    logging.error("Invalid Backup Folder!")
                    restart_force()
                else:
                    copy(f"{backup_files}\\settings.json",
                         f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json")
                    showinfo(title="Restore Successful",
                             message="Restore Successful! EasyMinecraftServer will now restart!")
                    logging.info("Restore successful")
                    restart_force()
            else:
                pass
            pass
        showinfo(title="NGROK", message="Makeshift port-forwarding requires a ngrok account. Please navigate to "
                                        "https://dashboard.ngrok.com/get-started/setup after making a free account and "
                                        "get your authtoken!")
        setup_window = Toplevel(root)
        setup_window.title("EasyMinecraftServer (SETUP)")
        setup_window.geometry("500x500")
        ngrok_authtoken_label = ttk.Label(setup_window, text="Ngrok Authtoken")
        ngrok_authtoken_label.pack()
        ngrok_authtoken_entry = ttk.Entry(setup_window, width="50")
        ngrok_authtoken_entry.pack()
        try:
            ngrok_authtoken_entry.insert(0, settings_json["ngrok_authtoken"])
            pass
        except:
            pass
        ngrok_button = ttk.Button(setup_window, text="Ngrok Dashboard", command=ngrok_website)
        ngrok_button.pack()
        ram_bytes = psutil.virtual_memory().total
        ram_mb = ram_bytes / 1000000
        ram_allocation_amount_label = ttk.Label(setup_window,
                                                text=f"RAM Allocation Amount. Total Available: {str(round(float(ram_mb)))} MB")
        ram_allocation_amount_label.pack()
        ram_allocation_entry = ttk.Entry(setup_window, width="50")
        ram_allocation_entry.pack()
        try:
            ram_allocation_entry.insert(0, settings_json["ram_allocation_amount"])
            pass
        except:
            ram_allocation_entry.insert(0, str(round(float(ram_mb)) / 2))
            pass
        variable = StringVar(setup_window)
        try:
            variable.set(settings_json["auto_server_backup"])
            pass
        except:
            variable.set("True")
            pass
        auto_server_backup_label = ttk.Label(setup_window, text="Auto Server Backup")
        auto_server_backup_label.pack()
        auto_server_backup_entry_true = ttk.Radiobutton(setup_window, text="True", variable=variable, value="True")
        auto_server_backup_entry_true.pack()
        auto_server_backup_entry_false = ttk.Radiobutton(setup_window, text="False", variable=variable, value="False")
        auto_server_backup_entry_false.pack()
        backup_interval_label = ttk.Label(setup_window, text="Auto Backup Interval In Minutes")
        backup_interval_label.pack()
        backup_interval_entry = ttk.Entry(setup_window, width="50")
        backup_interval_entry.pack()
        try:
            backup_interval_entry.insert(0, settings_json["backup_interval"])
            pass
        except:
            backup_interval_entry.insert(0, "5")
            pass
        variable_two = StringVar(setup_window)
        try:
            variable_two.set(settings_json["server_gui"])
            pass
        except:
            variable_two.set("True")
            pass
        server_gui_label = ttk.Label(setup_window, text="Server GUI")
        server_gui_label.pack()
        server_gui_entry_true = ttk.Radiobutton(setup_window, text="True", variable=variable_two, value="True")
        server_gui_entry_true.pack()
        server_gui_entry_false = ttk.Radiobutton(setup_window, text="False", variable=variable_two, value="False")
        server_gui_entry_false.pack()
        variable_three = StringVar(setup_window)
        try:
            variable_three.set(settings_json["theme"])
            pass
        except:
            variable_three.set("Dark")
            pass
        theme_label = ttk.Label(setup_window, text="Theme")
        theme_label.pack()
        theme_entry_light = ttk.Radiobutton(setup_window, text="Light", variable=variable_three, value="Light")
        theme_entry_light.pack()
        theme_entry_dark = ttk.Radiobutton(setup_window, text="Dark", variable=variable_three, value="Dark")
        theme_entry_dark.pack()
        theme_entry_auto = ttk.Radiobutton(setup_window, text="Auto", variable=variable_three, value="Auto")
        theme_entry_auto.pack()
        var = IntVar()
        submit_button = ttk.Button(setup_window,
                                   command=lambda: var.set(1),
                                   text="Click Here To Save And Continue!", width="50", style="Accent.TButton")
        submit_button.pack()
        submit_button.wait_variable(var)
        new_ngrok_authtoken = ngrok_authtoken_entry.get()
        new_ram_allocation_amount = ram_allocation_entry.get()
        new_auto_server_backup = variable.get()
        new_backup_interval = backup_interval_entry.get()
        new_server_gui = variable_two.get()
        new_theme = variable_three.get()
        if new_backup_interval.isnumeric():
            pass
        else:
            showerror(title="Error", message="Backup Interval must be a number!")
            logging.error("Backup Interval must be a number!")
            restart_force()
            sys.exit(0)
        if new_ram_allocation_amount >= str(round(float(ram_mb))):
            showwarning(title="RAM Allocation Error",
                        message="RAM Allocation Amount is greater than the total available RAM!")
            logging.warning("RAM Allocation Amount is greater than the total available RAM!")
            restart_force()
            sys.exit(0)
        else:
            pass
        settings = {
            "ngrok_authtoken": new_ngrok_authtoken,
            "ram_allocation_amount": new_ram_allocation_amount,
            "auto_server_backup": new_auto_server_backup,
            "server_gui": new_server_gui,
            "theme": new_theme,
            "backup_interval": new_backup_interval
        }
        settings_object = json.dumps(settings, indent=4)
        settings_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "w+")
        settings_file.truncate(0)
        with settings_file as outfile:
            outfile.write(settings_object)
            pass
        settings_file.close()
        showinfo(title="EasyMinecraftServer Settings", message="New settings saved! Please restart to continue!")
        setup_window.destroy()
        restart_force()
        sys.exit(0)
    elif arg == "theme":
        settings_json = json.load(open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "r"))
        theme_window = Toplevel(root)
        theme_window.title("EasyMinecraftServer (SETUP)")
        theme_window.geometry("500x500")
        theme_variable = StringVar(theme_window)
        theme_label = ttk.Label(theme_window, text="Select an application theme")
        theme_label.pack()
        theme_entry_light = ttk.Radiobutton(theme_window, text="Light", variable=theme_variable, value="Light")
        theme_entry_light.pack()
        theme_entry_dark = ttk.Radiobutton(theme_window, text="Dark", variable=theme_variable, value="Dark")
        theme_entry_dark.pack()
        theme_entry_auto = ttk.Radiobutton(theme_window, text="Auto", variable=theme_variable, value="Auto")
        theme_entry_auto.pack()
        var = IntVar()
        submit_button = ttk.Button(theme_window, command=lambda: var.set(1), text="Click Here To Save And Continue!",
                                   width="50", style="Accent.TButton")
        submit_button.pack()
        submit_button.wait_variable(var)
        new_theme = theme_variable.get()
        settings = {
            "ngrok_authtoken": settings_json["ngrok_authtoken"],
            "ram_allocation_amount": settings_json["ram_allocation_amount"],
            "auto_server_backup": settings_json["auto_server_backup"],
            "server_gui": settings_json["server_gui"],
            "theme": new_theme,
            "backup_interval": settings_json["backup_interval"]
        }
        settings_object = json.dumps(settings, indent=4)
        settings_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "w+")
        settings_file.truncate(0)
        with settings_file as outfile:
            outfile.write(settings_object)
            pass
        settings_file.close()
        showinfo("EasyMinecraftServer Settings", "New settings saved! Please restart to continue!")
        theme_window.destroy()
        restart_force()
        sys.exit(0)
    elif arg == "backup_interval":
        settings_json = json.load(open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "r"))
        backup_interval_window = Toplevel(root)
        backup_interval_window.title("EasyMinecraftServer (SETUP)")
        backup_interval_window.geometry("500x500")
        backup_interval_label = ttk.Label(backup_interval_window, text="Enter the backup interval in minutes")
        backup_interval_label.pack()
        backup_interval_entry = ttk.Entry(backup_interval_window, width=10)
        backup_interval_entry.pack()
        backup_interval_entry.insert(0, "5")
        var = IntVar()
        submit_button = ttk.Button(backup_interval_window, command=lambda: var.set(1),
                                   text="Click Here To Save And Continue!", width="50", style="Accent.TButton")
        submit_button.pack()
        submit_button.wait_variable(var)
        new_backup_interval = backup_interval_entry.get()
        if new_backup_interval.isnumeric():
            pass
        else:
            showerror(title="Error", message="Backup Interval must be a number!")
            logging.error("Backup Interval must be a number!")
            restart_force()
            sys.exit(0)
        settings = {
            "ngrok_authtoken": settings_json["ngrok_authtoken"],
            "ram_allocation_amount": settings_json["ram_allocation_amount"],
            "auto_server_backup": settings_json["auto_server_backup"],
            "server_gui": settings_json["server_gui"],
            "theme": settings_json["theme"],
            "backup_interval": new_backup_interval
        }
        settings_object = json.dumps(settings, indent=4)
        settings_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "w+")
        settings_file.truncate(0)
        with settings_file as outfile:
            outfile.write(settings_object)
            pass
        settings_file.close()
        showinfo("EasyMinecraftServer Settings", "New settings saved! Please restart to continue!")
        backup_interval_window.destroy()
        restart_force()
        sys.exit(0)
    elif arg == "auto_server_backup":
        showerror(title="Settings Error",
                  message="Settings file has been corrupted! Program will now be reset and setup will be required again!")
        program_reset_force()
        sys.exit(0)
    elif arg == "server_gui":
        showerror(title="Settings Error",
                  message="Settings file has been corrupted! Program will now be reset and setup will be required again!")
        program_reset_force()
        sys.exit(0)
    elif arg == "ram_allocation_amount":
        showerror(title="Settings Error",
                  message="Settings file has been corrupted! Program will now be reset and setup will be required again!")
        program_reset_force()
        sys.exit(0)
    elif arg == "ngrok_authtoken":
        showerror(title="Settings Error",
                  message="Settings file has been corrupted! Program will now be reset and setup will be required again!")
        program_reset_force()
        sys.exit(0)


def settings_check():
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json"):
        create_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "x")
        create_file.close()
        pass
    else:
        pass
    while True:
        settings_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "r")
        settings_content = settings_file.read()
        settings_file.close()
        if "auto_server_backup" not in settings_content and "server_gui" not in settings_content and "ram_allocation_amount" not in settings_content and "ngrok_authtoken" not in settings_content and "theme" not in settings_content:
            setup("all")
            restart_force()
            sys.exit(0)
        elif "theme" not in settings_content and "backup_interval" not in settings_content:
            setup("all")
            restart_force()
            sys.exit(0)
        elif "auto_server_backup" not in settings_content:
            setup("auto_server_backup")
            restart_force()
            sys.exit(0)
        elif "server_gui" not in settings_content:
            setup("server_gui")
            restart_force()
            sys.exit(0)
        elif "ram_allocation_amount" not in settings_content:
            setup("ram_allocation_amount")
            restart_force()
            sys.exit(0)
        elif "ngrok_authtoken" not in settings_content:
            setup("ngrok_authtoken")
            restart_force()
            sys.exit(0)
        elif "theme" not in settings_content:
            setup("theme")
            restart_force()
            sys.exit(0)
        elif "backup_interval" not in settings_content:
            setup("backup_interval")
            restart_force()
            sys.exit(0)
        else:
            break
    return True


def settings():
    logging.info("Settings window launched")
    settings_window = Toplevel(root)
    settings_window.title("EasyMinecraftServer (SETTINGS)")
    settings_window.geometry("500x500")
    ngrok_authtoken_label = ttk.Label(settings_window, text="Ngrok Authtoken")
    ngrok_authtoken_label.pack()
    ngrok_authtoken_entry = ttk.Entry(settings_window, width="50")
    ngrok_authtoken_entry.pack()
    ngrok_authtoken = settings_json["ngrok_authtoken"]
    ngrok_authtoken_entry.insert(0, ngrok_authtoken)
    ngrok_button = ttk.Button(settings_window, text="Ngrok Dashboard", command=ngrok_website)
    ngrok_button.pack()
    ram_bytes = psutil.virtual_memory().total
    ram_mb = ram_bytes / 1000000
    ram_allocation_amount_label = ttk.Label(settings_window,
                                            text=f"RAM Allocation Amount. Total Available: {str(round(float(ram_mb)))} MB")
    ram_allocation_amount_label.pack()
    ram_allocation_amount_entry = ttk.Entry(settings_window, width="50")
    ram_allocation_amount_entry.pack()
    ram_allocation_amount = settings_json["ram_allocation_amount"]
    ram_allocation_amount_entry.insert(0, ram_allocation_amount)
    variable = StringVar(settings_window)
    auto_server_backup = settings_json["auto_server_backup"]
    variable.set(auto_server_backup)
    auto_server_backup_label = ttk.Label(settings_window, text="Auto Server Backup")
    auto_server_backup_label.pack()
    auto_server_backup_entry_true = ttk.Radiobutton(settings_window, text="True", variable=variable, value="True")
    auto_server_backup_entry_true.pack()
    auto_server_backup_entry_false = ttk.Radiobutton(settings_window, text="False", variable=variable, value="False")
    auto_server_backup_entry_false.pack()
    backup_interval_label = ttk.Label(settings_window, text="Auto Backup Interval In Minutes")
    backup_interval_label.pack()
    backup_interval_entry = ttk.Entry(settings_window, width="50")
    backup_interval_entry.pack()
    backup_interval = settings_json["backup_interval"]
    backup_interval_entry.insert(0, backup_interval)
    variable_two = StringVar(settings_window)
    server_gui = settings_json["server_gui"]
    variable_two.set(server_gui)
    server_gui_label = ttk.Label(settings_window, text="Server GUI")
    server_gui_label.pack()
    server_gui_entry_true = ttk.Radiobutton(settings_window, text="True", variable=variable_two, value="True")
    server_gui_entry_true.pack()
    server_gui_entry_false = ttk.Radiobutton(settings_window, text="False", variable=variable_two, value="False")
    server_gui_entry_false.pack()
    variable_three = StringVar(settings_window)
    current_theme_setting = settings_json["theme"]
    variable_three.set(current_theme_setting)
    theme_label = ttk.Label(settings_window, text="Theme")
    theme_label.pack()
    theme_entry_light = ttk.Radiobutton(settings_window, text="Light", variable=variable_three, value="Light")
    theme_entry_light.pack()
    theme_entry_dark = ttk.Radiobutton(settings_window, text="Dark", variable=variable_three, value="Dark")
    theme_entry_dark.pack()
    theme_entry_auto = ttk.Radiobutton(settings_window, text="Auto", variable=variable_three, value="Auto")
    theme_entry_auto.pack()
    var = IntVar()
    submit_button = ttk.Button(settings_window,
                               command=lambda: var.set(1),
                               text="Click Here To Save And Continue!", width="50", style="Accent.TButton")
    submit_button.pack()
    logging.info("Awaiting user input in settings window")
    submit_button.wait_variable(var)
    logging.info("Writing new settings")
    new_ngrok_authtoken = ngrok_authtoken_entry.get()
    new_ram_allocation_amount = ram_allocation_amount_entry.get()
    new_auto_server_backup = variable.get()
    new_backup_interval = backup_interval_entry.get()
    new_server_gui = variable_two.get()
    new_theme = variable_three.get()
    if new_ram_allocation_amount >= str(round(float(ram_mb))):
        showwarning(title="RAM Allocation Error",
                    message="RAM Allocation Amount is greater than the total available RAM!")
        logging.warning("RAM Allocation Amount is greater than the total available RAM!")
        return
    else:
        pass
    if new_backup_interval.isnumeric():
        pass
    else:
        showwarning(title="Backup Interval Error",
                    message="Backup Interval is not a number!")
        logging.warning("Backup Interval is not a number!")
        return
    settings = {
        "ngrok_authtoken": new_ngrok_authtoken,
        "ram_allocation_amount": new_ram_allocation_amount,
        "auto_server_backup": new_auto_server_backup,
        "server_gui": new_server_gui,
        "theme": new_theme,
        "backup_interval": new_backup_interval
    }
    settings_object = json.dumps(settings, indent=4)
    settings_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "w+")
    settings_file.truncate(0)
    with settings_file as outfile:
        outfile.write(settings_object)
        pass
    settings_file.close()
    showinfo(title="EasyMinecraftServer Settings", message="New settings saved! Please restart to continue!")
    logging.info("New settings saved")
    settings_window.destroy()
    restart_force()
    sys.exit(0)


def program_reset_force():
    logging.warning("Program reset forced")
    file_path = f"{user_dir}\\Documents\\EasyMinecraftServer\\"
    file_list = os.listdir(file_path)
    for folder in file_list:
        if folder == "Logs" or folder == "ProgramBackups":
            pass
        else:
            rmtree(f"{file_path}\\{folder}")
            pass
        pass
    showinfo(title="Reset", message="EasyMinecraftServer has been reset!")
    logging.warning("EasyMinecraftServer reset")
    restart_force()


def program_reset():
    logging.warning("Program reset started")
    reset_confirm = askyesno(title="Reset", message="Are you sure you want to reset EasyMinecraftServer?")
    if reset_confirm:
        logging.info("User confirmed reset")
        file_path = f"{user_dir}\\Documents\\EasyMinecraftServer\\"
        file_list = os.listdir(file_path)
        for folder in file_list:
            if folder == "Logs" or folder == "ProgramBackups":
                pass
            else:
                rmtree(f"{file_path}\\{folder}")
                pass
            pass
        showinfo(title="Reset", message="EasyMinecraftServer has been reset!")
        logging.warning("EasyMinecraftServer reset")
        restart_force()
    else:
        return


def program_backup():
    logging.info("Program backup started")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\")
        logging.info("Program backup directory created")
        pass
    else:
        pass
    backup_name = askstring(title="Backup Name", prompt="What would you like to name your backup?")
    if backup_name is None or backup_name == "" or backup_name.isspace():
        showerror(title="Backup Error", message="Backup name cannot be empty!")
        logging.error("Backup name cannot be empty")
        return
    elif os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\{backup_name}\\"):
        logging.warning("Backup name already exists")
        replace_ask = askyesno(title="EasyMinecraftServer Backup",
                               message="A backup with this name already exists! Would you like to replace it?")
        if replace_ask:
            logging.info("User confirmed backup replace")
            logging.info("Removing old backup")
            rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\{backup_name}\\")
            logging.info("Old backup removed")
            logging.info("Creating new backup")
            logging.info(f"Starting backup with name: {backup_name}")
            copytree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\",
                     f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\{backup_name}\\")
            showinfo(title="Backup", message="EasyMinecraftServer has been backed up!")
            logging.info("EasyMinecraftServer backup complete")
            return
        else:
            logging.error("Backup name already exists and user chose not to replace")
            showinfo(title="Backup", message="EasyMinecraftServer has NOT been backed up!")
            return
    else:
        logging.info(f"Starting backup with name: {backup_name}")
        copytree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\",
                 f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\{backup_name}\\")
        showinfo(title="Backup", message="EasyMinecraftServer has been backed up!")
        logging.info("EasyMinecraftServer backup complete")
        return


def program_restore():
    logging.info("Program restore started")
    path = f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\"
    backup_subdirs = os.listdir(path)
    if len(backup_subdirs) == 0:
        showerror(title="Restore Error", message="No backups found!")
        logging.error("No backups found")
        return
    else:
        backup_name = askdirectory(title="Select A Backup To Restore", initialdir=path)
        if not os.path.exists(f"{backup_name}\\settings.json"):
            showerror(title="Restore Error", message="Invalid Backup!")
            logging.error("Invalid backup")
            return
        else:
            if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\"):
                rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\")
                logging.info("EasyMinecraftServer reset")
                pass
            else:
                pass
            logging.info("Restoring settings from backup")
            copytree(f"{backup_name}\\", f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\")
            showinfo(title="Restore", message="EasyMinecraftServer backup has been restored!")
            logging.info("EasyMinecraftServer backup restored")
            restart_force()
            sys.exit(0)


def changelog():
    logging.info("Opening changelog window")
    changelog_window = Toplevel(root)
    changelog_window.title("EasyMinecraftServer (CHANGELOG)")
    changelog_window.geometry("550x550")
    changelog_file = open(f"{cwd}\\CHANGELOG.txt", "r")
    changelog_label = ttk.Label(changelog_window, text=f"{changelog_file.read()}")
    changelog_file.close()
    changelog_label.pack()


def update():
    logging.info("Manual update check started")
    try:
        url = "https://github.com/teekar2023/EasyMinecraftServer/releases/latest"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        showerror(title="Update Error", message=f"Error While Checking For Updates: {e}")
        logging.error(f"Error While Checking For Updates: {e}")
        return
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"Update available: {new_version}")
        new_url = str(redirected_url) + f"/EasyMinecraftServerInstaller-{str(new_version.replace('v', ''))}.exe"
        download_url = new_url.replace("tag", "download")
        logging.info("Update download url: " + download_url)
        update_window = Toplevel(root)
        update_window.title("EasyMinecraftServer (UPDATE)")
        update_window.geometry("550x550")
        update_text = ttk.Label(update_window,
                                text="There Is A New Update Available! Click The Button Below If You Wish To Download It!")
        update_text.pack()
        int_var = IntVar(update_window)
        update_button = ttk.Button(update_window, command=lambda: int_var.set(1), text="Update Now", width="50",
                                   style="Accent.TButton")
        update_button.pack()
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\"):
            os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\")
            pass
        else:
            pass
        try:
            logging.info("Downloading new version changelog")
            changelog_url = "https://raw.githubusercontent.com/teekar2023/EasyMinecraftServer/master/CHANGELOG.txt"
            changelog_download = urllib.request.urlopen(changelog_url)
            if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt"):
                os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt")
                pass
            else:
                pass
            create_changelog_file = open(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'x')
            create_changelog_file.close()
            changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt",
                                  'wb')
            while True:
                changelog_data = changelog_download.read()
                if not changelog_data:
                    break
                else:
                    changelog_file.write(changelog_data)
                    pass
            changelog_file.close()
            changelog_txt = str(
                open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'r').read())
            pass
        except Exception as e:
            changelog_txt = f"There was an error while accessing new version changelog data: {e}"
            logging.error("There was an error while accessing changelog data")
            pass
        changelog_text = ttk.Label(update_window, text=str(changelog_txt))
        changelog_text.pack()
        update_button.wait_variable(int_var)
        if os.path.exists(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe"):
            logging.info("Update already downloaded")
            logging.info("Launching update installer")
            os.startfile(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe")
            exit_program_force()
        else:
            try:
                f = open(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe",
                    'wb')
                showwarning(title="EasyMinecraftServer Update",
                            message="Update will now be downloaded and installer will be launcher. "
                                    "This may take a while to please be patient and d not do anything if program becomes unresponsive!")
                logging.info("Downloading update installer")
                f2 = urllib.request.urlopen(download_url)
                while True:
                    data = f2.read()
                    if not data:
                        break
                    else:
                        f.write(data)
                        pass
                    pass
                f.close()
                showinfo(title="EasyMinecraftServer Update",
                         message="Update Downloaded Successfully! Installer Will Now Be Launched To Complete Update!")
                logging.info("Update Downloaded Successfully!")
                logging.info("Launching update installer")
                os.startfile(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe")
                exit_program_force()
            except Exception as e:
                showerror(title="EasyMinecraftServer Update",
                          message=f"There was an error while downloading update: {e}")
                logging.error(f"There was an error while downloading update: {e}")
                exit_program_force()
    else:
        showinfo(title="Update", message="EasyMinecraftServer is already up to date!")
        return


def update_event(event):
    logging.info("Manual update check started")
    try:
        url = "https://github.com/teekar2023/EasyMinecraftServer/releases/latest"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        showerror(title="Update Error", message=f"Error While Checking For Updates: {e}")
        logging.error(f"Error While Checking For Updates: {e}")
        return
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"Update available: {new_version}")
        new_url = str(redirected_url) + f"/EasyMinecraftServerInstaller-{str(new_version.replace('v', ''))}.exe"
        download_url = new_url.replace("tag", "download")
        logging.info("Update download url: " + download_url)
        update_window = Toplevel(root)
        update_window.title("EasyMinecraftServer (UPDATE)")
        update_window.geometry("550x550")
        update_text = ttk.Label(update_window,
                                text="There Is A New Update Available! Click The Button Below If You Wish To Download It!")
        update_text.pack()
        int_var = IntVar(update_window)
        update_button = ttk.Button(update_window, command=lambda: int_var.set(1), text="Update Now", width="50",
                                   style="Accent.TButton")
        update_button.pack()
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\"):
            os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\")
            pass
        else:
            pass
        try:
            logging.info("Downloading new version changelog")
            changelog_url = "https://raw.githubusercontent.com/teekar2023/EasyMinecraftServer/master/CHANGELOG.txt"
            changelog_download = urllib.request.urlopen(changelog_url)
            if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt"):
                os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt")
                pass
            else:
                pass
            create_changelog_file = open(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'x')
            create_changelog_file.close()
            changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt",
                                  'wb')
            while True:
                changelog_data = changelog_download.read()
                if not changelog_data:
                    break
                else:
                    changelog_file.write(changelog_data)
                    pass
            changelog_file.close()
            changelog_txt = str(
                open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'r').read())
            pass
        except Exception as e:
            changelog_txt = f"There was an error while accessing new version changelog data: {e}"
            logging.error("There was an error while accessing changelog data")
            pass
        changelog_text = ttk.Label(update_window, text=str(changelog_txt))
        changelog_text.pack()
        update_button.wait_variable(int_var)
        if os.path.exists(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe"):
            logging.info("Update already downloaded")
            logging.info("Launching update installer")
            os.startfile(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe")
            exit_program_force()
        else:
            try:
                f = open(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe",
                    'wb')
                showwarning(title="EasyMinecraftServer Update",
                            message="Update will now be downloaded and installer will be launcher. "
                                    "This may take a while to please be patient and d not do anything if program becomes unresponsive!")
                logging.info("Downloading update installer")
                f2 = urllib.request.urlopen(download_url)
                while True:
                    data = f2.read()
                    if not data:
                        break
                    else:
                        f.write(data)
                        pass
                    pass
                f.close()
                showinfo(title="EasyMinecraftServer Update",
                         message="Update Downloaded Successfully! Installer Will Now Be Launched To Complete Update!")
                logging.info("Update Downloaded Successfully!")
                logging.info("Launching update installer")
                os.startfile(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe")
                exit_program_force()
            except Exception as e:
                showerror(title="EasyMinecraftServer Update",
                          message=f"There was an error while downloading update: {e}")
                logging.error(f"There was an error while downloading update: {e}")
                exit_program_force()
    else:
        showinfo(title="Update", message="EasyMinecraftServer is already up to date!")
        return


def update_startup():
    logging.info("Manual update check started")
    try:
        url = "https://github.com/teekar2023/EasyMinecraftServer/releases/latest"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        showerror(title="Update Error", message=f"Error While Checking For Updates: {e}")
        logging.error(f"Error While Checking For Updates: {e}")
        return
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"Update available: {new_version}")
        new_url = str(redirected_url) + f"/EasyMinecraftServerInstaller-{str(new_version.replace('v', ''))}.exe"
        download_url = new_url.replace("tag", "download")
        logging.info("Update download url: " + download_url)
        update_window = Toplevel(root)
        root.withdraw()
        update_window.protocol("WM_DELETE_WINDOW", exit_program_force)
        update_window.title("EasyMinecraftServer (UPDATE)")
        update_window.geometry("550x550")
        update_text = ttk.Label(update_window,
                                text="There Is A New Update Available! Click The Button Below If You Wish To Download It!")
        update_text.pack()
        int_var = IntVar(update_window)
        update_button = ttk.Button(update_window, command=lambda: int_var.set(1), text="Update Now", width="50",
                                   style="Accent.TButton")
        update_button.pack()
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\"):
            os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\")
            pass
        else:
            pass
        try:
            logging.info("Downloading new version changelog")
            changelog_url = "https://raw.githubusercontent.com/teekar2023/EasyMinecraftServer/master/CHANGELOG.txt"
            changelog_download = urllib.request.urlopen(changelog_url)
            if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt"):
                os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt")
                pass
            else:
                pass
            create_changelog_file = open(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'x')
            create_changelog_file.close()
            changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt",
                                  'wb')
            while True:
                changelog_data = changelog_download.read()
                if not changelog_data:
                    break
                else:
                    changelog_file.write(changelog_data)
                    pass
            changelog_file.close()
            changelog_txt = str(
                open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'r').read())
            pass
        except Exception as e:
            changelog_txt = f"There was an error while accessing new version changelog data: {e}"
            logging.error("There was an error while accessing changelog data")
            pass
        changelog_text = ttk.Label(update_window, text=str(changelog_txt))
        changelog_text.pack()
        update_button.wait_variable(int_var)
        if os.path.exists(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe"):
            logging.info("Update already downloaded")
            logging.info("Launching update installer")
            os.startfile(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe")
            exit_program_force()
        else:
            try:
                f = open(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe",
                    'wb')
                showwarning(title="EasyMinecraftServer Update",
                            message="Update will now be downloaded and installer will be launcher. "
                                    "This may take a while to please be patient and d not do anything if program becomes unresponsive!")
                logging.info("Downloading update installer")
                f2 = urllib.request.urlopen(download_url)
                while True:
                    data = f2.read()
                    if not data:
                        break
                    else:
                        f.write(data)
                        pass
                    pass
                f.close()
                showinfo(title="EasyMinecraftServer Update",
                         message="Update Downloaded Successfully! Installer Will Now Be Launched To Complete Update!")
                logging.info("Update Downloaded Successfully!")
                logging.info("Launching update installer")
                os.startfile(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe")
                exit_program_force()
            except Exception as e:
                showerror(title="EasyMinecraftServer Update",
                          message=f"There was an error while downloading update: {e}")
                logging.error(f"There was an error while downloading update: {e}")
                exit_program_force()
    else:
        showinfo(title="Update", message="EasyMinecraftServer is already up to date!")
        return


def exit_program():
    exit_confirmation = askyesno("Exit", "Are you sure you want to exit?")
    if exit_confirmation:
        logging.info("Exiting EasyMinecraftServer")
        logging.shutdown()
        root.destroy()
        PROCNAME = "EasyMinecraftServer.exe"
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                proc.kill()
                pass
            else:
                pass
            pass
        sys.exit(0)
    else:
        pass


def exit_program_event(event):
    exit_confirmation = askyesno("Exit", "Are you sure you want to exit?")
    if exit_confirmation:
        logging.info("Exiting EasyMinecraftServer")
        logging.shutdown()
        root.destroy()
        PROCNAME = "EasyMinecraftServer.exe"
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                proc.kill()
                pass
            else:
                pass
            pass
        sys.exit(0)
    else:
        pass


def exit_program_force():
    logging.info("Exiting EasyMinecraftServer")
    logging.shutdown()
    PROCNAME = "EasyMinecraftServer.exe"
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()
            pass
        else:
            pass
        pass
    root.destroy()
    sys.exit(0)


def restart_force():
    logging.info("Restarting EasyMinecraftServer")
    logging.shutdown()
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    sys.exit(0)


def restart_program():
    confirm_restart = askyesno(title="Restart", message="Restart EasyMinecraftServer?")
    if confirm_restart:
        logging.info("Restarting EasyMinecraftServer")
        logging.shutdown()
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        sys.exit(0)
    else:
        pass


def restart_program_event(event):
    confirm_restart = askyesno(title="Restart", message="Restart EasyMinecraftServer?")
    if confirm_restart:
        logging.info("Restarting EasyMinecraftServer")
        logging.shutdown()
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        sys.exit(0)
    else:
        pass


def uninstall_program():
    confirm_uninstall = askyesno(title="Uninstall", message="Are you sure you want to uninstall EasyMinecraftServer?")
    if confirm_uninstall:
        logging.info("Uninstalling EasyMinecraftServer")
        reset_all = askyesno(title="Uninstall",
                             message="Would you like to reset all settings and data including backups?")
        if reset_all:
            logging.info("Resetting all settings and data including backups")
            try:
                file_path = f"{user_dir}\\Documents\\EasyMinecraftServer\\"
                file_list = os.listdir(file_path)
                for folder in file_list:
                    if folder == "Logs" or folder == "ProgramBackups":
                        pass
                    else:
                        rmtree(f"{file_path}\\{folder}")
                        pass
                    pass
                showwarning(title="Uninstall", message="EasyMinecraftServer Data Reset!")
                logging.info("EasyMinecraftServer Data Reset!")
                pass
            except Exception as e:
                showerror(title="Reset Error", message=f"Error while resetting data and settings: {e}")
                showerror(title="Uninstall",
                          message="EasyMinecraftServer Data Reset Failed! These Files Can Be Manually Deleted In Your Documents Folder!")
                logging.error(f"Error while resetting data and settings: {e}")
                logging.error("EasyMinecraftServer Data Reset Failed")
                pass
            pass
        else:
            pass
        remove_av = askyesno(title="Anti-Virus Exclusions",
                             message="Would you like to remove all Anti-Virus Exclusions?")
        if remove_av:
            logging.info("Launching MinecraftServerUnelevator.exe")
            os.system(f"MinecraftServerUnelevator")
            pass
        else:
            logging.info("Anti-Virus Exclusion removal denied")
            pass
        showinfo(title="Uninstall", message="Sorry to see you go! Hope you come back soon!")
        logging.info("Launching EasyMinecraftServer Uninstaller")
        os.startfile(f"{cwd}\\unins000.exe")
        exit_program_force()
    else:
        showinfo(title="Uninstall", message="Uninstall Cancelled!")
        return


def uninstall_program_event(event):
    confirm_uninstall = askyesno(title="Uninstall", message="Are you sure you want to uninstall EasyMinecraftServer?")
    if confirm_uninstall:
        logging.info("Uninstalling EasyMinecraftServer")
        reset_all = askyesno(title="Uninstall",
                             message="Would you like to reset all settings and data including backups?")
        if reset_all:
            logging.info("Resetting all settings and data including backups")
            try:
                file_path = f"{user_dir}\\Documents\\EasyMinecraftServer\\"
                file_list = os.listdir(file_path)
                for folder in file_list:
                    if folder == "Logs":
                        pass
                    else:
                        rmtree(f"{file_path}\\{folder}")
                        pass
                    pass
                showwarning(title="Uninstall", message="EasyMinecraftServer Data Reset!")
                logging.info("EasyMinecraftServer Data Reset!")
                pass
            except Exception as e:
                showerror(title="Reset Error", message=f"Error while resetting data and settings: {e}")
                showerror(title="Uninstall",
                          message="EasyMinecraftServer Data Reset Failed! These Files Can Be Manually Deleted In Your Documents Folder!")
                logging.error(f"Error while resetting data and settings: {e}")
                logging.error("EasyMinecraftServer Data Reset Failed")
                pass
            pass
        else:
            pass
        showinfo(title="Uninstall", message="Sorry to see you go! Hope you come back soon!")
        logging.info("Launching EasyMinecraftServer Uninstaller")
        os.startfile(f"{cwd}\\unins000.exe")
        exit_program_force()
    else:
        showinfo(title="Uninstall", message="Uninstall Cancelled!")
        return


def jdk_installer():
    try:
        os.startfile(f"{cwd}\\jdk17-installer.exe")
        logging.info("Launched JDK installer")
        pass
    except Exception:
        logging.error("JDK installer not found")
        if askyesno(title="JDK Installer", message="JDK Installer Not Found! Would you like to download it?"):
            logging.error("Downloading JDK installer from website")
            logging.info("Downloading JDK installer")
            java_f = open(f"{cwd}\\jdk17-installer.exe", mode="wb")
            java_f2 = urllib.request.urlopen("https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe")
            while True:
                java_data = java_f2.read()
                if not java_data:
                    break
                else:
                    java_f.write(java_data)
                    pass
                pass
            java_f.close()
            logging.info("JDK installer downloaded")
            os.startfile(f"{cwd}\\jdk17-installer.exe")
            logging.info("Launched JDK installer")
            pass
        else:
            logging.info("JDK installer download cancelled")
            pass
    return


def backup_logs():
    mod_time = os.path.getmtime(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\")
        pass
    else:
        pass
    copy(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log",
         f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\AppCrash.log")
    showinfo(title="Crash Logs",
             message=f"Crash logs were backed up and can be found here: {user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\AppCrash.log")
    return


def backup_logs_event(event):
    logging.info("Backing up server logs due to request")
    mod_time = os.path.getmtime(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\")
        pass
    else:
        pass
    copy(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log",
         f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\App.log")
    showinfo(title="EasyMinecraftServer Logs",
             message=f"Program logs were backed up and can be found here: {user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\App.log")
    return


def license_window():
    logging.info("Showing license window")
    license_window = Toplevel()
    license_window.title("EasyMinecraftServer (LICENSE)")
    license_window.geometry("500x600")
    license_text = Text(license_window, width=500, height=600)
    license_text.pack()
    license_text_string = open(f"{cwd}\\LICENSE.txt", 'r').read()
    license_text.insert(END, license_text_string)
    license_text.config(state=DISABLED)
    return


def license_window_event(event):
    logging.info("Showing license window")
    license_window = Toplevel()
    license_window.title("EasyMinecraftServer (LICENSE)")
    license_window.geometry("500x600")
    license_text = Text(license_window, width=500, height=600)
    license_text.pack()
    license_text_string = open(f"{cwd}\\LICENSE.txt", 'r').read()
    license_text.insert(END, license_text_string)
    license_text.config(state=DISABLED)
    return


def readme_window():
    logging.info("Showing readme window")
    readme_window = Toplevel()
    readme_window.title("EasyMinecraftServer (README)")
    readme_window.geometry("500x600")
    readme_text = Text(readme_window, width=500, height=600)
    readme_text.pack()
    readme_text_string = open(f"{cwd}\\README.md", 'r').read()
    readme_text.insert(END, readme_text_string)
    readme_text.config(state=DISABLED)
    return


def help_window():
    logging.info("Showing help window")
    help_window = Toplevel()
    help_window.title("EasyMinecraftServer (HELP)")
    help_window.geometry("800x640")
    try:
        url = "https://github.com/teekar2023/EasyMinecraftServer/releases/latest"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        logging.error(f"Error While Checking For Updates: {e}")
        redirected_url = "ERROR"
        pass
    help_text = "EasyMinecraftServer v2.15.0\n"
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"Update available: {new_version}")
        help_text += "Update available: " + new_version + "\n\n"
        pass
    elif redirected_url == "ERROR":
        help_text += "Error while checking for updates!\n\n"
        pass
    else:
        logging.info("No update available")
        help_text += "Latest Version Installed\n\n"
        pass
    help_text += """EasyMinecraftServer is a free and open source program that makes hosting and manipulating minecraft servers easy and convenient!

All the buttons should be pretty self explanatory:
Start Server: Starts the server!
Create Backup Button: Creates a backup of the server files!
Restore Backup Button: Restores a backup of the server files!
Manage Backups Button: Rename, remove, or export server backups!
Reset Server Button: Resets the server files!
Use Custom Map Button: Allows you to use a custom map in your server!
Reset Dimension Button: Resets a dimension from the server!
Change Server Properties Button: Allows you to change the server properties!
Import External Server Button: Allows you to import an external server to be used with the program!
Export Server Button: Allows you to export a server archive to a folder of your choice for easy sharing!

Hosting a server without port forwarding requires a ngrok account and an authtoken!
More information about ngrok can be found by visiting the ngrok dashboard with the button below!

Feel free to ask questions on the GitHub page using the button below!
    """
    help_label = ttk.Label(help_window, text=help_text)
    help_label.pack()
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
        update_button = ttk.Button(help_window, text="Update", command=update, style="Accent.TButton", width="50")
        update_button.pack()
        pass
    else:
        pass
    program_github = ttk.Button(help_window, text="GitHub", command=website, width="50")
    program_github.pack()
    ngrok_button = ttk.Button(help_window, text="Ngrok Dashboard", command=ngrok_website, width="50")
    ngrok_button.pack()
    jdk_installer_button = ttk.Button(help_window, text="JDK Installer", command=jdk_installer, width="50")
    jdk_installer_button.pack()
    changelog_button = ttk.Button(help_window, text="Changelog", command=changelog, width="50")
    changelog_button.pack()
    license_button = ttk.Button(help_window, text="License", command=license_window, width="50")
    license_button.pack()
    readme_button = ttk.Button(help_window, text="Readme", command=readme_window, width="50")
    readme_button.pack()
    debug_button = ttk.Button(help_window, text="Debug", command=debug, width="50")
    debug_button.pack()
    return


def help_window_event(event):
    logging.info("Showing help window")
    help_window = Toplevel()
    help_window.title("EasyMinecraftServer (HELP)")
    help_window.geometry("800x640")
    try:
        url = "https://github.com/teekar2023/EasyMinecraftServer/releases/latest"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        logging.error(f"Error While Checking For Updates: {e}")
        redirected_url = "ERROR"
        pass
    help_text = "EasyMinecraftServer v2.15.0\n"
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"Update available: {new_version}")
        help_text += "Update available: " + new_version + "\n\n"
        pass
    elif redirected_url == "ERROR":
        help_text += "Error while checking for updates!\n\n"
        pass
    else:
        logging.info("No update available")
        help_text += "Latest Version Installed\n\n"
        pass
    help_text += """EasyMinecraftServer is a free and open source program that makes hosting and manipulating minecraft servers easy and convenient!

All the buttons should be pretty self explanatory:
Start Server: Starts the server!
Create Backup Button: Creates a backup of the server files!
Restore Backup Button: Restores a backup of the server files!
Manage Backups Button: Rename, remove, or export server backups!
Reset Server Button: Resets the server files!
Use Custom Map Button: Allows you to use a custom map in your server!
Reset Dimension Button: Resets a dimension from the server!
Change Server Properties Button: Allows you to change the server properties!
Import External Server Button: Allows you to import an external server to be used with the program!
Export Server Button: Allows you to export a server archive to a folder of your choice for easy sharing!

Hosting a server without port forwarding requires a ngrok account and an authtoken!
More information about ngrok can be found by visiting the ngrok dashboard with the button below!

Feel free to ask questions on the GitHub page using the button below!
    """
    help_label = ttk.Label(help_window, text=help_text)
    help_label.pack()
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
        update_button = ttk.Button(help_window, text="Update", command=update, style="Accent.TButton", width="50")
        update_button.pack()
        pass
    else:
        pass
    program_github = ttk.Button(help_window, text="GitHub", command=website, width="50")
    program_github.pack()
    ngrok_button = ttk.Button(help_window, text="Ngrok Dashboard", command=ngrok_website, width="50")
    ngrok_button.pack()
    jdk_installer_button = ttk.Button(help_window, text="JDK Installer", command=jdk_installer, width="50")
    jdk_installer_button.pack()
    changelog_button = ttk.Button(help_window, text="Changelog", command=changelog, width="50")
    changelog_button.pack()
    license_button = ttk.Button(help_window, text="License", command=license_window, width="50")
    license_button.pack()
    readme_button = ttk.Button(help_window, text="Readme", command=readme_window, width="50")
    readme_button.pack()
    debug_button = ttk.Button(help_window, text="Debug", command=debug, width="50")
    debug_button.pack()
    return


def ngrok_website():
    webbrowser.open("https://dashboard.ngrok.com/")
    return


def explorer_logs():
    subprocess.Popen(f"explorer {user_dir}\\Documents\\EasyMinecraftServer\\Logs\\")
    subprocess.Popen(f"explorer {cwd}")
    return


def debug_event(event):
    logging.info("Debug function called")
    explorer_logs_thread = Thread(target=explorer_logs)
    explorer_logs_thread.start()
    os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log")
    showinfo(title="Debug",
             message="Logs and data folder launched! Press F3 on the main window to create a backup of current logs!")
    return


def debug():
    logging.info("Debug function called")
    explorer_logs_thread = Thread(target=explorer_logs)
    explorer_logs_thread.start()
    os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log")
    showinfo(title="Debug",
             message="Logs and data folder launched! Press F3 on the main window to create a backup of current logs!")
    return


def server_backups():
    subprocess.Popen(f"explorer {user_dir}\\Documents\\EasyMinecraftServer\\Backups\\")
    return


def server_files():
    version = askstring(title="View Server Files",
                        prompt="Enter the version you want to view! This can be any version but must be in the format 'num.num.num'!")
    if version is None:
        return
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
            showwarning(title="View Server Files", message="Do not tamper with ServerFiles unless you know what you "
                                                           "are doing! A server backup is recommended before "
                                                           "interacting with ServerFiles!")
            subprocess.Popen(f"explorer {cwd}\\ServerFiles-{version}\\")
            return
        else:
            showerror(title="Error", message="Version does not exist!")
            logging.error("Version does not exist!")
            return


def av_exclusions():
    exclusion_confirm = askyesno(title="Anti-Virus Exclusion",
                                 message="Would you like to launch the anti-virus exception creator to make all program and server files not be scanned by your antivirus program?")
    if exclusion_confirm:
        showinfo(title="Anti-Virus Exclusion", message="Launching Anti-Virus Exclusion Creator! Program will exit!")
        logging.info("Launching Anti-Virus Exclusion Creator!")
        os.startfile(f"MinecraftServerElevator.exe")
        exit_program_force()
    else:
        return


def av_exclusions_remove():
    exclusion_confirm = askyesno(title="Anti-Virus Exclusion",
                                 message="Would you like to remove the anti-virus exception creator to make all program and server files be scanned by your antivirus program?")
    if exclusion_confirm:
        showinfo(title="Anti-Virus Exclusion", message="Launching Anti-Virus Exclusion Remover! Program will exit!")
        logging.info("Launching Anti-Virus Exclusion Remover!")
        os.startfile(f"MinecraftServerUnelevator.exe")
        exit_program_force()
    else:
        return


def website():
    webbrowser.open("https://github.com/teekar2023/EasyMinecraftServer/")
    logging.info("Launched website!")
    return


def dark_title_bar():
    root.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ctypes.windll.user32.GetParent
    hwnd = get_parent(root.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ctypes.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value))
    return


def get_server_versions():
    logging.info("Getting existing server versions")
    server_files_directory = f"{cwd}\\"
    server_folders = os.listdir(server_files_directory)
    server_versions = []
    for folder in server_folders:
        if "ServerFiles-" in folder:
            server_versions.append(folder.replace("ServerFiles-", ""))
            pass
        else:
            pass
    logging.info(f"Server versions found: {server_versions}")
    return server_versions


def log_settings():
    logging.info("Reading settings.json file")
    settings_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "r")
    logging.info(f"{settings_file.read()}")
    settings_file.close()
    return


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    if is_admin():
        pass
    else:
        showwarning(title="EasyMinecraftServer",
                    message="EasyMinecraftServer requires administrator privileges to run! Please run as administrator!")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)

    toaster = ToastNotifier()
    cwd = which("EasyMinecraftServer").replace("\\EasyMinecraftServer.EXE", "")
    if cwd == ".":
        cwd = os.getcwd()
        pass
    else:
        pass
    os.chdir(cwd)
    user_dir = os.path.expanduser("~")
    root = Tk()
    root.title("EasyMinecraftServer v2.15.0")
    root.geometry("510x390")
    root.iconbitmap(f"{cwd}\\mc.ico")
    root.bind("<Escape>", exit_program_event)
    root.bind("<Return>", start_server_event)
    root.bind("<Control-s>", start_server_event)
    root.bind("<Control-S>", start_server_event)
    root.bind("<Control-r>", reset_server_event)
    root.bind("<Control-R>", reset_server_event)
    root.bind("<F1>", help_window_event)
    root.bind("<F2>", license_window_event)
    root.bind("<F3>", backup_logs_event)
    root.bind("<F4>", uninstall_program_event)
    root.bind("<F5>", restart_program_event)
    root.bind("<F6>", update_event)
    root.bind("<F12>", debug_event)
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
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\")
        pass
    else:
        pass
    settings_good = settings_check()
    if settings_good:
        pass
    else:
        pass
    settings_json = json.load(open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "r"))
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log"):
        create_app_log = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log", 'x')
        create_app_log.close()
        pass
    else:
        pass
    try:
        log_bytes = open("{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log", "rb")
        with log_bytes as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
        if "Exiting Program" not in last_line and "Exiting for JDK Install" not in last_line and "Exiting Due To JDK Installation Denial" not in last_line and "Exiting EasyMinecraftServer" not in last_line and "Restarting EasyMinecraftServer" not in last_line and last_line != "" and not last_line.isspace() and "Restarting Program" not in last_line:
            showwarning(title="EasyMinecraftServer",
                        message="EasyMinecraftServer has detected that the program did not close properly last time it was run. Submitting a bug report on the github page is recommended and log files will now be backed up!")
            backup_logs()
            pass
    except OSError:
        pass
    log_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log", "w")
    try:
        log_file.truncate(0)
        pass
    except Exception:
        pass
    logging.basicConfig(filename=f'{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log', level="DEBUG",
                        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    logging.info("EasyMinecraftServer v2.15.0 Started")
    logging.info(f"Current Working Directory: {cwd}")
    logging.info(f"User Directory: {user_dir}")
    log_settings()
    logging.info("Building GUI")
    logging.info("Applying GUI theme")
    logging.info("Retreiving theme settings")
    app_theme = settings_json["theme"]
    if app_theme.upper() == "LIGHT":
        logging.info("Light Theme Selected")
        sv_ttk.use_light_theme()
        pass
    elif app_theme.upper() == "DARK":
        logging.info("Dark Theme Selected")
        sv_ttk.use_dark_theme()
        dark_title_bar()
        pass
    elif app_theme.upper() == "AUTO":
        logging.info("Auto Theme Selected")
        system_theme = darkdetect.theme()
        if system_theme.upper() == "DARK":
            logging.info("Dark Theme Detected")
            sv_ttk.use_dark_theme()
            dark_title_bar()
            pass
        elif system_theme.upper() == "LIGHT":
            logging.info("Light Theme Detected")
            sv_ttk.use_light_theme()
            pass
        else:
            logging.error("Auto Theme Failed")
            sv_ttk.use_light_theme()
            pass
        pass
    else:
        logging.error("Error getting theme settings")
        logging.error("Defaulting to light theme")
        sv_ttk.use_light_theme()
        pass
    menubar = Menu(root)
    main_menu = Menu(menubar, tearoff=0)
    main_menu.add_command(label="Help", command=help_window, underline=0)
    main_menu.add_command(label="Settings", command=settings, underline=0)
    main_menu.add_separator()
    main_menu.add_command(label="View ServerFiles", command=server_files, underline=0)
    main_menu.add_command(label="Server Backups", command=server_backups)
    main_menu.add_command(label="Backup Program", command=program_backup)
    main_menu.add_command(label="Restore Program", command=program_restore)
    main_menu.add_command(label="Reset Program", command=program_reset)
    main_menu.add_separator()
    main_menu.add_command(label="Changelog", command=changelog)
    main_menu.add_command(label="Update", command=update, underline=0)
    main_menu.add_command(label="Uninstall", command=uninstall_program)
    main_menu.add_command(label="Website", command=website, underline=0)
    main_menu.add_separator()
    main_menu.add_command(label="Create Anti-Virus Exclusions", command=av_exclusions)
    main_menu.add_command(label="Remove Anti-Virus Exclusions", command=av_exclusions_remove)
    main_menu.add_separator()
    main_menu.add_command(label="Restart", command=restart_program, underline=0)
    main_menu.add_command(label="Exit", command=exit_program, underline=0)
    menubar.add_cascade(label="Menu", menu=main_menu)
    root.config(menu=menubar)
    root.protocol("WM_DELETE_WINDOW", exit_program_force)
    loading_text = ttk.Label(root, text="Loading EasyMinecraftServer...")
    loading_text.place(relx=0.5, rely=0.5, anchor="center")
    root.update()
    try:
        logging.info("Checking for updates")
        url = "https://github.com/teekar2023/EasyMinecraftServer/releases/latest"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.15.0":
            new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
            logging.warning(f"New version available: {new_version}")
            toaster.show_toast("EasyMinecraftServer", f"New update available: {new_version}",
                               icon_path=f"{cwd}\\mc.ico",
                               threaded=True)
            loading_text.destroy()
            update_text = ttk.Label(root, text="New update available! Click the button below to update!")
            update_text.pack(pady=50)
            update_button = ttk.Button(root, text="Update", command=update_startup, style="Accent.TButton", width=50)
            update_button.pack(pady=10)
            continue_var = IntVar()
            continue_without_update_button = ttk.Button(root, text="Continue Without Updating", command=lambda: continue_var.set(1), width=50)
            continue_without_update_button.pack()
            root.update()
            root.wait_variable(continue_var)
            update_text.destroy()
            update_button.destroy()
            continue_without_update_button.destroy()
            loading_text = ttk.Label(root, text="Loading EasyMinecraftServer...")
            loading_text.place(relx=0.5, rely=0.5, anchor="center")
            root.update()
            pass
        else:
            logging.info("No new update available")
            file_path = f"{user_dir}\\Documents\\EasyMinecraftServer\\"
            file_list = os.listdir(file_path)
            for folder in file_list:
                if "Update" in folder:
                    logging.info(f"Deleting update folder: {user_dir}\\Documents\\EasyMinecraftServer\\{folder}")
                    rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\{folder}")
                    pass
                else:
                    pass
            pass
    except Exception as e:
        showerror(title="Error", message=f"Error while checking for updates: {e}")
        logging.error(f"Error while checking for updates: {e}")
        pass
    info = subprocess.STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    logging.info("Running ngrok update")
    subprocess.Popen([f"{cwd}\\ngrok\\ngrok.exe", "update"], startupinfo=info)
    logging.info("Finished running ngrok update")
    logging.info("Running ngrok config upgrade")
    subprocess.Popen([f"{cwd}\\ngrok\\ngrok.exe", "config", "upgrade"], startupinfo=info)
    logging.info("Finished running ngrok config upgrade")
    if os.path.exists(f"{cwd}\\ngrok\\.ngrok.exe.old"):
        logging.info("ngrok.exe.old found")
        logging.info("Removing ngrok.exe.old")
        try:
            os.remove(f"{cwd}\\ngrok\\.ngrok.exe.old")
            logging.info("Removed ngrok.exe.old")
            pass
        except Exception as e:
            logging.info(f"Failed to remove ngrok.exe.old: {e}")
            pass
        pass
    else:
        logging.info("ngrok.exe.old not found")
        pass
    logging.info("Creating ngrok secret")
    subprocess.Popen(["SecretManager.exe", "create"], startupinfo=info)
    logging.info("Finished creating ngrok secret")
    logging.info("Reading ngrok secret")
    ngrok_secret = str(os.environ.get("MinecraftServerNgrokSecret"))
    if settings_json["ngrok_authtoken"] == ngrok_secret:
        logging.warning("Authtoken for ngrok is the same as dev authtoken")
        pass
    else:
        logging.info("User authtoken does not match dev authtoken")
        pass
    logging.info("Removing ngrok secret")
    subprocess.Popen(["SecretManager.exe", "remove"], startupinfo=info)
    logging.info("Removed ngrok secret")
    p = subprocess.Popen(["powershell", "-Command",
                          f"Get-MpPreference | select-object -ExpandProperty ExclusionPath | Out-File -FilePath {user_dir}\\Documents\\EasyMinecraftServer\\Temp\\Paths.txt"],
                         startupinfo=info)
    logging.info("Ran ExclusionPath retriever")
    p2 = subprocess.Popen(["powershell", "-Command",
                           f"Get-MpPreference | select-object -ExpandProperty Exclusionprocess | Out-File -FilePath {user_dir}\\Documents\\EasyMinecraftServer\\Temp\\Processes.txt"],
                          startupinfo=info)
    logging.info("Ran ExclusionProcess retriever")
    logging.info("Waiting 3 seconds")
    time.sleep(3)
    logging.info("Finished waiting")
    logging.info("Reading exclusion paths from Paths.txt")
    try:
        exclusion_paths_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\Paths.txt", mode="r",
                                    encoding='utf-16-le')
        pass
    except Exception:
        loading_error_text = ttk.Label(root, text="Something went wrong. Please wait...")
        loading_error_text.place(relx=0.5, rely=0.7, anchor="center")
        root.update()
        time.sleep(5)
        loading_error_text.destroy()
        exclusion_paths_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\Paths.txt", mode="r",
                                    encoding='utf-16-le')
        pass
    exclusion_paths = exclusion_paths_file.read()
    exclusion_paths_file.close()
    try:
        os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\Paths.txt")
        pass
    except Exception as e:
        logging.error(f"Failed to remove temporary exclusion paths file: {e}")
        pass
    try:
        logging.warning(f"Exclusion Paths: {str(exclusion_paths)}")
        pass
    except Exception as e:
        logging.error(f"Failed to log exclusion paths: {e}")
        pass
    logging.info("Reading exclusion processes from Processes.txt")
    exclusion_processes_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\Processes.txt", mode="r",
                                    encoding='utf-16-le')
    exclusion_processes = exclusion_processes_file.read()
    exclusion_processes_file.close()
    try:
        os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\Processes.txt")
        pass
    except Exception as e:
        logging.error(f"Failed to remove temporary exclusion processes file: {e}")
        pass
    try:
        logging.warning(f"Exclusion Processes: {str(exclusion_processes)}")
        pass
    except Exception as e:
        logging.error(f"Failed to log exclusion processes: {e}")
        pass
    if "EasyMinecraftServer" not in str(exclusion_processes) or "mcserver" not in str(
            exclusion_processes) or "MinecraftServerGUI" not in str(
        exclusion_processes) or "MinecraftServer-nogui" not in str(exclusion_processes) or "java" not in str(
        exclusion_processes) or "javaw" not in str(exclusion_processes) or str(cwd) not in str(exclusion_paths) or str(
        user_dir) not in str(exclusion_paths):
        exclusion_prompt = askyesno(title="EasyMinecraftServer",
                                    message="It appears that you have not created all anti-virus exclusions for EasyMinecraftServer. Would you like to do this now?")
        if exclusion_prompt:
            logging.info("User chose to create exclusions on startup")
            av_exclusions()
            pass
        else:
            logging.info("User chose not to create exclusions on startup")
            pass
        pass
    else:
        logging.info("All exclusion paths and processes found")
        pass
    java_check = which("java")
    if java_check is None:
        logging.warning("JDK Not Found")
        install_jdk_ask = askyesno(title="JDK Required",
                                   message="Java Development Kit 17 Is Required To Run Minecraft Servers! Would You Like To "
                                           "Download/Install It Now?")
        if install_jdk_ask:
            try:
                os.startfile(f"{cwd}\\jdk17-installer.exe")
                logging.info("Launched JDK installer")
                pass
            except Exception:
                jdk_download_text = ttk.Label(root, text="Downloading JDK Installer...")
                jdk_download_text.place(relx=0.5, rely=0.6, anchor="center")
                logging.error("JDK installer not found. Downloading from website")
                logging.info("Downloading JDK installer")
                java_f = open(f"{cwd}\\jdk17-installer.exe", mode="wb")
                java_f2 = urllib.request.urlopen(
                    "https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe")
                while True:
                    java_data = java_f2.read()
                    if not java_data:
                        break
                    else:
                        java_f.write(java_data)
                        pass
                    pass
                java_f.close()
                logging.info("JDK installer downloaded")
                os.startfile(f"{cwd}\\jdk17-installer.exe")
                logging.info("Launched JDK installer")
                pass
            logging.warning("Exiting for JDK Install")
            exit_program_force()
            sys.exit(0)
        else:
            showerror(title="JDK Required",
                      message="Java Development Kit 17 Is Required! Please Install It And Restart "
                              "The Program!")
            logging.error("JDK Installation Denied!")
            logging.warning("Exiting Due To JDK Installation Denial")
            exit_program_force()
            sys.exit(0)
        pass
    else:
        logging.info(f"JDK Installation Found: {java_check}")
        try:
            os.remove(f"{cwd}\\jdk17-installer.exe")
            logging.info("Removed jdk17-installer.exe")
        except Exception as e:
            logging.error(f"Failed to remove jdk17-installer.exe: {e}")
            pass
        pass
    if os.path.exists(f"{cwd}\\JDK\\"):
        logging.info("JDK installer found")
        rmtree(f"{cwd}\\JDK\\")
        pass
    else:
        pass
    if os.path.exists(f"{cwd}\\1.8.9-recovery\\"):
        logging.info("1.8.9-Recovery Found")
        rmtree(f"{cwd}\\1.8.9-recovery\\")
        pass
    else:
        pass
    if os.path.exists(f"{cwd}\\1.12.2-recovery\\"):
        logging.info("1.12.2-Recovery Found")
        rmtree(f"{cwd}\\1.12.2-recovery\\")
        pass
    else:
        pass
    if os.path.exists(f"{cwd}\\1.16.5-recovery\\"):
        logging.info("1.16.5-Recovery Found")
        rmtree(f"{cwd}\\1.16.5-recovery\\")
        pass
    else:
        pass
    if os.path.exists(f"{cwd}\\1.17.1-recovery\\"):
        logging.info("1.17.1-Recovery Found")
        rmtree(f"{cwd}\\1.17.1-recovery\\")
        pass
    else:
        pass
    if os.path.exists(f"{cwd}\\1.18.1-recovery\\"):
        logging.info("1.18.1-Recovery Found")
        rmtree(f"{cwd}\\1.18.1-recovery\\")
        pass
    else:
        pass
    loading_text.destroy()
    root.update()
    main_text_label = ttk.Label(root, text="Easy Minecraft Server v2.15.0\n"
                                           "Github: https://github.com/teekar2023/EasyMinecraftServer\n"
                                           "Not In Any Way Affiliated With Minecraft, Mojang, Or Microsoft\n"
                                           f"Installation Directory: {cwd}\n"
                                           f"User Directory: {user_dir}\n"
                                           "Click Any Of The Following Buttons To Begin!")
    main_text_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    start_button = ttk.Button(root, text="Start Server", command=start_server, width="30", style="Accent.TButton")
    start_button.grid(row=1, column=0, padx=10, pady=10)
    create_backup_button = ttk.Button(root, text="Create Server Backup", command=create_server_backup, width="30")
    create_backup_button.grid(row=2, column=0, padx=10, pady=10)
    restore_backup_button = ttk.Button(root, text="Restore Server Backup", command=restore_server_backup, width="30")
    restore_backup_button.grid(row=3, column=0, padx=10, pady=10)
    manage_backups_button = ttk.Button(root, text="Manage Server Backups", command=manage_server_backups, width="30")
    manage_backups_button.grid(row=4, column=0, padx=10, pady=10)
    reset_server_button = ttk.Button(root, text="Reset Server", command=reset_server, width="30")
    reset_server_button.grid(row=5, column=0, padx=10, pady=10)
    use_custom_map_button = ttk.Button(root, text="Inject Custom Map", command=inject_custom_map, width="30")
    use_custom_map_button.grid(row=1, column=1, padx=10, pady=10)
    reset_dimension_button = ttk.Button(root, text="Reset Dimension", command=reset_dimension_main, width="30")
    reset_dimension_button.grid(row=2, column=1, padx=10, pady=10)
    change_server_properties_button = ttk.Button(root, text="Edit Server Properties",
                                                 command=change_server_properties, width="30")
    change_server_properties_button.grid(row=3, column=1, padx=10, pady=10)
    import_external_server_button = ttk.Button(root, text="Import External Server", command=import_external_server,
                                               width="30")
    import_external_server_button.grid(row=4, column=1, padx=10, pady=10)
    export_server_button = ttk.Button(root, text="Export Server", command=export_server, width="30")
    export_server_button.grid(row=5, column=1, padx=10, pady=10)
    root.update()
    logging.info("Starting Main Loop")
    root.mainloop()
    logging.info("Main Loop Ended")
    logging.warning("Exiting Program")
    logging.shutdown()
    PROCNAME = "EasyMinecraftServer.exe"
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()
            pass
        else:
            pass
        pass
    sys.exit(0)
