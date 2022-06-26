import ctypes
import glob
import json
import os
import subprocess
import sys
import time
import urllib
from shutil import rmtree, copy, which, copytree
from tkinter.filedialog import askdirectory

import click
import pyautogui as kbm
import requests
from click import confirm
from jproperties import Properties


@click.command()
@click.argument("command", default="help")
def main(command):
    if command.upper() == "HELP" or command.upper() == "H":
        print("---EasyMinecraftServer CLI Tool Help---")
        print("Arguments:")
        print("help - displays this help message")
        print("launch - launches the main program")
        print("update - Checks for updates and updates if available")
        print("uninstall - uninstalls the program")
        print("start - starts the Minecraft Server")
        print("reset - resets a server")
        print("cb - create a backup of server")
        print("rb - restore a backup of server")
        print("cm - use a custom map in a server")
        print("rd - reset a dimension in a server")
        print("sp - edit server properties")
        print("ies - import an external server into the program")
        return
    elif command.upper() == "LAUNCH" or command.upper() == "L":
        os.startfile("EasyMinecraftServer.exe")
        print("Launched EasyMinecraftServer.exe")
        return
    elif command.upper() == "START" or command.upper() == "S":
        start_server()
        return
    elif command.upper() == "RESET" or command.upper() == "R":
        reset_server()
        return
    elif command.upper() == "CREATEBACKUP" or command.upper() == "CBACKUP" or command.upper() == "CB":
        create_server_backup()
        return
    elif command.upper() == "RESTOREBACKUP" or command.upper() == "RESTORE" or command.upper() == "RB":
        restore_server_backup()
        return
    elif command.upper() == "CUSTOMMAP" or command.upper() == "CM":
        inject_custom_map()
        return
    elif command.upper() == "RESETDIMENSION" or command.upper() == "RDIMENSION" or command.upper() == "RD":
        reset_dimension_main()
        return
    elif command.upper() == "SERVERPROPERTIES" or command.upper() == "PROPERTIES" or command.upper() == "PROP" or command.upper() == "SP":
        change_server_properties()
        return
    elif command.upper() == "IMPORTEXTERNALSERVER" or command.upper() == "IMPORTEXTERNAL" or command.upper() == "EXTERNALSERVER" or command.upper() == "EXTERNAL" or command.upper() == "IES":
        import_external_server()
        return
    elif command.upper() == "UPDATE":
        update_program()
        return
    elif command.upper() == "UNINSTALL":
        confirm_uninstall = confirm("Are you sure you want to uninstall the program?")
        if confirm_uninstall:
            reset_all = confirm("Would you like to reset all settings and data including backups?")
            if reset_all:
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
                except Exception as e:
                    print(f"Error while resettings data: {e}")
                    print("EasyMinecraftServer data reset failed!")
                    pass
            else:
                print("Settings and data will not be reset...")
                pass
            remove_av = confirm("Would you like to remove Anti-Virus Exclusions?")
            if remove_av:
                print("Calling Anti-Virus Exception Remover...")
                os.system("MinecraftServerUnelevator.exe")
                print("Removed Anti-Virus Exclusions...")
                pass
            else:
                print("Anti-Virus Exclusions will not be removed...")
                pass
            print("Sorry to see you go! Hope you come back soon!")
            time.sleep(1)
            os.startfile(f"{cwd}\\unins000.exe")
            return
        else:
            print("Uninstall cancelled.")
            return
    else:
        print("This command does not exist! For a list of available commands type 'mcserver help'")
        return


