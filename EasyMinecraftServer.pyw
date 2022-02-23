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
from shutil import rmtree, copytree, copy
import time
import pyautogui as kbm
import json
import ctypes
import urllib
import logging


def start_server():
    version_selection = askstring("Minecraft Server",
                                  "Enter the version you want to use! '1.8.9' or '1.12.2' or '1.16.5' "
                                  "or '1.17.1' or '1.18.1'")
    if version_selection == "1.8.9":
        version = "1.8.9"
        server_version = "189"
        pass
    elif version_selection == "1.12.2":
        version = "1.12.2"
        server_version = "1122"
        pass
    elif version_selection == "1.16.5":
        version = "1.16.5"
        server_version = "1165"
        pass
    elif version_selection == "1.17.1":
        version = "1.17.1"
        server_version = "1171"
        pass
    elif version_selection == "1.18.1":
        version = "1.18.1"
        server_version = "1181"
        pass
    else:
        showerror("Minecraft Server", "You have entered an invalid version!")
        logging.error("Invalid Minecraft Version Selected In start_server(): " + version_selection)
        return
    logging.info("Version Selected In start_server(): " + version_selection)
    if version == "1.16.5" or version == "1.17.1" or version == "1.18.1":
        logging.info("Reading Server Properties File For Server Port")
        p = Properties()
        with open(f"{cwd}\\ServerFiles-{version}\\server.properties", "rb") as f:
            p.load(f)
        port = str(p.get("server-port").data)
        pass
    else:
        logging.info("Defaulting To Port 25565")
        port = "25565"
        pass
    port_forwarded = askyesno(title="Minecraft Server", message=f"Is tcp port {port} forwarded on your network? Press 'NO' if you are not sure!")
    if port_forwarded:
        logging.info("Port Forward Confirmed In start_server()")
        pass
    else:
        logging.info("Port Forward Not Confirmed In start_server()")
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
    showwarning(title="WARNING", message="DO NOT TOUCH ANYTHING FOR AT LEAST 10 SECONDS AFTER CLOSING THIS POPUP IN ORDER TO LET SERVER SUCCESSFULLY START!")
    if server_gui_setting == "True":
        logging.info("Starting Powershell Process")
        os.system("start powershell")
        time.sleep(1)
        logging.info("Starting Minecraft Server With GUI")
        logging.info(f"Executing System Command In Powershell: MinecraftServerGUI {server_version} {ram_amount} {server_backup}")
        kbm.typewrite(f"MinecraftServerGUI {server_version} {ram_amount} {server_backup}\n")
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
        logging.info(f"Executing System Command In Powershell: MinecraftServer-nogui {server_version} {ram_amount} {server_backup}")
        kbm.typewrite(f"MinecraftServer-nogui {server_version} {ram_amount} {server_backup}\n")
        time.sleep(1)
        logging.info("Moving To exit_program_force()")
        exit_program_force()
        sys.exit(0)


