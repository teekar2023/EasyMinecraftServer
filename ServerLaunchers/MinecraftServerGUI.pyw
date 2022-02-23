import click
import os
import sys
import time
from shutil import rmtree, copytree
from tkinter.messagebox import showerror
import logging


@click.command()
@click.argument("s_version")
@click.argument("ram_amount")
@click.argument("auto_server_backup")
def main(s_version, ram_amount, auto_server_backup):
    if s_version == "189":
        version = "1.8.9"
        pass
    elif s_version == "1122":
        version = "1.12.2"
        pass
    elif s_version == "1165":
        version = "1.16.5"
        pass
    elif s_version == "1171":
        version = "1.17.1"
        pass
    elif s_version == "1181":
        version = "1.18.1"
        pass
    logging.info("Starting Minecraft Server with GUI")
    logging.info("Version: " + version)
    logging.info("RAM: " + ram_amount)
    logging.info("Auto Server Backup: " + auto_server_backup)
    os.chdir(f"{str(cwd).replace('ServerLaunchers', '')}\\ServerFiles-{version}\\")
    if version == "1.8.9":
        logging.info(f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_17-111.xml -jar server.jar")
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_17-111.xml -jar server.jar")
        pass
    elif version == "1.12.2":
        logging.info("Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar")
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar")
        pass
    elif version == "1.16.5":
        logging.info(f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar")
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar")
        pass
        pass
    elif version == "1.17.1":
        logging.info(f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j2.formatMsgNoLookups=true -jar server.jar")
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j2.formatMsgNoLookups=true -jar server.jar")
        pass
    elif version == "1.18.1":
        logging.info(f"Executing system command: java -Xmx{ram_amount}M -Xms{ram_amount}M -jar server.jar")
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -jar server.jar")
        pass
    else:
        showerror("Error", "Invalid Version")
        logging.error("Invalid Version")
        sys.exit(1)
    if auto_server_backup == "True":
        logging.info("Auto Server Backup Enabled")
        auto_backup(version)
        pass
    else:
        logging.info("Auto Server Backup Disabled")
        pass
    logging.info("Exiting Program")
    logging.shutdown()
    program_log_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log", "a")
    server_log_file = open(f"{cwd}\\ServerFiles-{version}\\logs\\latest.log", "r+")
    server_logs = server_log_file.read()
    program_log_file.write(server_logs)
    program_log_file.close()
    server_log_file.close()
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
    copytree(f"{cwd}\\ServerFiles-{version}\\",
            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{current_time}\\")
    last_auto_backup_file = open(
        f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt", 'w+')
    last_auto_backup_file.write(str(current_time))
    last_auto_backup_file.close()
    logging.info("Auto Server Backup Complete")
    return


if __name__ == "__main__":
    time.sleep(5)
    cwd = os.getcwd()
    user_dir = os.path.expanduser("~")
    logging.basicConfig(filename=f'{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log', filemode='r+', level="DEBUG",
                    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    main()