def start_server():
    version_selection = click.prompt(
        "Enter the version you want to use! This can be any version but must be in the format 'num.num.num'!", type=str)
    server_download_url = f"https://serverjars.com/api/fetchJar/vanilla/{version_selection}/"
    if not os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\"):
        print(f"New server version entered: {version_selection}")
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}"):
            subdirs = set([os.path.dirname(p) for p in
                           glob.glob(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\")])
            if len(subdirs) == 0:
                pass
            else:
                print("Found server backups")
                restore_ask = click.confirm(
                    "Server backups for this version were found! Would you like to restore one?")
                if restore_ask:
                    backup_files = str(askdirectory(title="Select Backup",
                                                    initialdir=f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version_selection}\\"))
                    if not os.path.exists(f"{backup_files}\\server.jar") or not os.path.exists(
                            f"{backup_files}\\") or backup_files == "":
                        print("Invalid Backup Selected In start_server()")
                        return
                    else:
                        print("Valid Backup Selected In start_server()")
                        print(
                            "Copying from " + f"{backup_files}\\" + " to " + f"{cwd}\\ServerFiles-{version_selection}\\")
                        copytree(f"{backup_files}\\", f"{cwd}\\ServerFiles-{version_selection}\\")
                        print("Restore Succesful! Please restart server!")
                        return
                else:
                    print("Server restore cancelled")
                    pass
                pass
            pass
        else:
            pass
        print(f"Setting up new server version: {version_selection}")
        os.mkdir(f"{cwd}\\ServerFiles-{version_selection}\\")
        print("Created server directory")
        print(f"Creating ServerFiles Exclusion Path for version {version_selection}")
        subprocess.call(f"powershell -Command Add-MpPreference -ExclusionPath '{cwd}\\ServerFiles-{version_selection}\\'")
        print("Created server files exclusion path")
        print(f"Downloading server version {version_selection}")
        try:
            f = open(f"{cwd}\\ServerFiles-{version_selection}\\server.jar", 'wb')
            print(
                "To create a new server version, the server files will need to be downloaded! This may take a minute!")
            print("Downloading server jar file...")
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
            print("Server jar file downloaded")
            eula_check = click.confirm(
                "Do you agree to the minecraft server EULA? https://account.mojang.com/documents/minecraft_eula")
            if eula_check:
                copy(f"{cwd}\\UniversalServerFilesDefaults\\eula.txt",
                     f"{cwd}\\ServerFiles-{version_selection}\\eula.txt")
                pass
            else:
                print("You must agree to the EULA to use this program!")
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
                print("Injecting Chimpanzee222 as an operator")
                copy(f"{cwd}\\UniversalServerFilesDefaults\\ops.json",
                     f"{cwd}\\ServerFiles-{version_selection}\\ops.json")
                print("Copied ops.json")
                pass
            else:
                pass
            print("Server files set up")
            pass
        except Exception as e:
            print(
                f"The server files may not be supported or were unable to be downloaded! Error while downloading new server files: {e}")
            f.close()
            rmtree(f"{cwd}\\ServerFiles-{version_selection}\\")
            return
        pass
    else:
        print("Server version already exists")
        pass
    if os.path.exists(f"{cwd}\\ServerFiles-{version_selection}\\server.proeprties"):
        server_prop_check = open(f"{cwd}\\ServerFiles-{version_selection}\\server.properties", 'r')
        if "port" in str(server_prop_check.read()):
            server_prop_check.close()
            print("reading server properties file for server port...")
            p = Properties()
            with open(f"{cwd}\\ServerFiles-{version_selection}\\server.properties", 'rb') as f:
                p.load(f)
            port = str(p.get("server-port").data)
            print(f"Using port {port}...")
            pass
        else:
            server_prop_check.close()
            print("Defaulting to port 25565...")
            port = "25565"
            pass
    else:
        print("Defaulting to port 25565...")
        port = "25565"
        pass
    port_forwarded = click.confirm(f"Is tcp port {port} forwarded on your network? Select 'NO' if you are not sure!")
    if port_forwarded:
        print("Already port forwarded...")
        port_forward_status = "True"
        pass
    else:
        print("Not port forwarded...")
        port_forward_status = "False"
        print("Launching ngrok for server port forwarding...")
        authtoken = settings_json["ngrok_authtoken"]
        os.system("start cmd")
        time.sleep(1)
        kbm.typewrite(f"cd {cwd}\n")
        kbm.typewrite("cd ngrok\n")
        kbm.typewrite(f"ngrok authtoken {authtoken}\n")
        kbm.typewrite(f"ngrok tcp {port}\n")
        time.sleep(1)
        pass
    server_gui_setting = settings_json["server_gui"]
    ram_amount = settings_json["ram_allocation_amount"]
    server_backup = settings_json["auto_server_backup"]
    print(f"Server GUI setting: {server_gui_setting}")
    print(f"RAM allocation amount: {ram_amount}")
    print(f"Server backup setting: {server_backup}")
    launch_version_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt", 'w+')
    try:
        launch_version_file.truncate(0)
        pass
    except Exception:
        pass
    launch_version_file.write(f"{version_selection}")
    launch_version_file.close()
    if server_gui_setting == "True":
        print("Starting server with GUI...")
        os.system("start powershell")
        time.sleep(1)
        kbm.typewrite(f"MinecraftServerGUI {ram_amount} {server_backup} {port_forward_status} {port}\n")
        kbm.typewrite("exit\n")
        time.sleep(1)
        return
    else:
        print("Starting server without GUI...")
        os.system("start powershell")
        time.sleep(1)
        kbm.typewrite(f"MinecraftServer-nogui {ram_amount} {server_backup} {port_forward_status} {port}\n")
        time.sleep(1)
        return


def reset_server():
    reset_version = click.prompt(
        "Enter the version you want to reset! This can be any version but must be in the format 'num.num.num'!")
    if os.path.exists(f"{cwd}\\ServerFiles-{reset_version}\\"):
        if os.path.exists(f"{cwd}\\ServerFiles-{reset_version}\\"):
            backup_current_server = click.confirm("You have current data in the server! Would you like "
                                                  "to perform a backup?")
            if backup_current_server:
                print("Performing Server Backup Before Resetting...")
                current_time = time.time()
                backup_name = click.prompt("Enter a name for the backup!", type=str, default=str(current_time))
                if not backup_name:
                    print("Invalid Name!")
                    return
                else:
                    pass
                if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\"):
                    os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\")
                    pass
                else:
                    pass
                if os.path.exists(
                        f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\{backup_name}\\"):
                    print("Backup with the same name already exists! Please try again!")
                    return
                else:
                    try:
                        copytree(f"{cwd}\\ServerFiles-{reset_version}\\",
                                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{reset_version}\\{backup_name}\\")
                        print("Server Backup Successful")
                        pass
                    except Exception as e:
                        print(f"Error while performing backup: {e}")
                    return
            else:
                print("You have chosen not to backup the current "
                      "server! Current server data will be "
                      "overwritten!")
                pass
            pass
        try:
            print("Performing Server Reset")
            print(f"Removing ExclusionPath for ServerFiles-{reset_version}")
            subprocess.call(f"powershell -Command Remove-MpPreference -ExclusionPath '{cwd}\\ServerFiles-{reset_version}\\'")
            print("Removed ExclusionPath")
            rmtree(f"{cwd}\\ServerFiles-{reset_version}\\")
            print("Removed ServerFiles-{reset_version} directory")
            print("Server Reset Successful!")
            return
        except Exception as e:
            print(f"Error While Resetting Server: {e}")
            return
    else:
        print("Invalid Version!")
        return


def create_server_backup():
    backup_version = click.prompt(
        "Enter the version you want to backup! This can be any version but must be in the format 'num.num.num'!")
    backup_name = click.prompt("Enter a name for the backup!", type=str, default=str(time.time()))
    if not os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\"):
        print("The server version you are trying to backup does not exist!")
        return
    else:
        pass
    if not backup_name or backup_name == "" or backup_name.isspace():
        print("Invalid Name!")
        return
    else:
        pass
    if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\"):
        print("Backup with the same name already exists! Please try again!")
        return
    else:
        try:
            if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"):
                print(f"Creating new backup direcotry for version {backup_version}")
                os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\")
                pass
            else:
                pass
            print("Performing Server Backup")
            print(
                "Copying from " + f"{cwd}\\ServerFiles-{backup_version}\\" + " to " + f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            copytree(f"{cwd}\\ServerFiles-{backup_version}\\",
                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
            print("Backup Successful")
            return
        except Exception as e:
            print(f"Error while performing backup: {e}")
            return


def restore_server_backup():
    backup_version = click.prompt(
        "Enter the version you want to restore! This can be any version but must be in the format 'num.num.num'!")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"):
        print("The backup version you are trying to restore does not exist!")
        return
    else:
        pass
    backup_path = str(askdirectory(title="Restore Server Backup",
                                   initialdir=f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\"))
    if backup_version not in backup_path:
        print("Those files are unusable in this server version!")
        return
    else:
        pass
    if not os.path.exists(f"{backup_path}\\server.jar"):
        print("This backup is invalid and wont work!")
        return
    else:
        confirm_restore = click.confirm("Are you sure you want to restore this backup?")
        if confirm_restore:
            if os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\ops.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\banned-players.json\\") or \
                    os.path.exists(f"{cwd}\\ServerFiles-{backup_version}\\banned-ips.json\\"):
                print("Existing server files found...")
                backup_current_server = click.confirm(
                    "You have current data in the server! Would you like to perform a backup?")
                if backup_current_server:
                    backup_name = click.prompt("Enter the name of the backup", type=str, default=str(time.time()))
                    if not backup_name:
                        print("Invalid Name! Please Try Again!")
                        return
                    else:
                        pass
                    if os.path.exists(
                            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\"):
                        print("Backup with the same name already exists! Please try again!")
                        return
                    else:
                        try:
                            copytree(f"{cwd}\\ServerFiles-{backup_version}\\",
                                     f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{backup_version}\\{backup_name}\\")
                            print("Backup Successful!")
                            pass
                        except Exception as e:
                            print(f"Error while performing backup: {e}")
                            return
                        pass
                else:
                    print("You have chosen not to backup current server files...")
                    print("Current server files will be overwritten!")
                    pass
                pass
            else:
                pass
            try:
                print("Performing Server Restore...")
                rmtree(f"{cwd}\\ServerFiles-{backup_version}\\")
                print("Removed Old Server Files...")
                copytree(f"{backup_path}\\", f"{cwd}\\ServerFiles-{backup_version}\\")
                print("Copied Backup Files...")
                print("Restore Successful...")
                return
            except Exception as e:
                print(f"Error while restoring backup: {e}")
                return
        else:
            print("Server Restore Cancelled...")
            return


def inject_custom_map():
    version = click.prompt(
        "Enter the version you want to inject the map into! This can be any version but must be in the format 'num.num.num'!")
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        print("Invalid Version!")
        return
    else:
        pass
    custom_map = str(askdirectory(title="Select Custom Map Folder"))
    if custom_map is None:
        print("Invalid folder selected!")
        return
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\ops.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-players.json\\") or \
                os.path.exists(f"{cwd}\\ServerFiles-{version}\\banned-ips.json\\"):
            print("Current Server Files Detected")
            backup_current_server = click.confirm(
                "You have current data in the server! Would you like to perform a backup?")
            if backup_current_server:
                print("Performing backup...")
                backup_name = click.prompt("Enter the name of the backup", type=str, default=str(time.time()))
                if not backup_name:
                    print("Invalid Name! Please Try Again!")
                    return
                else:
                    pass
                if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\"):
                    os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\")
                    pass
                else:
                    pass
                if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
                    print("Backup with the same name already exists! Please try again!")
                else:
                    try:
                        copytree(f"{cwd}\\ServerFiles-{version}\\",
                                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
                        print("Server Backup Successful")
                        pass
                    except Exception as e:
                        print(f"Error while performing backup: {e}")
                        return
                    pass
                pass
            else:
                print("No backup will be performed!")
                pass
            pass
        else:
            pass
        try:
            server_prop = open(f"{cwd}\\ServerFiles-{version}\\server.properties", "r")
            if "level-name" in str(server_prop.read()):
                p = Properties()
                p.load(open(f"{cwd}\\ServerFiles-{version}\\server.properties", "rb"))
                level_name = p.get("level-name").data
                pass
            else:
                level_name = "world"
                pass
            print("Performing Custom Map Injection")
            rmtree(f"{cwd}\\ServerFiles-{version}\\{level_name}\\")
            copytree(f"{custom_map}\\", f"{cwd}\\ServerFiles-{version}\\{level_name}\\")
            print("Custom Map Injection Successful")
            pass
        except Exception as e:
            print(f"Error while injecting custom map: {e}")
            pass
        return


def change_server_properties():
    properties_version = click.prompt(
        "Enter the version you want to change the properties for! This can be any version but must be in the format 'num.num.num'!")
    try:
        os.startfile(f"{cwd}\\ServerFiles-{properties_version}\\server.properties")
        print("Launched server properties file...")
        return
    except Exception as e:
        print(f"Error while launching server properties file: {e}")
        return


def reset_nether():
    version = click.prompt(
        "Enter the version you want to reset the nether for! This can be any version but must be in the format 'num.num.num'!")
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        print("Invalid Version!")
        return
    else:
        pass
    backup_ask = click.confirm("You have current data in the server! Would you like to perform a backup?")
    if backup_ask:
        backup_name = click.prompt("Enter the name of the backup", type=str, default=str(time.time()))
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
            print("Backup with the same name already exists! Please try again!")
            return
        else:
            pass
        print("Performing backup...")
        copytree(f"{cwd}\\ServerFiles-{version}\\",
                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
        print("Backup Successful...")
        pass
    else:
        print("No backup will be performed...")
        pass
    reset_ask = click.confirm("Are you sure you want to reset the nether?")
    if reset_ask:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\world\\DIM-1\\region\\"):
            pass
        else:
            print("Nether files not found in server!")
            return
        print("Performing Nether Reset...")
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM-1\\region\\")
            print("Nether Reset Successful...")
            return
        except Exception as e:
            print(f"Error while resetting nether: {e}")
            return
    else:
        print("Nether Reset Cancelled...")
        return


def reset_end():
    version = click.prompt(
        "Enter the version you want to reset the end for! This can be any version but must be in the format 'num.num.num'!")
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        print("Invalid Version!")
        return
    else:
        pass
    backup_ask = click.confirm("You have current data in the server! Would you like to perform a backup?")
    if backup_ask:
        backup_name = click.prompt("Enter the name of the backup", type=str, default=str(time.time()))
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
            print("Backup with the same name already exists! Please try again!")
            return
        else:
            pass
        print("Performing backup...")
        copytree(f"{cwd}\\ServerFiles-{version}\\",
                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
        print("Backup Successful...")
        pass
    else:
        print("No backup will be performed...")
        pass
    reset_ask = click.confirm("Are you sure you want to reset the end?")
    if reset_ask:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\world\\DIM1\\region\\"):
            pass
        else:
            print("End files not found in server!")
            return
        print("Performing End Reset...")
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\DIM1\\region\\")
            print("End Reset Successful...")
            return
        except Exception as e:
            print(f"Error while resetting end: {e}")
            return
    else:
        print("End Reset Cancelled...")
        return


def reset_overworld():
    version = click.prompt(
        "Enter the version you want to reset the overworld for! This can be any version but must be in the format 'num.num.num'!")
    if not os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
        print("Invalid Version!")
        return
    else:
        pass
    backup_ask = click.confirm("You have current data in the server! Would you like to perform a backup?")
    if backup_ask:
        backup_name = click.prompt("Enter the name of the backup", type=str, default=str(time.time()))
        if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
            print("Backup with the same name already exists! Please try again!")
            return
        else:
            pass
        print("Performing backup...")
        copytree(f"{cwd}\\ServerFiles-{version}\\",
                 f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
        print("Backup Successful...")
        pass
    else:
        print("No backup will be performed...")
        pass
    reset_ask = click.confirm("Are you sure you want to reset the overworld?")
    if reset_ask:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\world\\region\\"):
            pass
        else:
            print("Overworld files not found in server!")
            return
        print("Performing Overworld Reset...")
        try:
            rmtree(f"{cwd}\\ServerFiles-{version}\\world\\region\\")
            print("Overworld Reset Successful...")
            return
        except Exception as e:
            print(f"Error while resetting overworld: {e}")
            return
    else:
        print("Overworld Reset Cancelled...")
        return


def reset_dimension_main():
    print("Select the number of the dimension you want to reset!")
    print("1. Nether")
    print("2. The End")
    print("3. Overworld")
    dimension_number = click.prompt("Enter the number of the dimension you want to reset!", type=int)
    if not dimension_number:
        print("Invalid Dimension Number! Please Try Again!")
        return
    else:
        if dimension_number == 1:
            reset_nether()
            return
        elif dimension_number == 2:
            reset_end()
            return
        elif dimension_number == 3:
            reset_overworld()
            return
        else:
            print("Invalid Dimension Number! Please Try Again!")
            return


def import_external_server():
    version = click.prompt(
        "Enter the version you want to import the server for! This can be any version but must be in the format 'num.num.num'!")
    import_files = str(askdirectory(title="Select Folder To Import"))
    if not os.path.exists(f"{import_files}\\world\\") or not os.path.exists(
            f"{import_files}\\server.properties") or not os.path.exists(
        f"{import_files}\\eula.txt") or not os.path.exists(f"{import_files}\\ops.json") or not os.path.exists(
        f"{import_files}\\banned-ips.json") or not os.path.exists(
        f"{import_files}\\banned-players.json") or not os.path.exists(
        f"{import_files}\\whitelist.json"):
        print("Invalid Folder! Please Try Again!")
        return
    else:
        if os.path.exists(f"{cwd}\\ServerFiles-{version}\\"):
            backup_ask = click.confirm("You have current data in the server! Would you like to perform a backup?")
            if backup_ask:
                backup_name = click.prompt("Enter the name of the backup", type=str, default=str(time.time()))
                if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\"):
                    print("Backup with the same name already exists! Please try again!")
                    return
                else:
                    pass
                print("Performing backup...")
                copytree(f"{cwd}\\ServerFiles-{version}\\",
                         f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\{backup_name}\\")
                print("Backup Successful...")
                pass
            else:
                print("No backup will be performed...")
                pass
            pass
        else:
            pass
        print("Performing Import...")
        try:
            copytree(f"{import_files}\\", f"{cwd}\\ServerFiles-{version}\\")
            print("Import Successful...")
            return
        except Exception as e:
            print(f"Error while importing: {e}")
            return


def update_program():
    try:
        url = "http://github.com/teekar2023/EasyMinecraftServer/releases/latest/"
        r = requests.get(url, allow_redirects=True)
        redirected_url = r.url
        pass
    except Exception as e:
        print(f"There was an error while checking for updates: {e}")
        return
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.12.0":
        new_version = redirected_url.replace("https://github.com/teekar2023/EasyMinecraftServer/releases/tag/", "")
        print(f"Update available: {new_version}")
        new_url = str(redirected_url) + f"/EasyMinecraftServerInstaller-{str(new_version.replace('v', ''))}.exe"
        download_url = new_url.replace("tag", "download")
        print("Download url: " + download_url)
        if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\"):
            os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\")
            pass
        else:
            pass
        try:
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
            pass
        print(f"Changelog:\n{changelog_txt}")
        confirm_update = confirm(f"Would you like to update to version {new_version}?")
        if confirm_update:
            try:
                f = open(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe",
                    'wb')
                print("Downloading update installer...")
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
                print("Update Downloaded Successfully! Installer Will Now Be Launched To Complete Update!")
                time.sleep(5)
                os.startfile(
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Update-{new_version}\\EasyMinecraftServerInstaller-{new_version}.exe")
                return
            except Exception as e:
                print(f"There was an error while downloading the update: {e}")
                return
        else:
            print("Update cancelled.")
            return
    else:
        print("Latest version of EasyMinecraftServer is already installed!")
        return


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
            print("EasyMinecraftServer has not been set up yet! Please launch the main program to setup!")
            launch_confirm = click.confirm("Would you like to launch the main program now?")
            if launch_confirm:
                os.startfile("EasyMinecraftServer.exe")
                print("Launched EasyMinecraftServer.exe")
                print("Exiting...")
                sys.exit(0)
            else:
                print("Exiting...")
                sys.exit(0)
        else:
            pass
        break
    return True


def av_exclusions():
    exclusion_confirm = confirm("Would you like to launch the anti-virus exception creator to make all program and server files not be scanned by your antivirus program?")
    if exclusion_confirm:
        print("Launching Anti-Virus Exclusion Creator...")
        time.sleep(1)
        os.startfile("MinecraftServerElevator.exe")
        sys.exit(0)
    else:
        return


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    os.system("title EasyMinecraftServer")
    os.system("cls")
    print("EasyMinecraftServer v2.12.0")
    if is_admin():
        pass
    else:
        print(
            "EasyMinecraftServer CLI Tool requires admin privileges to run. Please run your terminal window as administrator.")
        sys.exit(0)
    user_dir = os.path.expanduser("~")
    print(f"User Directory: {user_dir}")
    cwd = which("EasyMinecraftServer").replace("\\EasyMinecraftServer.EXE", "")
    if cwd == ".":
        cwd = os.getcwd()
        pass
    else:
        pass
    print(f"Program Installation Directory: {cwd}")
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
    info = subprocess.STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    subprocess.Popen([f"{cwd}\\ngrok\\ngrok.exe", "config", "upgrade"], startupinfo=info)
    create_ngrok_secret = subprocess.Popen(["SecretManager.exe", "create"], startupinfo=info)
    ngrok_secret = str(os.environ.get("MinecraftServerNgrokSecret"))
    if settings_json["ngrok_authtoken"] == ngrok_secret:
        print("Authtoken for ngrok is the same as dev authtoken")
        pass
    else:
        pass
    remove_ngrok_secret = subprocess.Popen(["SecretManager.exe", "remove"], startupinfo=info)
    os.system("cls")
    print("EasyMinecraftServer v2.12.0")
    print(f"User Directory: {user_dir}")
    print(f"Program Installation Directory: {cwd}")
    url = "http://github.com/teekar2023/EasyMinecraftServer/releases/latest/"
    r = requests.get(url, allow_redirects=True)
    redirected_url = r.url
    if redirected_url != "https://github.com/teekar2023/EasyMinecraftServer/releases/tag/v2.12.0":
        update_program()
        pass
    else:
        file_path = f"{user_dir}\\Documents\\EasyMinecraftServer\\"
        file_list = os.listdir(file_path)
        for folder in file_list:
            if "Update" in folder:
                print(f"Deleting update folder: {user_dir}\\Documents\\EasyMinecraftServer\\{folder}")
                rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\{folder}")
                pass
            else:
                pass
        pass
    os.system("cls")
    print("EasyMinecraftServer v2.12.0")
    print(f"User Directory: {user_dir}")
    print(f"Program Installation Directory: {cwd}")
    main()
    sys.exit(0)