def create_server_backup():
    backup_version_selection = askstring(title="Create Server Backup", prompt="Enter the version you want to backup! "
                                                                              "'1.8.9' or '1.12.2' or '1.16.5' "
                                                                              "or '1.17.1' or '1.18.1'")
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
    elif backup_version_selection == "1.18.1":
        backup_version = "1.18.1"
        pass
    else:
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Selected In create_server_backup(): " + backup_version_selection)
        return
    logging.info("Version Selected In create_server_backup(): " + backup_version_selection)
    backup_name = askstring(title="Create Server Backup", prompt="Enter the name of the backup!")
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
    backup_version_selection = askstring(title="Create Server Backup", prompt="Enter the version you want to backup! "
                                                                              "'1.8.9' or '1.12.2' or '1.16.5' "
                                                                              "or '1.17.1' or '1.18.1'")
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
    elif backup_version_selection == "1.18.1":
        backup_version = "1.18.1"
        pass
    else:
        showerror(title="Error", message="Invalid Version!")
        logging.error("Invalid Version Selected In restore_server_backup(): " + backup_version_selection)
        return
    logging.info("Version Selected In restore_server_backup(): " + backup_version_selection)
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
                                                                          "backup? It will replace any current data "
                                                                          "in the server!")
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
    reset_version_selection = askstring(title="Reset Server",
                                        prompt="Please Select The Version You Would Like To Reset! '1.8.9' or "
                                               "'1.12.2' or '1.16.5' "
                                               "or '1.17.1' or '1.18.1'")
    logging.info("Version Selected In reset_server(): " + reset_version_selection)
    if reset_version_selection == "1.8.9":
        try:
            logging.warning("Performing Server Reset")
            os.remove(f"{cwd}\\ServerFiles-1.8.9\\ops.json")
            os.remove(f"{cwd}\\ServerFiles-1.8.9\\banned-ips.json")
            os.remove(f"{cwd}\\ServerFiles-1.8.9\\banned-players.json")
            os.remove(f"{cwd}\\ServerFiles-1.8.9\\whitelist.json")
            os.remove(f"{cwd}\\ServerFiles-1.8.9\\usercache.json")
            rmtree(f"{cwd}\\ServerFiles-1.8.9\\world\\")
            rmtree(f"{cwd}\\ServerFiles-1.8.9\\logs\\")
            os.remove(f"{cwd}\\ServerFiles-1.8.9\\server.properties")
            os.remove(f"{cwd}\\ServerFiles-1.8.9\\eula.txt")
            copy(f"{cwd}\\1.8.9-recovery\\server.properties", f"{cwd}\\ServerFiles-1.8.9\\server.properties")
            copy(f"{cwd}\\1.8.9-recovery\\eula.txt", f"{cwd}\\ServerFiles-1.8.9\\eula.txt")
            logging.info("Server Reset Successful")
            showinfo(title="Reset Server",
                     message="Reset Successful! However, If Your Server Jar File Is Corrupted, You Will Have To Uninstall This Program And Reinstall It!")
            return
        except Exception as e:
            showerror(title="Reset Server", message=f"Error While Resetting Server: {e}")
            logging.error("Error In reset_server(): " + str(e))
            return
    elif reset_version_selection == "1.12.2":
        try:
            logging.warning("Performing Server Reset")
            os.remove(f"{cwd}\\ServerFiles-1.12.2\\ops.json")
            os.remove(f"{cwd}\\ServerFiles-1.12.2\\banned-ips.json")
            os.remove(f"{cwd}\\ServerFiles-1.12.2\\banned-players.json")
            os.remove(f"{cwd}\\ServerFiles-1.12.2\\whitelist.json")
            os.remove(f"{cwd}\\ServerFiles-1.12.2\\usercache.json")
            rmtree(f"{cwd}\\ServerFiles-1.12.2\\world\\")
            rmtree(f"{cwd}\\ServerFiles-1.12.2\\logs\\")
            os.remove(f"{cwd}\\ServerFiles-1.12.2\\server.properties")
            os.remove(f"{cwd}\\ServerFiles-1.12.2\\eula.txt")
            copy(f"{cwd}\\1.12.2-recovery\\server.properties", f"{cwd}\\ServerFiles-1.12.2\\server.properties")
            copy(f"{cwd}\\1.12.2-recovery\\eula.txt", f"{cwd}\\ServerFiles-1.12.2\\eula.txt")
            logging.info("Server Reset Successful")
            showinfo(title="Reset Server",
                     message="Reset Successful! However, If Your Server Jar File Is Corrupted, You Will Have To Uninstall This Program And Reinstall It!")
            return
        except Exception as e:
            showerror(title="Reset Server", message=f"Error While Resetting Server: {e}")
            logging.error("Error In reset_server(): " + str(e))
            return
    elif reset_version_selection == "1.16.5":
        try:
            logging.warning("Performing Server Reset")
            os.remove(f"{cwd}\\ServerFiles-1.16.5\\ops.json")
            os.remove(f"{cwd}\\ServerFiles-1.16.5\\banned-ips.json")
            os.remove(f"{cwd}\\ServerFiles-1.16.5\\banned-players.json")
            os.remove(f"{cwd}\\ServerFiles-1.16.5\\whitelist.json")
            os.remove(f"{cwd}\\ServerFiles-1.16.5\\usercache.json")
            rmtree(f"{cwd}\\ServerFiles-1.16.5\\world\\")
            rmtree(f"{cwd}\\ServerFiles-1.16.5\\logs\\")
            os.remove(f"{cwd}\\ServerFiles-1.16.5\\server.properties")
            os.remove(f"{cwd}\\ServerFiles-1.16.5\\eula.txt")
            copy(f"{cwd}\\1.16.5-recovery\\server.properties", f"{cwd}\\ServerFiles-1.16.5\\server.properties")
            copy(f"{cwd}\\1.16.5-recovery\\eula.txt", f"{cwd}\\ServerFiles-1.16.5\\eula.txt")
            logging.info("Server Reset Successful")
            showinfo(title="Reset Server",
                     message="Reset Successful! However, If Your Server Jar File Is Corrupted, You Will Have To Uninstall This Program And Reinstall It!")
            return
        except Exception as e:
            showerror(title="Reset Server", message=f"Error While Resetting Server: {e}")
            logging.error("Error In reset_server(): " + str(e))
            return
    elif reset_version_selection == "1.17.1":
        try:
            logging.warning("Performing Server Reset")
            os.remove(f"{cwd}\\ServerFiles-1.17.1\\ops.json")
            os.remove(f"{cwd}\\ServerFiles-1.17.1\\banned-ips.json")
            os.remove(f"{cwd}\\ServerFiles-1.17.1\\banned-players.json")
            os.remove(f"{cwd}\\ServerFiles-1.17.1\\whitelist.json")
            os.remove(f"{cwd}\\ServerFiles-1.17.1\\usercache.json")
            rmtree(f"{cwd}\\ServerFiles-1.17.1\\world\\")
            rmtree(f"{cwd}\\ServerFiles-1.17.1\\logs\\")
            os.remove(f"{cwd}\\ServerFiles-1.17.1\\server.properties")
            os.remove(f"{cwd}\\ServerFiles-1.17.1\\eula.txt")
            copy(f"{cwd}\\1.17.1-recovery\\server.properties", f"{cwd}\\ServerFiles-1.17.1\\server.properties")
            copy(f"{cwd}\\1.17.1-recovery\\eula.txt", f"{cwd}\\ServerFiles-1.17.1\\eula.txt")
            logging.info("Server Reset Successful")
            showinfo(title="Reset Server",
                     message="Reset Successful! However, If Your Server Jar File Is Corrupted, You Will Have To Uninstall This Program And Reinstall It!")
            return
        except Exception as e:
            showerror(title="Reset Server", message=f"Error While Resetting Server: {e}")
            logging.error("Error In reset_server(): " + str(e))
            return
    elif reset_version_selection == "1.18.1":
        try:
            logging.warning("Performing Server Reset")
            os.remove(f"{cwd}\\ServerFiles-1.18.1\\ops.json")
            os.remove(f"{cwd}\\ServerFiles-1.18.1\\banned-ips.json")
            os.remove(f"{cwd}\\ServerFiles-1.18.1\\banned-players.json")
            os.remove(f"{cwd}\\ServerFiles-1.18.1\\whitelist.json")
            os.remove(f"{cwd}\\ServerFiles-1.18.1\\usercache.json")
            rmtree(f"{cwd}\\ServerFiles-1.18.1\\world\\")
            rmtree(f"{cwd}\\ServerFiles-1.18.1\\logs\\")
            os.remove(f"{cwd}\\ServerFiles-1.18.1\\server.properties")
            os.remove(f"{cwd}\\ServerFiles-1.18.1\\eula.txt")
            copy(f"{cwd}\\1.18.1-recovery\\server.properties", f"{cwd}\\ServerFiles-1.18.1\\server.properties")
            copy(f"{cwd}\\1.18.1-recovery\\eula.txt", f"{cwd}\\ServerFiles-1.18.1\\eula.txt")
            logging.info("Server Reset Successful")
            showinfo(title="Reset Server",
                     message="Reset Successful! However, If Your Server Jar File Is Corrupted, You Will Have To Uninstall This Program And Reinstall It!")
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
    version_select = askstring(title="Select Version",
                               prompt="Please Select The Version You Would Like To Use The Custom Map In! '1.8.9' or "
                                      "'1.12.2' or '1.16.5' "
                                      "or '1.17.1' or '1.18.1'")
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
    elif version_select == "1.18.1":
        version = "1.18.1"
        pass
    else:
        showerror(title="Select Version", message="Invalid Version!")
        logging.error("Invalid Version Selected In inject_custom_map()")
        return
    logging.info("Version Selected In inject_custom_map(): " + version)
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
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\")
            copytree(f"{custom_map}\\", f"{cwd}\\ServerFiles-{version}\\world\\")
            showinfo(title="Custom Map", message="Custom Map Successfully Injected!")
            logging.info("Custom Map Injection Successful")
            pass
        except Exception as e:
            showerror(title="Custom Map", message=f"Error while injecting custom map: {e}")
            logging.error("Error In inject_custom_map(): " + str(e))
            pass
        return


