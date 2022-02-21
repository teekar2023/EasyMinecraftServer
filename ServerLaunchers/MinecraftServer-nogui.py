import click
import os
import sys
import time
from shutil import rmtree, copytree


@click.command()
@click.argument("s_version")
@click.argument("ram_amount")
@click.argument("auto_server_backup")
def main(s_version, ram_amount, auto_server_backup):
    cwd = os.getcwd()
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
    os.chdir(f"{str(cwd).replace('ServerLaunchers', '')}\\ServerFiles-{version}\\")
    if version == "1.8.9":
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_17-111.xml -jar server.jar nogui")
        pass
    elif version == "1.12.2":
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar nogui")
        pass
    elif version == "1.16.5":
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j.configurationFile=log4j2_112-116.xml -jar server.jar nogui")
        pass
    elif version == "1.17.1":
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -Dlog4j2.formatMsgNoLookups=true -jar server.jar nogui")
        pass
    elif version == "1.18.1":
        os.system(f"java -Xmx{ram_amount}M -Xms{ram_amount}M -jar server.jar nogui")
        pass
    else:
        print("Version not supported")
        sys.exit(1)
    if auto_server_backup == "True":
        print("Auto Backup Started...")
        auto_backup()
        pass
    else:
        pass
    sys.exit(0)


def auto_backup(version):
    cwd = os.getcwd()
    user_dir = os.path.expanduser("~")
    print("Auto Backup Started...")
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
        os.remove(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt")
        rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{last_auto_backup}\\")
        pass
    else:
        pass
    current_time = time.time()
    copytree(f"{cwd}\\",
            f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{current_time}\\")
    last_auto_backup_file = open(
        f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt", 'w+')
    last_auto_backup_file.write(str(current_time))
    last_auto_backup_file.close()
    return


if __name__ == "__main__":
    main()
