import logging
import os
import socket
import sys
import time
from shutil import rmtree, copytree, which

import click
import psutil


@click.command()
@click.argument("ram_amount")
@click.argument("auto_server_backup")
@click.argument("port_forward_status")
@click.argument("port")
def main(ram_amount, auto_server_backup, port_forward_status, port):
    version_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt", "r")
    version = version_file.read()
    logging.info("Starting Minecraft Server with GUI")
    logging.info("Version: " + version)
    logging.info("RAM: " + ram_amount)
    logging.info("Auto Server Backup: " + auto_server_backup)
    logging.info("Port Forward Status: " + port_forward_status)
    logging.info("Port: " + port)
    os.chdir(f"{str(cwd).replace('ServerLaunchers', '')}\\ServerFiles-{version}\\")
    if port_forward_status == "True":
        ip = str(socket.gethostbyname(socket.gethostname()))
        logging.info("IP: " + ip)
        ip_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\ip.txt", "w+")
        ip_file.write(f"Server IP: {ip}:{port}")
        ip_file.close()
        os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\ip.txt")
        pass
    else:
        ip_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\ip.txt", "w+")
        ip_file.write(
            "To find your ip for this session, go to the ngrok window and find it next to the 'Forwarding' category. The ip will be in the format of '<number>.tcp.ngrok.io:<numbers>'")
        ip_file.close()
        os.startfile(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\ip.txt")
        pass
    list_one = ["1.7", "1.7.1", "1.7.2", "1.7.3", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9", "1.7.10", "1.8",
                "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9", "1.9.1",
                "1.9.2", "1.9.3", "1.9.4", "1.10", "1.10.1", "1.10.2", "1.11", "1.11.1", "1.11.2"]
    list_two = ["1.12", "1.12.1", "1.12.2", "1.13", "1.13.1", "1.13.2", "1.14", "1.14.1", "1.14.2", "1.14.3", "1.14.4",
                "1.15", "1.15.1", "1.15.2", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.16.5"]
    list_three = ["1.17", "1.17.1"]
    if version in list_one:
        logging.info(
            f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_17-111.xml -jar server.jar")
        os.system(
            f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_17-111.xml -jar server.jar")
        pass
    elif version in list_two:
        logging.info(
            f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar")
        os.system(
            f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar")
        pass
    elif version in list_three:
        logging.info(
            f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j2.formatMsgNoLookups=true -jar server.jar")
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j2.formatMsgNoLookups=true -jar server.jar")
        pass
    else:
        logging.info(f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -jar server.jar")
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -jar server.jar")
        pass
    if auto_server_backup == "True":
        logging.info("Auto Server Backup Enabled")
        auto_backup(version)
        pass
    else:
        logging.info("Auto Server Backup Disabled")
        pass
    logging.info("Exiting Program")
    logging.shutdown()
    try:
        program_log_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log", "a")
        server_log_file = open(f"{cwd}\\ServerFiles-{version}\\logs\\latest.log", "r+")
        server_logs = server_log_file.read()
        program_log_file.write(server_logs)
        program_log_file.close()
        server_log_file.close()
        pass
    except Exception as e:
        logging.error(f"Error while copying server logs: {e}")
        pass
    os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\ip.txt")
    logging.info("Removed ip.txt")
    logging.shutdown()
    sys.exit(0)


def auto_backup(version):
    logging.info("Starting Auto Server Backup")
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\")
        pass
    else:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\")
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\"):
        os.mkdir(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\")
        pass
    else:
        pass
    if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt"):
        last_auto_backup_file = open(
            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt", 'r+')
        last_auto_backup = str(last_auto_backup_file.read())
        last_auto_backup_file.close()
        logging.info("Removing last auto backup")
        os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt")
        rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{last_auto_backup}\\")
        pass
    else:
        pass
    current_time = time.time()
    logging.info("Time: " + str(current_time))
    logging.info("Creating new auto backup")
    copytree(f"{cwd}\\ServerFiles-{version}",
             f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{current_time}\\")
    last_auto_backup_file = open(
        f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt", 'w+')
    last_auto_backup_file.write(str(current_time))
    last_auto_backup_file.close()
    logging.info("Auto Server Backup Complete")
    return


if __name__ == "__main__":
    PROCNAME = "EasyMinecraftServer.exe"
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()
            pass
        else:
            pass
        pass
    time.sleep(5)
    cwd = which("EasyMinecraftServer").replace("\\EasyMinecraftServer.EXE", "")
    os.chdir(cwd)
    user_dir = os.path.expanduser("~")
    logging.basicConfig(filename=f'{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log', filemode='r+',
                        level="DEBUG",
                        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    main()