def reset_overworld():
    dim_reset_version = askstring(title="Select Version",
                                  prompt="Please Select The Version You Would Like To Reset 'THE OVERWORLD' In! '1.8.9' or "
                                         "'1.12.2' or '1.16.5' "
                                         "or '1.17.1' or '1.18.1'")
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
    elif dim_reset_version == "1.18.1":
        version = "1.18.1"
        pass
    else:
        showerror(title="Reset Dimension", message="Invalid Version!")
        logging.error("Invalid Version Selected In reset_overworld()")
        return
    logging.info("Version Selected In reset_overworld(): " + version)
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
        rmtree(f"{cwd}\\ServerFiles-{version}\\world\\region\\")
        showinfo(title="Dimension Reset", message="Overworld Successfully Reset!")
        logging.info("Overworld Successfully Reset In reset_overworld()")
        return
    else:
        showinfo("Dimension Reset", "Dimension Reset Cancelled!")
        logging.info("Dimension Reset Cancelled In reset_overworld()")
        return


def reset_nether():
    dim_reset_version = askstring(title="Select Version",
                                  prompt="Please Select The Version You Would Like To Reset 'THE NETHER' In! '1.8.9' or "
                                         "'1.12.2' or '1.16.5' "
                                         "or '1.17.1' or '1.18.1'")
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
    elif dim_reset_version == "1.18.1":
        version = "1.18.1"
        pass
    else:
        showerror(title="Reset Dimension", message="Invalid Version!")
        logging.error("Invalid Version Selected In reset_nether()")
        return
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
        rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM-1\\region\\")
        showinfo(title="Dimension Reset", message="Nether Successfully Reset!")
        logging.info("Nether Successfully Reset In reset_nether()")
        return
    else:
        showinfo("Dimension Reset", "Dimension Reset Cancelled!")
        logging.info("Dimension Reset Cancelled In reset_nether()")
        return


