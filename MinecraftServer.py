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
from shutil import copytree, rmtree, copy
from jproperties import Properties


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart():
    confirm_restart = askyesno(title="Restart", message="Restart EasyMinecraftServer?")
    if confirm_restart:
        os.system("cls")
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
    if backup_version not in backup_path:
        showerror("Those files are unusable in this server!")
        print("Those files are unusable in this server!")
        restart()
        sys.exit(0)
    else:
        pass
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
                backup_current_server = askyesno(title="Restore Server Backup", message="You have current data in the "
                                                                                        "server! Would you like "
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
        showinfo(title="Reset Server", message="Reset Successful!")
        print("Reset Successful!")
        restart()
        sys.exit(0)
    elif reset_version_selection == "1.12.2":
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
        showinfo(title="Reset Server", message="Reset Successful!")
        print("Reset Successful!")
        restart()
        sys.exit(0)
    elif reset_version_selection == "1.16.5":
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
        showinfo(title="Reset Server", message="Reset Successful!")
        print("Reset Successful!")
        restart()
        sys.exit(0)
    elif reset_version_selection == "1.17.1":
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


def change_server_properties(properties_version):
    if properties_version == "1.8.9":
        version = "1.8.9"
        pass
    elif properties_version == "1.12.2":
        version = "1.12.2"
        pass
    elif properties_version == "1.16.5":
        version = "1.16.5"
        pass
    elif properties_version == "1.17.1":
        version = "1.17.1"
        pass
    else:
        version = "1.17.1"
        pass
    properties_window = Toplevel(root)
    properties_window.title("Change Server Properties")
    properties_window.geometry("1750x1050")
    properties_window.resizable(False, False)
    p = Properties()
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
    snooper_enabled_label = Label(properties_window, text="Snooper Enabled")
    snooper_enabled_label.grid(sticky=W, row=13, column=2)
    snooper_enabled_entry = Entry(properties_window, width=115)
    snooper_enabled_entry.grid(row=14, column=2)
    snooper_enabled_entry.insert(0, p.get("snooper-enabled").data)
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
    var = IntVar()
    properties_window.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    save_button = Button(properties_window, text="Save", command=lambda: var.set(1))
    save_button.grid(row=47, column=2)
    save_button.wait_variable(var)
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
    snooper_enabled = snooper_enabled_entry.get()
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
        p["snooper-enabled"] = str(snooper_enabled)
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
    print("Server Properties Updated!")
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
print("EasyMinecraftServer Version: 1.9.0")
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
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v1.9.0":
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
            new_url = str(redirected_url) + "/MinecraftServerInstaller.exe"
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
                                            message=f"Update Completed! Would You Like To Install? Installer Location: {installed_file2}")
            if install_confirmation:
                os.startfile(f"{installed_file2}")
                sys.exit(0)
            else:
                showinfo(title="Update Installer", message="Update Installer Downloaded To: "
                                                           f"{installed_file2}\n\nPlease run this installer to "
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
print("If Something Is Not Working Correctly, Please Reset The Server!")
print("-------------------------")
print("1. Start Server")
print("2. Create Server Backup")
print("3. Restore Server Backup")
print("4. Reset Server")
print("5. Use A Custom Map In Server")
print("6. Reset A Dimension In Server")
print("7. Change Server Properties (BETA)")
print("8. Changelog")
print("9. Exit")
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
    properties_version = askstring(title="Select Version",
                                   prompt="Please Select The Version You Would Like To Edit Server Properties For! '1.8.9' or "
                                          "'1.12.2' or '1.16.5' "
                                          "or '1.17.1'")
    change_server_properties(properties_version=properties_version)
    root.mainloop()
elif main_input == "8":
    changelog = str(open(f"{cwd}\\CHANGELOG.txt", "r").read())
    showinfo(title="EasyMinecraftServer Changelog", message=changelog)
    print(changelog)
    restart()
    sys.exit(0)
elif main_input == "9":
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
p = Properties()
with open(f"{cwd}\\ServerFiles-{version}\\server.properties", "w") as f:
    p.load(open(f"{cwd}\\ServerFiles-{version}\\server.properties"))
showinfo(title="Minecraft Server", message="Server will be created/started in a moment after closing this popup! Type "
                                           "'STOP' and press 'ENTER' in the console window to shutdown the "
                                           "server! Also, if you are using ngrok, your server's ip can be found in "
                                           "the ngrok window "
                                           "next to 'Forwarding' and should follow the format: '("
                                           "numbers).tcp.ngrok.io:(more_numbers)! If you are not using ngrok "
                                           "and are port forwarded, the server ip will be your computer's ip with the "
                                           f"port '{str(p.get('server-port').data)}'! Have Fun!")
server_properties = str(open(f"{cwd}\\ServerFiles-{version}\\server.properties", "r").read())
print("---SERVER PROPERTIES---")
print(server_properties)
print(f"Starting Minecraft Server On {version}")
os.system(f"java -Xmx{ram_input}M -Xms{ram_input}M -jar server.jar nogui")
time.sleep(1)
print("Server Stopped...")
showinfo(title="Minecraft Server", message="Server Stopped Successfully!")
print("Exiting...")
time.sleep(1)
sys.exit(0)
