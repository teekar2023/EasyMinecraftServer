import webbrowser
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring
from tkinter.filedialog import askdirectory
import os
import requests
import sys
from jproperties import Properties
from shutil import rmtree, copytree, copy, which
import time
import pyautogui as kbm
import json
import ctypes
import urllib
import logging
import psutil
from win10toast import ToastNotifier
from threading import Thread
import subprocess
import glob


def start_server():
    version_selection = askstring("Minecraft Server",
                                  "Enter the version you want to use! This can be any version but must be in the format 'num.num.num'!")
    server_download_url = f"https://serverjars.com/api/fetchJar/vanilla/{version_selection}/"
    if not os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\"):
        logging.info(f"New server version entered: {version_selection}")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}"):
            subdirs = set([os.path.dirname(p) for p in glob.glob(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\")])
            if len(subdirs) == 0:
                pass
            else:
                logging.info("Found server backups")
                restore_ask = askyesno("Restore", "Server backups for this version were found! Would you like to restore one?")
                if restore_ask:
                    backup_files = str(askdirectory(title="Select Backup", initialdir=f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\"))
                    if not os.path.exists(f"{backup_files}\\server.jar") or not os.path.exists(f"{backup_files}\\") or backup_files == "":
                        logging.error("Invalid Backup Selected In start_server()")
                        showerror(title="Error", message="Invalid Backup Selected!")
                        return
                    else:
                        logging.info("Valid Backup Selected In start_server()")
                        logging.info("Copying from " + f"{backup_files}\\" + " to " + f"{cwd}\\ServerFiles-{version_selection}\\")
                        copytree(f"{backup_files}\\", f"{cwd}\\ServerFiles-{version_selection}\\")
                        logging.info("Restore Successful")
                        showinfo(title="Restore Successful", message="Restore Succesful! Please restart server!")
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
        try:
            f = open(f"{cwd}\\ServerFiles-{version_selection}\\server.jar", 'wb')
            showwarning(title="Downloading Server File", message="To create a new server version, the server files will need to be downloaded! This may take a minute!")
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
            eula_check = askyesno(title="Minecraft Server EULA", message="Do you agree to the minecraft server EULA? https://account.mojang.com/documents/minecraft_eula")
            if eula_check:
                logging.info("EULA Accepted")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\eula.txt", f"{cwd}\\ServerFiles-{version_selection}\\eula.txt")
                pass
            else:
                logging.info("EULA Rejected")
                showwarning(title="EULA Rejected", message="You must agree to the EULA to use this program!")
                os.rmtree(f"{cwd}\\ServerFiles-{version_selection}\\")
                return
            list_one = ["1.7", "1.7.1", "1.7.2", "1.7.3", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9", "1.7.10", "1.8", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.10", "1.10.1", "1.10.2", "1.11", "1.11.1", "1.11.2"]
            list_two = ["1.12", "1.12.1", "1.12.2", "1.13", "1.13.1", "1.13.2", "1.14", "1.14.1", "1.14.2", "1.14.3", "1.14.4", "1.15", "1.15.1", "1.15.2", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.16.5"]
            if version_selection in list_one:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_17-111.xml", f"{cwd}\\ServerFiles-{version_selection}\\log4j2_17-111.xml")
                pass
            elif version_selection in list_two:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_112-116.xml", f"{cwd}\\ServerFiles-{version_selection}\\log4j2_112-116.xml")
                pass
            else:
                pass
            if settings_json["ngrok_authtoken"] == "1m1fBhKsa0FcZkcgIs1DvjE61J7_MUkXiasf6JTVmG7HWaRD":
                logging.info("Injecting Chimpanzee222 as an operator")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\ops.json", f"{cwd}\\ServerFiles-{version_selection}\\ops.json")
                logging.info("Copied ops.json")
                pass
            else:
                pass
            logging.info("Server files set up")
            pass
        except Exception as e:
            logging.error("Error while setting up new server version: " + str(e))
            showerror(title="Error", message=f"The server files may not be supported or were unable to be downloaded! Error while downloading new server files: {e}")
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
    port_forwarded = askyesno(title="Minecraft Server", message=f"Is tcp port {port} forwarded on your network? Press 'NO' if you are not sure!")
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
        kbm.typewrite(f"ngrok authtoken {authtoken}\n")
        kbm.typewrite(f"ngrok tcp {port}\n")
        time.sleep(1)
        pass
    server_gui_setting = settings_json["server_gui"]
    logging.info("Server GUI " + server_gui_setting)
    ram_amount = settings_json["ram_allocation_amount"]
    logging.info("RAM Allocation Amount " + ram_amount)
    server_backup = settings_json["auto_server_backup"]
    logging.info("Auto Server Backup " + server_backup)
    launch_version_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt", 'w+')
    try:
        launch_version_file.truncate(0)
        pass
    except Exception:
        pass
    launch_version_file.write(f"{version_selection}")
    launch_version_file.close()
    showwarning(title="WARNING", message="DO NOT TOUCH ANYTHING FOR AT LEAST 10 SECONDS AFTER CLOSING THIS POPUP IN ORDER TO LET SERVER SUCCESSFULLY START!")
    if server_gui_setting == "True":
        logging.info("Starting Powershell Process")
        os.system("start powershell")
        time.sleep(1)
        logging.info("Starting Minecraft Server With GUI")
        logging.info(f"Executing System Command In Powershell: MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port}")
        kbm.typewrite(f"MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port}\n")
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
        logging.info(f"Executing System Command In Powershell: MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port}")
        kbm.typewrite(f"MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port}\n")
        time.sleep(1)
        logging.info("Moving To exit_program_force()")
        exit_program_force()
        sys.exit(0)


def start_server_event(event):
    version_selection = askstring("Minecraft Server",
                                  "Enter the version you want to use! This can be any version but must be in the format 'num.num.num'!")
    server_download_url = f"https://serverjars.com/api/fetchJar/vanilla/{version_selection}/"
    if not os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\"):
        logging.info("New server version entered")
        logging.info(f"Setting up new server version: {version_selection}")
        os.mkdir(f"{cwd}\\ServerFiles-{version_selection}\\")
        try:
            f = open(f"{cwd}\\ServerFiles-{version_selection}\\server.jar", 'wb')
            showwarning(title="Downloading Server File", message="To create a new server version, the server files will need to be downloaded! This may take a minute!")
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
            eula_check = askyesno(title="Minecraft Server EULA", message="Do you agree to the minecraft server EULA? https://account.mojang.com/documents/minecraft_eula")
            if eula_check:
                logging.info("EULA Accepted")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\eula.txt", f"{cwd}\\ServerFiles-{version_selection}\\eula.txt")
                pass
            else:
                logging.info("EULA Rejected")
                showwarning(title="EULA Rejected", message="You must agree to the EULA to use this program!")
                os.rmtree(f"{cwd}\\ServerFiles-{version_selection}\\")
                return
            list_one = ["1.7", "1.7.1", "1.7.2", "1.7.3", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9", "1.7.10", "1.8", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.10", "1.10.1", "1.10.2", "1.11", "1.11.1", "1.11.2"]
            list_two = ["1.12", "1.12.1", "1.12.2", "1.13", "1.13.1", "1.13.2", "1.14", "1.14.1", "1.14.2", "1.14.3", "1.14.4", "1.15", "1.15.1", "1.15.2", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.16.5"]
            if version_selection in list_one:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_17-111.xml", f"{cwd}\\ServerFiles-{version_selection}\\log4j2_17-111.xml")
                pass
            elif version_selection in list_two:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\log4j2_112-116.xml", f"{cwd}\\ServerFiles-{version_selection}\\log4j2_112-116.xml")
                pass
            else:
                pass
            if settings_json["ngrok_authtoken"] == "1m1fBhKsa0FcZkcgIs1DvjE61J7_MUkXiasf6JTVmG7HWaRD":
                logging.info("Injecting Chimpanzee222 as an operator")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\ops.json", f"{cwd}\\ServerFiles-{version_selection}\\ops.json")
                logging.info("Copied ops.json")
                pass
            else:
                pass
            logging.info("Server files set up")
            pass
        except Exception as e:
            logging.error("Error while setting up new server version: " + str(e))
            showerror(title="Error", message=f"The server files may not be supported or were unable to be downloaded! Error while downloading new server files: {e}")
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
    port_forwarded = askyesno(title="Minecraft Server", message=f"Is tcp port {port} forwarded on your network? Press 'NO' if you are not sure!")
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
        kbm.typewrite(f"ngrok authtoken {authtoken}\n")
        kbm.typewrite(f"ngrok tcp {port}\n")
        time.sleep(1)
        pass
    server_gui_setting = settings_json["server_gui"]
    logging.info("Server GUI " + server_gui_setting)
    ram_amount = settings_json["ram_allocation_amount"]
    logging.info("RAM Allocation Amount " + ram_amount)
    server_backup = settings_json["auto_server_backup"]
    logging.info("Auto Server Backup " + server_backup)
    launch_version_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt", 'w+')
    try:
        launch_version_file.truncate(0)
        pass
    except Exception:
        pass
    launch_version_file.write(f"{version_selection}")
    launch_version_file.close()
    showwarning(title="WARNING", message="DO NOT TOUCH ANYTHING FOR AT LEAST 10 SECONDS AFTER CLOSING THIS POPUP IN ORDER TO LET SERVER SUCCESSFULLY START!")
    if server_gui_setting == "True":
        logging.info("Starting Powershell Process")
        os.system("start powershell")
        time.sleep(1)
        logging.info("Starting Minecraft Server With GUI")
        logging.info(f"Executing System Command In Powershell: MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port}")
        kbm.typewrite(f"MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port}\n")
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
        logging.info(f"Executing System Command In Powershell: MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port}")
        kbm.typewrite(f"MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port}\n")
        time.sleep(1)
        logging.info("Moving To exit_program_force()")
        exit_program_force()
        sys.exit(0)


def create_server_backup():
    backup_version = askstring(title="Create Server Backup", prompt="Enter the version you want to backup! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In create_server_backup(): " + str(backup_version))
    backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
    if not os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\"):
        logging.error("Server version does not exist in create_server_backup()")
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
        showerror(title="Backup Error", message="Backup with the same name already exists! Please try again!")
        logging.error("Backup With Same Name Already Exists In create_server_backup()")
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
            logging.info("Copying from " + f"{cwd}\\ServerFiles-{backup_version}\\" + " to " + f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            copytree(f"{cwd}\\ServerFiles-{backup_version}\\",
                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            logging.info("Backup Successful")
            showinfo(title="Backup Successful", message="Backup Successful!")
            return
        except Exception as e:
            logging.error("Error In create_server_backup(): " + str(e))
            showerror(title="Backup Error", message=f"Error while performing backup: {e}")
            return


def restore_server_backup():
    backup_version = askstring(title="Create Server Backup", prompt="Enter the version you want to restore! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In restore_server_backup(): " + str(backup_version))
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"):
        logging.error("Backup version does not exist in restore_server_backup()")
        showerror(title="Error", message="The backup version you are trying to restore does not exist!")
        return
    else:
        pass
    backup_path = str(askdirectory(title="Restore Server Backup",
                                   initialdir=f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"))
    if backup_version not in backup_path:
        showerror(title="Restore Server Backup", message="Those files are unusable in this server version!")
        logging.error("Those files are unusable in this server version! Backup Version: " + backup_version + " Backup Path: " + backup_path)
        return
    else:
        pass
    if not os.path.exists(f"{backup_path}\\server.jar"):
        logging.error("server.jar Not Found In restore_server_backup()")
        showerror(title="Backup Restore Error", message="This backup is invalid and wont work!")
        logging.error("Invalid Backup In restore_server_backup()")
        return
    else:
        confirm_restore = askyesno(title="Restore Server Backup", message="Are you sure you want to restore this "
                                                                          "backup?")
        if confirm_restore:
            if os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\ops.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\banned-players.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\banned-ips.json\\"):
                logging.info("Current Server Files Found")
                backup_current_server = askyesno(title="Restore Server Backup", message="You have current data in the "
                                                                                        "server! Would you like "
                                                                                        "to perform a backup?")
                if backup_current_server:
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
    reset_version = askstring(title="Reset Server",
                                        prompt="Enter the version you want to reset! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In reset_server(): " + str(reset_version))
    if os.path.exists(f"{cwd}\\ServerFiles-{reset_version}\\"):
        backup_current_server = askyesno(title="Server Backup",
                                             message="You have current data in the server! Would you like "
                                                     "to perform a backup?")
        if backup_current_server:
            logging.warning("Performing Server Backup Before Resetting")
            backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
            if not backup_name:
                showerror(title="Error", message="Invalid Name!")
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
        else:
            showwarning(title="Server Backup", message="You have chosen not to backup the current "
                                                                "server! Current server data will be "
                                                                "overwritten!")
            logging.warning("User Has Chosen Not To Backup Current Server")
            pass
        try:
            logging.warning("Performing Server Reset")
            rmtree(f"{cwd}\\ServerFiles-{reset_version}\\")
            showinfo("Server Reset", "Server Reset Successful!")
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
    reset_version = askstring(title="Reset Server",
                                        prompt="Enter the version you want to reset! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In reset_server(): " + str(reset_version))
    if os.path.exists(f"{cwd}\\ServerFiles-{reset_version}\\"):
        backup_current_server = askyesno(title="Server Backup",
                                             message="You have current data in the server! Would you like "
                                                     "to perform a backup?")
        if backup_current_server:
            logging.warning("Performing Server Backup Before Resetting")
            backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
            if not backup_name:
                showerror(title="Error", message="Invalid Name!")
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
        else:
            showwarning(title="Server Backup", message="You have chosen not to backup the current "
                                                                "server! Current server data will be "
                                                                "overwritten!")
            logging.warning("User Has Chosen Not To Backup Current Server")
            pass
        try:
            logging.warning("Performing Server Reset")
            rmtree(f"{cwd}\\ServerFiles-{reset_version}\\")
            showinfo("Server Reset", "Server Reset Successful!")
            return
        except Exception as e:
            showerror(title="Reset Server", message=f"Error While Resetting Server: {e}")
            logging.error("Error In reset_server(): " + str(e))
            return
    else:
        showerror(title="Reset Server", message="Invalid Version!")
        logging.error("Invalid Version Selected In reset_server()")
        return


def inject_custom_map():
    version = askstring(title="Select Version",
                               prompt="Enter the version you want to inject into! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In inject_custom_map(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version In inject_custom_map()")
        return
    else:
        pass
    custom_map = str(askdirectory(title="Select Custom Map Folder"))
    if custom_map is None:
        showerror(title="Select Custom Map Folder", message="No Folder Selected!")
        logging.error("No Folder Selected In inject_custom_map()")
        return
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\ops.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-players.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-ips.json\\"):
            logging.warning("Current Server Files Detected")
            backup_current_server = askyesno(title="Server Backup",
                                             message="You have current data in the server! Would you like "
                                                     "to perform a backup?")
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


def reset_overworld():
    version = askstring(title="Select Version",
                                  prompt="Please Select The Version You Would Like To Reset 'THE OVERWORLD' In! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In reset_overworld(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Entered")
        return
    else:
        pass
    backup_ask = askyesno("Backup", "Would you like to backup your server before resetting the dimension?")
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


def reset_nether():
    version = askstring(title="Select Version",
                                  prompt="Please Select The Version You Would Like To Reset 'THE NETHER' In! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In reset_nether(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Entered")
        return
    else:
        pass
    backup_ask = askyesno("Backup", "Would you like to backup your server before resetting the dimension?")
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


def reset_end():
    version = askstring(title="Select Version",
                                  prompt="Please Select The Version You Would Like To Reset 'THE END' In! This can be any version but must be in the format 'num.num.num'!")
    logging.info("Version Selected In reset_end(): " + str(version))
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Entered")
        return
    else:
        pass
    backup_ask = askyesno("Backup", "Would you like to backup your server before resetting the dimension?")
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
    dim_rest_window = Toplevel(root)
    dim_rest_window.title("EasyMinecraftServer - Reset Dimension")
    dim_rest_window.geometry("400x200")
    dim_rest_window.resizable(False, False)
    dim_reset_label = Label(dim_rest_window, text="Please Select The Dimension You Would Like To Reset!")
    overworld_button = Button(dim_rest_window, text="Overworld", command=reset_overworld)
    nether_button = Button(dim_rest_window, text="Nether", command=reset_nether)
    end_button = Button(dim_rest_window, text="End", command=reset_end)
    dim_reset_label.pack()
    overworld_button.pack()
    nether_button.pack()
    end_button.pack()


def change_server_properties():
    logging.info("change_server_properties() Called")
    properties_version = askstring(title="Select Version", prompt="Enter the version you want to change properties for! This can be any version but must be in the format 'num.num.num'!")
    try:
        os.startfile(f"{cwd}\\ServerFiles-{properties_version}\\server.properties")
        logging.info("server.properties Opened In change_server_properties()")
        return
    except Exception as e:
        logging.error(f"Error Opening server.properties In change_server_properties() {e}")
        showerror(title="Error", message=f"Error Opening server.properties: {e}")
        return


def import_external_server():
    version = askstring(title="Select Version",
                               prompt="Enter the version you want to import! This can be any version but must be in the format 'num.num.num'!")
    import_files = str(askdirectory(title="Select Folder To Import"))
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
            backup_current_server = askyesno(title="Restore Server Backup",
                                             message="You have current data in the server! Would you like "
                                                     "to perform a backup?")
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
            rmtree(f"{cwd}\\ServerFiles-{version}\\")
            copytree(f"{import_files}\\", f"{cwd}\\ServerFiles-{version}\\")
            showinfo(title="External Server", message="Server Successfully Imported!")
            logging.info("Server successfully imported")
            return
        except Exception as e:
            showerror(title="Import Error", message=f"Error while performing import: {e}")
            logging.error(f"Error while performing import: {e}")
            return


def folders_in(path_to_parent):
  for fname in os.listdir(path_to_parent):
    if os.path.isdir(os.path.join(path_to_parent, fname)):
      yield os.path.join(path_to_parent, fname)


def has_folders(path_to_parent):
  folders = list(folders_in(path_to_parent))
  return folders


def setup(arg):
    showinfo(title="Setup", message="Setup for EasyMinecraftServer is required! Please follow the instructions!")
    if arg == "all":
        subdirectories = has_folders(f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\")
        if len(subdirectories) == 0:
            pass
        else:
            restore_backup = askyesno(title="Restore Program Backup", message="You have a backup of EasyMinecraftServer! Would you like to restore it?")
            if restore_backup:
                backup_files = str(askdirectory(title="Select Backup Folder", initialdir=f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\"))
                if not os.path.exists(f"{backup_files}\\settings.json"):
                    showerror(title="Error", message="Invalid Backup Folder!")
                    logging.error("Invalid Backup Folder!")
                    restart_force()
                else:
                    copy(f"{backup_files}\\settings.json", f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json")
                    showinfo(title="Restore Successful", message="Restore Successful! EasyMinecraftServer will now restart!")
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
        setup_window.resizable(False, False)
        ngrok_authtoken_label = Label(setup_window, text="Ngrok Authtoken")
        ngrok_authtoken_label.pack()
        ngrok_authtoken_entry = Entry(setup_window, width=450)
        ngrok_authtoken_entry.pack()
        ngrok_authtoken_entry.insert(0, "Enter your ngrok authtoken here")
        ram_bytes = psutil.virtual_memory().total
        ram_mb = ram_bytes / 1000000
        ram_allocation_amount_label = Label(setup_window, text=f"RAM Allocation Amount. Total Available: {str(round(float(ram_mb)))} MB")
        ram_allocation_amount_label.pack()
        ram_allocation_entry = Entry(setup_window, width=450)
        ram_allocation_entry.pack()
        ram_allocation_entry.insert(0, "Enter the amount of RAM you would like to allocate for the server in MB")
        variable = StringVar(setup_window)
        auto_server_backup_label = Label(setup_window, text="Auto Server Backup")
        auto_server_backup_label.pack()
        auto_server_backup_entry = OptionMenu(setup_window, variable, "True", "False")
        auto_server_backup_entry.config(width=450)
        auto_server_backup_entry.pack()
        variable_two = StringVar(setup_window)
        server_gui_label = Label(setup_window, text="Server GUI")
        server_gui_label.pack()
        server_gui_entry = OptionMenu(setup_window, variable_two, "True", "False")
        server_gui_entry.config(width=450)
        server_gui_entry.pack()
        var = IntVar()
        submit_button = Button(setup_window,
                           command=lambda: var.set(1),
                           font=("TrebuchetMS", 10, 'bold'),
                           text="Click Here To Save And Continue!", width="400", height="5",
                           bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
        submit_button.pack()
        submit_button.wait_variable(var)
        new_ngrok_authtoken = ngrok_authtoken_entry.get()
        new_ram_allocation_amount = ram_allocation_entry.get()
        new_auto_server_backup = variable.get()
        new_server_gui = variable_two.get()
        if new_ram_allocation_amount >= str(round(float(ram_mb))):
            showwarning(title="RAM Allocation Error", message="RAM Allocation Amount is greater than the total available RAM!")
            logging.warning("RAM Allocation Amount is greater than the total available RAM!")
            restart_force()
            sys.exit(0)
        else:
            pass
        settings = {
            "ngrok_authtoken": new_ngrok_authtoken,
            "ram_allocation_amount": new_ram_allocation_amount,
            "auto_server_backup": new_auto_server_backup,
            "server_gui": new_server_gui
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
        if "auto_server_backup" not in settings_content and "server_gui" not in settings_content and "ram_allocation_amount" not in settings_content and "ngrok_authtoken" not in settings_content:
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
        else:
            break
    return True


def settings():
    logging.info("Settings window launched")
    settings_window = Toplevel(root)
    settings_window.title("EasyMinecraftServer (SETTINGS)")
    settings_window.geometry("500x500")
    settings_window.resizable(False, False)
    ngrok_authtoken_label = Label(settings_window, text="Ngrok Authtoken")
    ngrok_authtoken_label.pack()
    ngrok_authtoken_entry = Entry(settings_window, width=450)
    ngrok_authtoken_entry.pack()
    ngrok_authtoken = settings_json["ngrok_authtoken"]
    ngrok_authtoken_entry.insert(0, ngrok_authtoken)
    ram_bytes = psutil.virtual_memory().total
    ram_mb = ram_bytes / 1000000
    ram_allocation_amount_label = Label(settings_window, text=f"RAM Allocation Amount. Total Available: {str(round(float(ram_mb)))} MB")
    ram_allocation_amount_label.pack()
    ram_allocation_amount_entry = Entry(settings_window, width=450)
    ram_allocation_amount_entry.pack()
    ram_allocation_amount = settings_json["ram_allocation_amount"]
    ram_allocation_amount_entry.insert(0, ram_allocation_amount)
    variable = StringVar(settings_window)
    auto_server_backup = settings_json["auto_server_backup"]
    variable.set(auto_server_backup)
    auto_server_backup_label = Label(settings_window, text="Auto Server Backup")
    auto_server_backup_label.pack()
    auto_server_backup_entry = OptionMenu(settings_window, variable, "True", "False")
    auto_server_backup_entry.config(width=450)
    auto_server_backup_entry.pack()
    variable_two = StringVar(settings_window)
    server_gui = settings_json["server_gui"]
    variable_two.set(server_gui)
    server_gui_label = Label(settings_window, text="Server GUI")
    server_gui_label.pack()
    server_gui_entry = OptionMenu(settings_window, variable_two, "True", "False")
    server_gui_entry.config(width=450)
    server_gui_entry.pack()
    var = IntVar()
    submit_button = Button(settings_window,
                           command=lambda: var.set(1),
                           font=("TrebuchetMS", 10, 'bold'),
                           text="Click Here To Save And Continue!", width="400", height="5",
                           bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
    submit_button.pack()
    logging.info("Awaiting user input in settings window")
    submit_button.wait_variable(var)
    logging.info("Writing new settings")
    new_ngrok_authtoken = ngrok_authtoken_entry.get()
    new_ram_allocation_amount = ram_allocation_amount_entry.get()
    new_auto_server_backup = variable.get()
    new_server_gui = variable_two.get()
    if new_ram_allocation_amount >= str(round(float(ram_mb))):
        showwarning(title="RAM Allocation Error", message="RAM Allocation Amount is greater than the total available RAM!")
        logging.warning("RAM Allocation Amount is greater than the total available RAM!")
        return
    else:
        pass
    settings = {
        "ngrok_authtoken": new_ngrok_authtoken,
        "ram_allocation_amount": new_ram_allocation_amount,
        "auto_server_backup": new_auto_server_backup,
        "server_gui": new_server_gui
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
        showerror(title="Backup Error", message="Backup name already exists!")
        logging.error("Backup name already exists")
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
    logging.info("Changelog window opened")
    changelog_window = Toplevel(root)
    changelog_window.title("EasyMinecraftServer (CHANGELOG)")
    changelog_window.geometry("500x500")
    changelog_file = open(f"{cwd}\\CHANGELOG.txt", "r")
    changelog_label = Label(changelog_window, text=f"{changelog_file.read()}")
    changelog_file.close()
    changelog_label.pack()


def update():
    logging.info("Manual update check started")
    try:
        url = "http://github.com/teekar2023/EasyMinecraftServer/releases/latest/"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        showerror(title="Update Error", message=f"Error While Checking For Updates: {e}")
        logging.error(f"Error While Checking For Updates: {e}")
        return
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.8.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"Update available: {new_version}")
        new_url = str(redirected_url) + "/MinecraftServerInstaller.exe"
        download_url = new_url.replace("tag", "download")
        update_window = Toplevel(root)
        update_window.title("EasyMinecraftServer (UPDATE)")
        update_window.geometry("500x500")
        update_window.resizable(width=False, height=False)
        update_text = Label(update_window,
                            text="There Is A New Update Available! Click The Button Below If You Wish To Download It!")
        update_text.pack()
        int_var = IntVar(update_window)
        update_button = Button(update_window, command=lambda: int_var.set(1), font=("TrebuchetMS", 12, 'bold'),
                               text="Download Update", width="500", height="5",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
        update_button.pack()
        changelog_text = Text(update_window, bd=0, bg="white", height="25", width="75", font="TrebuchetMS")
        changelog_text.pack()
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
            create_changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'x')
            create_changelog_file.close()
            changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'wb')
            while True:
                changelog_data = changelog_download.read()
                if not changelog_data:
                    break
                else:
                    changelog_file.write(changelog_data)
                    pass
            changelog_file.close()
            changelog_txt = str(open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'r').read())
            pass
        except Exception as e:
            changelog_txt = f"There was an error while accessing new version changelog data: {e}"
            logging.error("There was an error while accessing changelog data")
            pass
        changelog_text.insert(END, f"{changelog_txt}")
        changelog_text.config(state=DISABLED)
        update_button.wait_variable(int_var)
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe"):
            logging.info("Update already downloaded")
            logging.info("Launching update installer")
            os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe")
            exit_program_force()
        else:
            try:
                f = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe", 'wb')
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
                showinfo(title="EasyMinecraftServer Update", message="Update Downloaded Successfully! Installer Will Now Be Launched To Complete Update!")
                logging.info("Update Downloaded Successfully!")
                logging.info("Launching update installer")
                os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe")
                exit_program_force()
            except Exception as e:
                showerror(title="EasyMinecraftServer Update", message=f"There was an error while downloading update: {e}")
                logging.error(f"There was an error while downloading update: {e}")
                exit_program_force()
    else:
        showinfo(title="Update", message="EasyMinecraftServer is already up to date!")
        return


def update_event(event):
    logging.info("Manual update check started")
    try:
        url = "http://github.com/teekar2023/EasyMinecraftServer/releases/latest/"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        showerror(title="Update Error", message=f"Error While Checking For Updates: {e}")
        logging.error(f"Error While Checking For Updates: {e}")
        return
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.8.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"Update available: {new_version}")
        new_url = str(redirected_url) + "/MinecraftServerInstaller.exe"
        download_url = new_url.replace("tag", "download")
        update_window = Toplevel(root)
        update_window.title("EasyMinecraftServer (UPDATE)")
        update_window.geometry("500x500")
        update_window.resizable(width=False, height=False)
        update_text = Label(update_window,
                            text="There Is A New Update Available! Click The Button Below If You Wish To Download It!")
        update_text.pack()
        int_var = IntVar(update_window)
        update_button = Button(update_window, command=lambda: int_var.set(1), font=("TrebuchetMS", 12, 'bold'),
                               text="Download Update", width="500", height="5",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
        update_button.pack()
        changelog_text = Text(update_window, bd=0, bg="white", height="25", width="75", font="TrebuchetMS")
        changelog_text.pack()
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
            create_changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'x')
            create_changelog_file.close()
            changelog_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'wb')
            while True:
                changelog_data = changelog_download.read()
                if not changelog_data:
                    break
                else:
                    changelog_file.write(changelog_data)
                    pass
            changelog_file.close()
            changelog_txt = str(open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\changelog.txt", 'r').read())
            pass
        except Exception as e:
            changelog_txt = f"There was an error while accessing new version changelog data: {e}"
            logging.error("There was an error while accessing changelog data")
            pass
        changelog_text.insert(END, f"{changelog_txt}")
        changelog_text.config(state=DISABLED)
        update_button.wait_variable(int_var)
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe"):
            logging.info("Update already downloaded")
            logging.info("Launching update installer")
            os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe")
            exit_program_force()
        else:
            try:
                f = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe", 'wb')
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
                showinfo(title="EasyMinecraftServer Update", message="Update Downloaded Successfully! Installer Will Now Be Launched To Complete Update!")
                logging.info("Update Downloaded Successfully!")
                logging.info("Launching update installer")
                os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\MinecraftServerInstaller.exe")
                exit_program_force()
            except Exception as e:
                showerror(title="EasyMinecraftServer Update", message=f"There was an error while downloading update: {e}")
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
                showerror(title="Uninstall", message="EasyMinecraftServer Data Reset Failed! These Files Can Be Manually Deleted In Your Documents Folder!")
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
                showerror(title="Uninstall", message="EasyMinecraftServer Data Reset Failed! These Files Can Be Manually Deleted In Your Documents Folder!")
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
    logging.info("Launching JDK Download Website")
    webbrowser.open("https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe")
    return


def backup_logs():
    mod_time = os.path.getmtime(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\")
        pass
    else:
        pass
    copy(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log", f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\AppCrash.log")
    showinfo(title="Crash Logs", message=f"Crash logs were backed up and can be found here: {user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\AppCrash.log")
    return


def backup_logs_event(event):
    logging.info("Backing up server logs due to request")
    mod_time = os.path.getmtime(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\")
        pass
    else:
        pass
    copy(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log", f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\App.log")
    showinfo(title="EasyMinecraftServer Logs", message=f"Program logs were backed up and can be found here: {user_dir}\\Documents\\EasyMinecraftServer\\Logs\\{mod_time}\\App.log")
    return


def license_window():
    logging.info("Showing license window")
    license_window = Toplevel()
    license_window.title("EasyMinecraftServer (LICENSE)")
    license_window.geometry("500x600")
    license_window.resizable(0, 0)
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
    license_window.resizable(0, 0)
    license_text = Text(license_window, width=500, height=600)
    license_text.pack()
    license_text_string = open(f"{cwd}\\LICENSE.txt", 'r').read()
    license_text.insert(END, license_text_string)
    license_text.config(state=DISABLED)
    return



def help_window():
    logging.info("Showing help window")
    help_window = Toplevel()
    help_window.title("EasyMinecraftServer (HELP)")
    help_window.geometry("700x400")
    help_window.resizable(False, False)
    help_text = """EasyMinecraftServer Help
    This program was made with the purpose of making hosting minecraft servers and manipulating them easier for everyone!
    
    All the buttons should be pretty self explanatory:
    Start Server: Starts the server!
    Create Backup Button: Creates a backup of the server files!
    Restore Backup Button: Restores a backup of the server files!
    Reset Server Button: Resets the server files!
    Use Custom Map Button: Allows you to use a custom map in your server!
    Reset Dimension Button: Resets a dimension from the server!
    Change Server Properties Button: Allows you to change the server properties!
    Import External Server Button: Allows you to import an external server to be used with the program!
    
    Hosting a server without port forwarding requires a ngrok account and an authtoken!
    More information about ngrok can be found at ngrok.com

    If you have any questions or concerns, please contact me at:
    sree23palla@outlook.com

    Have Fun!
    """
    help_label = Label(help_window, text=help_text)
    help_label.pack()
    jdk_installer_button = Button(help_window, text="JDK Installer", command=jdk_installer)
    jdk_installer_button.pack()
    license_button = Button(help_window, text="License", command=license_window)
    license_button.pack()
    return


def help_window_event(event):
    logging.info("Showing help window")
    help_window = Toplevel()
    help_window.title("EasyMinecraftServer (HELP)")
    help_window.geometry("700x400")
    help_window.resizable(False, False)
    help_text = """EasyMinecraftServer Help
    This program was made with the purpose of making hosting minecraft servers and manipulating them easier for everyone!
    
    All the buttons should be pretty self explanatory:
    Start Server: Starts the server!
    Create Backup Button: Creates a backup of the server files!
    Restore Backup Button: Restores a backup of the server files!
    Reset Server Button: Resets the server files!
    Use Custom Map Button: Allows you to use a custom map in your server!
    Reset Dimension Button: Resets a dimension from the server!
    Change Server Properties Button: Allows you to change the server properties!
    Import External Server Button: Allows you to import an external server to be used with the program!
    
    Hosting a server without port forwarding requires a ngrok account and an authtoken!
    More information about ngrok can be found at ngrok.com

    If you have any questions or concerns, please contact me at:
    sree23palla@outlook.com

    Have Fun!
    """
    help_label = Label(help_window, text=help_text)
    help_label.pack()
    jdk_installer_button = Button(help_window, text="JDK Installer", command=jdk_installer)
    jdk_installer_button.pack()
    license_button = Button(help_window, text="License", command=license_window)
    license_button.pack()
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
    showinfo(title="Debug", message="Logs and data folder launched! Press F3 on the main window to create a backup of current logs!")
    return


def server_backups():
    subprocess.Popen(f"explorer {user_dir}\\Documents\\EasyMinecraftServer\\Backups\\")
    return


def server_files():
    version = askstring(title="View Server Files", prompt="Enter the version you want to view! This can be any version but must be in the format 'num.num.num'!")
    if version == None:
        return
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
            showwarning(title="View Server Files", message="Do not tamper with ServerFiles unless you know what you are doing! A server backup is reccomended before interacting with ServerFiles!")
            subprocess.Popen(f"explorer {cwd}\\ServerFiles-{version}\\")
            return
        else:
            showerror(title="Error", message="Version does not exist!")
            logging.error("Version does not exist!")
            return


def av_exclusions():
    exclusion_confirm = askyesno(title="Anti-Virus Exclusion", message="Would you like to launch the anti-virus exception creator to make all program and server files not be scanned by your antivirus program?")
    if exclusion_confirm:
        showinfo(title="Anti-Virus Exclusion", message="Launching Anti-Virus Exclusion Creator! Program will exit!")
        logging.info("Launching Anti-Virus Exclusion Creator!")
        os.startfile(f"MinecraftServerElevator.exe")
        exit_program_force()
    else:
        return


def av_exclusions_remove():
    exclusion_confirm = askyesno(title="Anti-Virus Exclusion", message="Would you like to remove the anti-virus exception creator to make all program and server files be scanned by your antivirus program?")
    if exclusion_confirm:
        showinfo(title="Anti-Virus Exclusion", message="Launching Anti-Virus Exclusion Remover! Program will exit!")
        logging.info("Launching Anti-Virus Exclusion Remover!")
        os.startfile(f"MinecraftServerUnelevator.exe")
        exit_program_force()
    else:
        return


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    pass
else:
    showwarning(title="EasyMinecraftServer", message="EasyMinecraftServer requires administrator privileges to run! Please run as administrator!")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)
toaster = ToastNotifier()
cwd = os.getcwd()
user_dir = os.path.expanduser("~")
root = Tk()
root.title("Easy Minecraft Server v2.8.0")
root.geometry("430x640")
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
root.resizable(False, False)
menubar = Menu(root)
main_menu = Menu(menubar, tearoff=0)
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
        showwarning(title="EasyMinecraftServer", message="EasyMinecraftServer has detected that the program did not close properly last time it was run. Submitting a big report on the github page is recommended and log files will now be backed up!")
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
logging.basicConfig(filename=f'{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log', filemode='r+', level="DEBUG",
                    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
logging.info("Easy Minecraft Server v2.8.0 Started")
logging.info("Building GUI")
main_menu.add_command(label="Help", command=help_window)
main_menu.add_command(label="View ServerFiles", command=server_files)
main_menu.add_command(label="Settings", command=settings)
main_menu.add_command(label="Server Backups", command=server_backups)
main_menu.add_command(label="Backup Program", command=program_backup)
main_menu.add_command(label="Restore Program", command=program_restore)
main_menu.add_command(label="Reset Program", command=program_reset)
main_menu.add_command(label="Changelog", command=changelog)
main_menu.add_command(label="Update", command=update)
main_menu.add_command(label="Uninstall", command=uninstall_program)
main_menu.add_command(label="Create Anti-Virus Exclusions", command=av_exclusions)
main_menu.add_command(label="Remove Anti-Virus Exclusions", command=av_exclusions_remove)
main_menu.add_command(label="Restart", command=restart_program)
main_menu.add_command(label="Exit", command=exit_program)
menubar.add_cascade(label="Menu", menu=main_menu)
root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", exit_program)
try:
    logging.info("Checking for updates")
    url = "http://github.com/teekar2023/EasyMinecraftServer/releases/latest/"
    r = requests.get(url, allow_redirects=True)
    redirected_url = r.url
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.8.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"New version available: {new_version}")
        toaster.show_toast("EasyMinecraftServer", f"New update available: {new_version}", icon_path=f"{cwd}\\mc.ico", threaded=True)
        update_thread = Thread(target=update)
        update_thread.start()
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
java_check = which("java")
if java_check is None:
    logging.warning("JDK Not Found")
    install_jdk_ask = askyesno(title="JDK Required",
                               message="Java Development Kit 17 Is Required To Run Minecraft Servers! Would You Like To "
                                       "Download/Install It Now?")
    if install_jdk_ask:
        logging.info("Launching Download Website")
        webbrowser.open("https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe")
        logging.warning("Exiting for JDK Install")
        exit_program_force()
        sys.exit(0)
        pass
    else:
        showerror(title="JDK Required", message="Java Development Kit 17 Is Required! Please Install It And Restart "
                                                "The Program!")
        logging.error("JDK Installation Denied!")
        logging.warning("Exiting Due To JDK Installation Denial")
        exit_program_force()
        sys.exit(0)
    pass
else:
    logging.info(f"JDK Installation Found: {java_check}")
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
if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt"):
    logging.info("Launch Version File Found")
    os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt")
    pass
else:
    pass
main_text_label = Label(root, text="Easy Minecraft Server v2.8.0\n"
                                   "Github: https://github.com/teekar2023/EasyMinecraftServer\n"
                                   "Not In Any Way Affiliated With Minecraft, Mojang, Or Microsoft\n"
                                   f"Current Working Directory: {cwd}\n"
                                   f"User Directory: {user_dir}\n"
                                   "Click Any Of The Following Buttons To Begin!")
main_text_label.pack()
start_button = Button(root, text="Start Server", command=start_server, font=("TrebuchetMS", 12, 'bold'),
                               width="40", height="3",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
start_button.pack()
create_backup_button = Button(root, text="Create Server Backup", command=create_server_backup, font=("TrebuchetMS", 12, 'bold'),
                               width="40", height="3",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
create_backup_button.pack()
restore_backup_button = Button(root, text="Restore Server Backup", command=restore_server_backup, font=("TrebuchetMS", 12, 'bold'),
                               width="40", height="3",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
restore_backup_button.pack()
reset_server_button = Button(root, text="Reset Server", command=reset_server, font=("TrebuchetMS", 12, 'bold'),
                               width="40", height="3",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
reset_server_button.pack()
use_custom_map_button = Button(root, text="Use Custom Map In Server", command=inject_custom_map, font=("TrebuchetMS", 12, 'bold'),
                               width="40", height="3",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
use_custom_map_button.pack()
reset_dimension_button = Button(root, text="Reset Dimension In A Server", command=reset_dimension_main, font=("TrebuchetMS", 12, 'bold'),
                               width="40", height="3",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
reset_dimension_button.pack()
change_server_properties_button = Button(root, text="Edit Server Properties",
                                         command=change_server_properties, font=("TrebuchetMS", 12, 'bold'),
                                         width="40", height="3",
                                         bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
change_server_properties_button.pack()
import_external_server_button = Button(root, text="Import External Server", command=import_external_server, font=("TrebuchetMS", 12, 'bold'),
                               width="40", height="3",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
import_external_server_button.pack()
logging.info("GUI Built")
logging.info("Starting Main Loop")
root.mainloop()
logging.info("Main Loop Ended")
logging.warning("Exiting Program")
logging.shutdown()
sys.exit(0)