def reset_end():
    dim_reset_version = askstring(title="Select Version",
                                  prompt="Please Select The Version You Would Like To Reset 'THE END' In! '1.8.9' or "
                                         "'1.12.2' or '1.16.5' "
                                         "or '1.17.1' or '1.18.1'")
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
    elif dim_reset_version == "1.18.1":
        version = "1.18.1"
        pass
    else:
        showerror(title="Reset Dimension", message="Invalid Version!")
        return
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
        rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM1\\region\\")
        showinfo(title="Dimension Reset", message="End Successfully Reset!")
        logging.info("End Successfully Reset In reset_end()")
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
    properties_window = Toplevel(root)
    properties_window.title("Change Server Properties")
    properties_window.geometry("1750x1050")
    properties_window.resizable(False, False)
    showwarning(title="Warning",
                message="This feature is experimental and will have bugs and it is only for people who know what they are doing! Use at your own risk!")
    properties_version = askstring(title="Change Server Properties",
                                   prompt="Enter the version of the properties file you want to edit! 1.16.5, 1.17.1 or 1.18.1")
    if properties_version == "1.16.5":
        version = "1.16.5"
        pass
    elif properties_version == "1.17.1":
        version = "1.17.1"
        pass
    elif properties_version == "1.18.1":
        version = "1.18.1"
        pass
    else:
        showerror(title="Change Server Properties", message="Invalid Version!")
        logging.error("Invalid Version In change_server_properties()")
        properties_window.destroy()
    p = Properties()
    logging.info("Properties File Loaded In change_server_properties()")
    logging.info("Reading Server Properties In change_server_properties()")
    with open(f"{cwd}\\ServerFiles-{version}\\server.properties", "rb") as f:
        p.load(f)
    warning_label = Label(properties_window, text="WARNING: Changing Server Properties Can Cause Server To "
                                                  "Malfunction! Please Proceed With Caution! If You Do Not Know What "
                                                  "You Are Doing, Please Leave This Screen!")
    warning_label.grid(sticky=W, row=1, column=1)
    properties_label = Label(properties_window, text="Change What You Would Like And Then Click The Save Button!")
    properties_label.grid(sticky=W, row=2, column=1)
    broadcast_rcon_to_ops_label = Label(properties_window, text="Broadcast RCON To Ops")
    broadcast_rcon_to_ops_label.grid(sticky=W, row=3, column=1)
    broadcast_rcon_to_ops_entry = Entry(properties_window, width=115)
    broadcast_rcon_to_ops_entry.grid(row=4, column=1)
    broadcast_rcon_to_ops_entry.insert(0, p.get("broadcast-rcon-to-ops").data)
    view_distance_label = Label(properties_window, text="View Distance")
    view_distance_label.grid(sticky=W, row=5, column=1)
    view_distance_entry = Entry(properties_window, width=115)
    view_distance_entry.grid(row=6, column=1)
    view_distance_entry.insert(0, p.get("view-distance").data)
    enable_jmx_monitoring_label = Label(properties_window, text="Enable JMX Monitoring")
    enable_jmx_monitoring_label.grid(sticky=W, row=7, column=1)
    enable_jmx_monitoring_entry = Entry(properties_window, width=115)
    enable_jmx_monitoring_entry.grid(row=8, column=1)
    enable_jmx_monitoring_entry.insert(0, p.get("enable-jmx-monitoring").data)
    server_ip_label = Label(properties_window, text="Server IP")
    server_ip_label.grid(sticky=W, row=9, column=1)
    server_ip_entry = Entry(properties_window, width=115)
    server_ip_entry.grid(row=10, column=1)
    server_ip_entry.insert(0, p.get("server-ip").data)
    resource_pack_prompt_label = Label(properties_window, text="Resource Pack Prompt")
    resource_pack_prompt_label.grid(sticky=W, row=11, column=1)
    resource_pack_prompt_entry = Entry(properties_window, width=115)
    resource_pack_prompt_entry.grid(row=12, column=1)
    resource_pack_prompt_entry.insert(0, p.get("resource-pack-prompt").data)
    rcon_port_label = Label(properties_window, text="Rcon Port")
    rcon_port_label.grid(sticky=W, row=13, column=1)
    rcon_port_entry = Entry(properties_window, width=115)
    rcon_port_entry.grid(row=14, column=1)
    rcon_port_entry.insert(0, p.get("rcon.port").data)
    gamemode_label = Label(properties_window, text="Gamemode")
    gamemode_label.grid(sticky=W, row=15, column=1)
    gamemode_entry = Entry(properties_window, width=115)
    gamemode_entry.grid(row=16, column=1)
    gamemode_entry.insert(0, p.get("gamemode").data)
    server_port_label = Label(properties_window, text="Server Port")
    server_port_label.grid(sticky=W, row=17, column=1)
    server_port_entry = Entry(properties_window, width=115)
    server_port_entry.grid(row=18, column=1)
    server_port_entry.insert(0, p.get("server-port").data)
    allow_nether_label = Label(properties_window, text="Allow Nether")
    allow_nether_label.grid(sticky=W, row=19, column=1)
    allow_nether_entry = Entry(properties_window, width=115)
    allow_nether_entry.grid(row=20, column=1)
    allow_nether_entry.insert(0, p.get("allow-nether").data)
    enable_command_block_label = Label(properties_window, text="Enable Command Block")
    enable_command_block_label.grid(sticky=W, row=21, column=1)
    enable_command_block_entry = Entry(properties_window, width=115)
    enable_command_block_entry.grid(row=22, column=1)
    enable_command_block_entry.insert(0, p.get("enable-command-block").data)
    enable_rcon_label = Label(properties_window, text="Enable RCON")
    enable_rcon_label.grid(sticky=W, row=23, column=1)
    enable_rcon_entry = Entry(properties_window, width=115)
    enable_rcon_entry.grid(row=24, column=1)
    enable_rcon_entry.insert(0, p.get("enable-rcon").data)
    sync_chunk_writes_label = Label(properties_window, text="Sync Chunk Writes")
    sync_chunk_writes_label.grid(sticky=W, row=25, column=1)
    sync_chunk_writes_entry = Entry(properties_window, width=115)
    sync_chunk_writes_entry.grid(row=26, column=1)
    sync_chunk_writes_entry.insert(0, p.get("sync-chunk-writes").data)
    enable_query_label = Label(properties_window, text="Enable Query")
    enable_query_label.grid(sticky=W, row=27, column=1)
    enable_query_entry = Entry(properties_window, width=115)
    enable_query_entry.grid(row=28, column=1)
    enable_query_entry.insert(0, p.get("enable-query").data)
    op_permission_level_label = Label(properties_window, text="Op Permission Level")
    op_permission_level_label.grid(sticky=W, row=29, column=1)
    op_permission_level_entry = Entry(properties_window, width=115)
    op_permission_level_entry.grid(row=30, column=1)
    op_permission_level_entry.insert(0, p.get("op-permission-level").data)
    prevent_proxy_connections_label = Label(properties_window, text="Prevent Proxy Connections")
    prevent_proxy_connections_label.grid(sticky=W, row=31, column=1)
    prevent_proxy_connections_entry = Entry(properties_window, width=115)
    prevent_proxy_connections_entry.grid(row=32, column=1)
    prevent_proxy_connections_entry.insert(0, p.get("prevent-proxy-connections").data)
    resource_pack_label = Label(properties_window, text="Resource Pack")
    resource_pack_label.grid(sticky=W, row=33, column=1)
    resource_pack_entry = Entry(properties_window, width=115)
    resource_pack_entry.grid(row=34, column=1)
    resource_pack_entry.insert(0, p.get("resource-pack").data)
    entity_broadcast_range_percentage_label = Label(properties_window, text="Entity Broadcast Range Percentage")
    entity_broadcast_range_percentage_label.grid(sticky=W, row=35, column=1)
    entity_broadcast_range_percentage_entry = Entry(properties_window, width=115)
    entity_broadcast_range_percentage_entry.grid(row=36, column=1)
    entity_broadcast_range_percentage_entry.insert(0, p.get("entity-broadcast-range-percentage").data)
    level_name_label = Label(properties_window, text="Level Name")
    level_name_label.grid(sticky=W, row=37, column=1)
    level_name_entry = Entry(properties_window, width=115)
    level_name_entry.grid(row=38, column=1)
    level_name_entry.insert(0, p.get("level-name").data)
    rcon_password_label = Label(properties_window, text="Rcon Password")
    rcon_password_label.grid(sticky=W, row=39, column=1)
    rcon_password_entry = Entry(properties_window, width=115)
    rcon_password_entry.grid(row=40, column=1)
    rcon_password_entry.insert(0, p.get("rcon.password").data)
    player_idle_timeout_label = Label(properties_window, text="Player Idle Timeout")
    player_idle_timeout_label.grid(sticky=W, row=41, column=1)
    player_idle_timeout_entry = Entry(properties_window, width=115)
    player_idle_timeout_entry.grid(row=42, column=1)
    player_idle_timeout_entry.insert(0, p.get("player-idle-timeout").data)
    motd_label = Label(properties_window, text="MOTD")
    motd_label.grid(sticky=W, row=43, column=1)
    motd_entry = Entry(properties_window, width=115)
    motd_entry.grid(row=44, column=1)
    motd_entry.insert(0, p.get("motd").data)
    query_port_label = Label(properties_window, text="Query Port")
    query_port_label.grid(sticky=W, row=45, column=1)
    query_port_entry = Entry(properties_window, width=115)
    query_port_entry.grid(row=46, column=1)
    query_port_entry.insert(0, p.get("query.port").data)
    force_gamemode_label = Label(properties_window, text="Force Gamemode")
    force_gamemode_label.grid(sticky=W, row=47, column=1)
    force_gamemode_entry = Entry(properties_window, width=115)
    force_gamemode_entry.grid(row=48, column=1)
    force_gamemode_entry.insert(0, p.get("force-gamemode").data)
    rate_limit_label = Label(properties_window, text="Rate Limit")
    rate_limit_label.grid(sticky=W, row=49, column=1)
    rate_limit_entry = Entry(properties_window, width=115)
    rate_limit_entry.grid(row=50, column=1)
    rate_limit_entry.insert(0, p.get("rate-limit").data)
    hardcore_label = Label(properties_window, text="Hardcore")
    hardcore_label.grid(sticky=W, row=1, column=2)
    hardcore_entry = Entry(properties_window, width=115)
    hardcore_entry.grid(row=2, column=2)
    hardcore_entry.insert(0, p.get("hardcore").data)
    white_list_label = Label(properties_window, text="White List")
    white_list_label.grid(sticky=W, row=3, column=2)
    white_list_entry = Entry(properties_window, width=115)
    white_list_entry.grid(row=4, column=2)
    white_list_entry.insert(0, p.get("white-list").data)
    broadcast_console_to_ops_label = Label(properties_window, text="Broadcast Console To Ops")
    broadcast_console_to_ops_label.grid(sticky=W, row=5, column=2)
    broadcast_console_to_ops_entry = Entry(properties_window, width=115)
    broadcast_console_to_ops_entry.grid(row=6, column=2)
    broadcast_console_to_ops_entry.insert(0, p.get("broadcast-console-to-ops").data)
    pvp_label = Label(properties_window, text="PvP")
    pvp_label.grid(sticky=W, row=7, column=2)
    pvp_entry = Entry(properties_window, width=115)
    pvp_entry.grid(row=8, column=2)
    pvp_entry.insert(0, p.get("pvp").data)
    spawn_npcs_label = Label(properties_window, text="Spawn NPCs")
    spawn_npcs_label.grid(sticky=W, row=9, column=2)
    spawn_npcs_entry = Entry(properties_window, width=115)
    spawn_npcs_entry.grid(row=10, column=2)
    spawn_npcs_entry.insert(0, p.get("spawn-npcs").data)
    spawn_animals_label = Label(properties_window, text="Spawn Animals")
    spawn_animals_label.grid(sticky=W, row=11, column=2)
    spawn_animals_entry = Entry(properties_window, width=115)
    spawn_animals_entry.grid(row=12, column=2)
    spawn_animals_entry.insert(0, p.get("spawn-animals").data)
    if version != "1.18.1":
        snooper_enabled_label = Label(properties_window, text="Snooper Enabled")
        snooper_enabled_label.grid(sticky=W, row=13, column=2)
        snooper_enabled_entry = Entry(properties_window, width=115)
        snooper_enabled_entry.grid(row=14, column=2)
        snooper_enabled_entry.insert(0, p.get("snooper-enabled").data)
        pass
    else:
        pass
    difficulty_label = Label(properties_window, text="Difficulty")
    difficulty_label.grid(sticky=W, row=15, column=2)
    difficulty_entry = Entry(properties_window, width=115)
    difficulty_entry.grid(row=16, column=2)
    difficulty_entry.insert(0, p.get("difficulty").data)
    function_permission_level_label = Label(properties_window, text="Function Permission Level")
    function_permission_level_label.grid(sticky=W, row=17, column=2)
    function_permission_level_entry = Entry(properties_window, width=115)
    function_permission_level_entry.grid(row=18, column=2)
    function_permission_level_entry.insert(0, p.get("function-permission-level").data)
    network_compression_threshold_label = Label(properties_window, text="Network Compression Threshold")
    network_compression_threshold_label.grid(sticky=W, row=19, column=2)
    network_compression_threshold_entry = Entry(properties_window, width=115)
    network_compression_threshold_entry.grid(row=20, column=2)
    network_compression_threshold_entry.insert(0, p.get("network-compression-threshold").data)
    text_filtering_config_label = Label(properties_window, text="Text Filtering Config")
    text_filtering_config_label.grid(sticky=W, row=21, column=2)
    text_filtering_config_entry = Entry(properties_window, width=115)
    text_filtering_config_entry.grid(row=22, column=2)
    text_filtering_config_entry.insert(0, p.get("text-filtering-config").data)
    require_resource_pack_label = Label(properties_window, text="Require Resource Packs")
    require_resource_pack_label.grid(sticky=W, row=23, column=2)
    require_resource_pack_entry = Entry(properties_window, width=115)
    require_resource_pack_entry.grid(row=24, column=2)
    require_resource_pack_entry.insert(0, p.get("require-resource-pack").data)
    spawn_monsters_label = Label(properties_window, text="Spawn Monsters")
    spawn_monsters_label.grid(sticky=W, row=25, column=2)
    spawn_monsters_entry = Entry(properties_window, width=115)
    spawn_monsters_entry.grid(row=26, column=2)
    spawn_monsters_entry.insert(0, p.get("spawn-monsters").data)
    max_tick_time_label = Label(properties_window, text="Max Tick Time")
    max_tick_time_label.grid(sticky=W, row=27, column=2)
    max_tick_time_entry = Entry(properties_window, width=115)
    max_tick_time_entry.grid(row=28, column=2)
    max_tick_time_entry.insert(0, p.get("max-tick-time").data)
    enforce_whitelist_label = Label(properties_window, text="Enforce Whitelist")
    enforce_whitelist_label.grid(sticky=W, row=29, column=2)
    enforce_whitelist_entry = Entry(properties_window, width=115)
    enforce_whitelist_entry.grid(row=30, column=2)
    enforce_whitelist_entry.insert(0, p.get("enforce-whitelist").data)
    use_native_transport_label = Label(properties_window, text="Use Native Transport")
    use_native_transport_label.grid(sticky=W, row=31, column=2)
    use_native_transport_entry = Entry(properties_window, width=115)
    use_native_transport_entry.grid(row=32, column=2)
    use_native_transport_entry.insert(0, p.get("use-native-transport").data)
    max_players_label = Label(properties_window, text="Max Players")
    max_players_label.grid(sticky=W, row=33, column=2)
    max_players_entry = Entry(properties_window, width=115)
    max_players_entry.grid(row=34, column=2)
    max_players_entry.insert(0, p.get("max-players").data)
    resource_pack_sha1_label = Label(properties_window, text="Resource Pack SHA1")
    resource_pack_sha1_label.grid(sticky=W, row=35, column=2)
    resource_pack_sha1_entry = Entry(properties_window, width=115)
    resource_pack_sha1_entry.grid(row=36, column=2)
    resource_pack_sha1_entry.insert(0, p.get("resource-pack-sha1").data)
    spawn_protection_label = Label(properties_window, text="Spawn Protection")
    spawn_protection_label.grid(sticky=W, row=37, column=2)
    spawn_protection_entry = Entry(properties_window, width=115)
    spawn_protection_entry.grid(row=38, column=2)
    spawn_protection_entry.insert(0, p.get("spawn-protection").data)
    online_mode_label = Label(properties_window, text="Online Mode")
    online_mode_label.grid(sticky=W, row=39, column=2)
    online_mode_entry = Entry(properties_window, width=115)
    online_mode_entry.grid(row=40, column=2)
    online_mode_entry.insert(0, p.get("online-mode").data)
    enable_status_label = Label(properties_window, text="Enable Status")
    enable_status_label.grid(sticky=W, row=41, column=2)
    enable_status_entry = Entry(properties_window, width=115)
    enable_status_entry.grid(row=42, column=2)
    enable_status_entry.insert(0, p.get("enable-status").data)
    allow_flight_label = Label(properties_window, text="Allow Flight")
    allow_flight_label.grid(sticky=W, row=43, column=2)
    allow_flight_entry = Entry(properties_window, width=115)
    allow_flight_entry.grid(row=44, column=2)
    allow_flight_entry.insert(0, p.get("allow-flight").data)
    max_world_size_label = Label(properties_window, text="Max World Size")
    max_world_size_label.grid(sticky=W, row=45, column=2)
    max_world_size_entry = Entry(properties_window, width=115)
    max_world_size_entry.grid(row=46, column=2)
    max_world_size_entry.insert(0, p.get("max-world-size").data)
    logging.info("Loaded current server properties")
    logging.info("Awaiting user input to rewrite server properties")
    var = IntVar()
    properties_window.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    save_button = Button(properties_window, text="Save", command=lambda: var.set(1))
    save_button.grid(row=47, column=2)
    save_button.wait_variable(var)
    logging.warning("Saving new server properties")
    broadcast_rcon_to_ops = broadcast_rcon_to_ops_entry.get()
    view_distance = view_distance_entry.get()
    enable_jmx_monitoring = enable_jmx_monitoring_entry.get()
    server_ip = server_ip_entry.get()
    resource_pack_prompt = resource_pack_prompt_entry.get()
    rcon_port = rcon_port_entry.get()
    gamemode = gamemode_entry.get()
    server_port = server_port_entry.get()
    allow_nether = allow_nether_entry.get()
    enable_command_block = enable_command_block_entry.get()
    enable_rcon = enable_rcon_entry.get()
    sync_chunk_writes = sync_chunk_writes_entry.get()
    enable_query = enable_query_entry.get()
    op_permission_level = op_permission_level_entry.get()
    prevent_proxy_connections = prevent_proxy_connections_entry.get()
    resource_pack = resource_pack_entry.get()
    entity_broadcast_range_percentage = entity_broadcast_range_percentage_entry.get()
    level_name = level_name_entry.get()
    rcon_password = rcon_password_entry.get()
    player_idle_timeout = player_idle_timeout_entry.get()
    motd = motd_entry.get()
    query_port = query_port_entry.get()
    force_gamemode = force_gamemode_entry.get()
    rate_limit = rate_limit_entry.get()
    hardcore = hardcore_entry.get()
    white_list = white_list_entry.get()
    broadcast_console_to_ops = broadcast_console_to_ops_entry.get()
    pvp = pvp_entry.get()
    spawn_npcs = spawn_npcs_entry.get()
    spawn_animals = spawn_animals_entry.get()
    if version != "1.18.1":
        snooper_enabled = snooper_enabled_entry.get()
        pass
    else:
        pass
    difficulty = difficulty_entry.get()
    function_permission_level = function_permission_level_entry.get()
    network_compression_threshold = network_compression_threshold_entry.get()
    text_filtering_config = text_filtering_config_entry.get()
    require_resource_pack = require_resource_pack_entry.get()
    spawn_monsters = spawn_monsters_entry.get()
    max_tick_time = max_tick_time_entry.get()
    enforce_whitelist = enforce_whitelist_entry.get()
    use_native_transport = use_native_transport_entry.get()
    max_players = max_players_entry.get()
    resource_pack_sha1 = resource_pack_sha1_entry.get()
    spawn_protection = spawn_protection_entry.get()
    online_mode = online_mode_entry.get()
    enable_status = enable_status_entry.get()
    allow_flight = allow_flight_entry.get()
    max_world_size = max_world_size_entry.get()
    with open(f"{cwd}\\ServerFiles-{properties_version}\\server.properties", "r+b") as f:
        p["broadcast-rcon-to-ops"] = str(broadcast_rcon_to_ops)
        p["view-distance"] = str(view_distance)
        p["enable-jmx-monitoring"] = str(enable_jmx_monitoring)
        p["server-ip"] = str(server_ip)
        p["resource-pack-prompt"] = str(resource_pack_prompt)
        p["rcon.port"] = str(rcon_port)
        p["gamemode"] = str(gamemode)
        p["server-port"] = str(server_port)
        p["allow-nether"] = str(allow_nether)
        p["enable-command-block"] = str(enable_command_block)
        p["enable-rcon"] = str(enable_rcon)
        p["sync-chunk-writes"] = str(sync_chunk_writes)
        p["enable-query"] = str(enable_query)
        p["op-permission-level"] = str(op_permission_level)
        p["prevent-proxy-connections"] = str(prevent_proxy_connections)
        p["resource-pack"] = str(resource_pack)
        p["entity-broadcast-range-percentage"] = str(entity_broadcast_range_percentage)
        p["level-name"] = str(level_name)
        p["rcon.password"] = str(rcon_password)
        p["player-idle-timeout"] = str(player_idle_timeout)
        p["motd"] = str(motd)
        p["query.port"] = str(query_port)
        p["force-gamemode"] = str(force_gamemode)
        p["rate-limit"] = str(rate_limit)
        p["hardcore"] = str(hardcore)
        p["white-list"] = str(white_list)
        p["broadcast-console-to-ops"] = str(broadcast_console_to_ops)
        p["pvp"] = str(pvp)
        p["spawn-npcs"] = str(spawn_npcs)
        p["spawn-animals"] = str(spawn_animals)
        if version != "1.18.1":
            p["snooper-enabled"] = str(snooper_enabled)
            pass
        else:
            pass
        p["difficulty"] = str(difficulty)
        p["function-permission-level"] = str(function_permission_level)
        p["network-compression-threshold"] = str(network_compression_threshold)
        p["text-filtering-config"] = str(text_filtering_config)
        p["require-resource-pack"] = str(require_resource_pack)
        p["spawn-monsters"] = str(spawn_monsters)
        p["max-tick-time"] = str(max_tick_time)
        p["enforce-whitelist"] = str(enforce_whitelist)
        p["use-native-transport"] = str(use_native_transport)
        p["max-players"] = str(max_players)
        p["resource-pack-sha1"] = str(resource_pack_sha1)
        p["spawn-protection"] = str(spawn_protection)
        p["online-mode"] = str(online_mode)
        p["enable-status"] = str(enable_status)
        p["allow-flight"] = str(allow_flight)
        p["max-world-size"] = str(max_world_size)
        f.seek(0)
        f.truncate(0)
        p.store(f, "utf-8")
        pass
    showinfo(title="Server Properties", message="Server Properties Updated!")
    logging.warning("Server Properties Updated!")
    properties_window.destroy()


def import_external_server():
    version_select = askstring(title="Select Version",
                               prompt="Please Select The Version You Would Like To Use The Custom Map In! '1.8.9' or "
                                      "'1.12.2' or '1.16.5' "
                                      "or '1.17.1' or '1.18.1'")
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
    elif version_select == "1.18.1":
        version = "1.18.1"
        pass
    else:
        showerror(title="Error", message="Invalid Version Selected!")
        logging.error("Invalid Version Selected!")
        return
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
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\")
            os.remove(f"{cwd}\\ServerFiles-{version}\\server.properties")
            os.remove(f"{cwd}\\ServerFiles-{version}\\eula.txt")
            os.remove(f"{cwd}\\ServerFiles-{version}\\ops.json")
            os.remove(f"{cwd}\\ServerFiles-{version}\\banned-ips.json")
            os.remove(f"{cwd}\\ServerFiles-{version}\\banned-players.json")
            os.remove(f"{cwd}\\ServerFiles-{version}\\whitelist.json")
            copy(f"{import_files}\\world\\", f"{cwd}\\ServerFiles-{version}\\world\\")
            copy(f"{import_files}\\server.properties", f"{cwd}\\ServerFiles-{version}\\server.properties")
            copy(f"{import_files}\\eula.txt", f"{cwd}\\ServerFiles-{version}\\eula.txt")
            copy(f"{import_files}\\ops.json", f"{cwd}\\ServerFiles-{version}\\ops.json")
            copy(f"{import_files}\\banned-ips.json", f"{cwd}\\ServerFiles-{version}\\banned-ips.json")
            copy(f"{import_files}\\banned-players.json", f"{cwd}\\ServerFiles-{version}\\banned-players.json")
            copy(f"{import_files}\\whitelist.json", f"{cwd}\\ServerFiles-{version}\\whitelist.json")
            showinfo(title="Custom Map", message="Server Successfully Imported!")
            logging.info("Server successfully imported")
            return
        except Exception as e:
            showerror(title="Import Error", message=f"Error while performing import: {e}")
            logging.error(f"Error while performing import: {e}")
            return


def setup(arg):
    showinfo(title="Setup", message="Setup for EasyMinecraftServer is required! Please follow the instructions!")
    if arg == "all":
        path = f"{user_dir}\\Documents\\EasyMinecraftServer\\ProgramBackups\\"
        backup_subdirs = os.listdir(path)
        if len(backup_subdirs) == 0:
            pass
        else:
            restore_backup_prompt = askyesno(title="Restore Backup", message="Program backup detected! Would you like to restore?")
            if restore_backup_prompt:
                program_restore()
                restart_force()
                sys.exit(0)
            else:
                pass
            pass
        auto_server_backup = askyesno(title="Auto Server Backup",
                                      message="Would you like to automatically backup your servers whenever they are stopped?")
        server_gui = askyesno(title="Server GUI", message="Would you like to have a GUI for your servers?")
        ram_allocation_amount = askstring(title="RAM Allocation Amount",
                                          prompt="How much RAM (IN MB) would you like to allocate to the server? "
                                                 "Minimum Recommended: 2048")
        if not ram_allocation_amount or ram_allocation_amount.isspace() or ram_allocation_amount == "":
            showerror(title="Error", message="Invalid RAM Allocation Amount!")
            exit_program_force()
        else:
            pass
        webbrowser.open("https://dashboard.ngrok.com/get-started/setup")
        showinfo(title="NGROK", message="Makeshift port-forwarding requires a ngrok account. Please navigate to "
                                        "https://dashboard.ngrok.com/get-started/setup after making a free account and "
                                        "get your authtoken!")
        ngrok_authtoken = askstring(title="Ngrok Authtoken", prompt="Please enter your ngrok authtoken!")
        if not ngrok_authtoken or ngrok_authtoken.isspace() or ngrok_authtoken == "":
            showerror(title="Error", message="Invalid NGROK Authtoken!")
            exit_program_force()
        else:
            pass
        settings = {
            "auto_server_backup": f"{str(auto_server_backup)}",
            "server_gui": f"{str(server_gui)}",
            "ram_allocation_amount": f"{str(ram_allocation_amount)}",
            "ngrok_authtoken": f"{str(ngrok_authtoken)}"
        }
        settings_object = json.dumps(settings, indent=4)
        with open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "w+") as outfile:
            outfile.write(settings_object)
            outfile.close()
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
    ram_allocation_amount_label = Label(settings_window, text="RAM Allocation Amount (MB)")
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
        if folder == "Logs":
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
            if folder == "Logs":
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
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.1.0":
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
        sys.exit(0)
    else:
        pass


def exit_program_force():
    logging.info("Exiting EasyMinecraftServer")
    logging.shutdown()
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
        showinfo(title="Uninstall", message="Uninstall Cancelled! Please Restart To Use Again!")
        logging.info("Uninstall Cancelled! Please Restart To Use Again!")
        restart_program()
        sys.exit(0)


def jdk_installer():
    logging.info("Launching JDK Installer")
    os.startfile(f"{cwd}\\JDK\\jdk-17_windows-x64_bin.exe")
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
    


def help_window():
    logging.info("Showing help window")
    help_window = Toplevel()
    help_window.title("EasyMiencraftServer (HELP)")
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
cwd = os.getcwd()
user_dir = os.path.expanduser("~")
root = Tk()
root.title("Easy Minecraft Server v2.1.0")
root.geometry("400x400")
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
if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.18.1\\"):
    os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\1.18.1\\")
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
logging.info("Easy Minecraft Server v2.1.0 Started")
logging.info("Building GUI")
main_menu.add_command(label="Help", command=help_window)
main_menu.add_command(label="Settings", command=settings)
main_menu.add_command(label="Backup Program", command=program_backup)
main_menu.add_command(label="Restore Program", command=program_restore)
main_menu.add_command(label="Reset Program", command=program_reset)
main_menu.add_command(label="Changelog", command=changelog)
main_menu.add_command(label="Update", command=update)
main_menu.add_command(label="Uninstall", command=uninstall_program)
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
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.1.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        logging.warning(f"New version available: {new_version}")
        showinfo(title="Update Available", message=f"New version available: {new_version} Please press the update "
                                                   f"button in the main menu at the top to update!")
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
if not os.path.exists("C:\\Program Files\\Java\\jdk-17.0.1\\bin\\"):
    logging.warning("JDK Not Found")
    install_jdk_ask = askyesno(title="JDK Required",
                               message="Java Development Kit 17.0.1 Is Required To Run Minecraft Servers! Would You Like To "
                                       "Install It Now?")
    if install_jdk_ask:
        logging.info("Installing JDK")
        os.startfile(f"{cwd}\\JDK\\jdk-17_windows-x64_bin.exe")
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
    pass
main_text_label = Label(root, text="Easy Minecraft Server v2.1.0\n"
                                   "Github: https://github.com/teekar2023/EasyMinecraftServer\n"
                                   "Not In Any Way Affiliated With Minecraft, Mojang, Or Microsoft\n"
                                   f"Current Working Directory: {cwd}\n"
                                   f"User Directory: {user_dir}\n"
                                   "Click Any Of The Following Buttons To Begin!")
main_text_label.pack()
start_button = Button(root, text="Start Server", command=start_server)
start_button.pack()
create_backup_button = Button(root, text="Create Server Backup", command=create_server_backup)
create_backup_button.pack()
restore_backup_button = Button(root, text="Restore Server Backup", command=restore_server_backup)
restore_backup_button.pack()
reset_server_button = Button(root, text="Reset Server", command=reset_server)
reset_server_button.pack()
use_custom_map_button = Button(root, text="Use Custom Map In Server", command=inject_custom_map)
use_custom_map_button.pack()
reset_dimension_button = Button(root, text="Reset Dimension In A Server", command=reset_dimension_main)
reset_dimension_button.pack()
change_server_properties_button = Button(root, text="Change Server Properties (EXPERIMENTAL)",
                                         command=change_server_properties)
change_server_properties_button.pack()
import_external_server_button = Button(root, text="Import External Server", command=import_external_server)
import_external_server_button.pack()
logging.info("GUI Built")
logging.info("Starting Main Loop")
root.mainloop()
logging.info("Main Loop Ended")
logging.warning("Exiting Program")
logging.shutdown()
sys.exit(0)
