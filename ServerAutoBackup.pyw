#  Copyright (c) 2022. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

import logging
import os
import time
import json
from shutil import rmtree, copytree, which


def main():
    logging.info("Auto Backup Process Started")
    logging.info(f"Version: {version}")
    logging.info(f"Interval: {interval}")
    while True:
        time.sleep(int(interval) * 60)
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
            if os.path.exists(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{last_auto_backup}\\"):
                rmtree(f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{last_auto_backup}\\")
                logging.info("Removed last auto backup")
                pass
            else:
                logging.info("Last auto backup files not found")
                pass
            pass
        else:
            pass
        current_time = time.time()
        logging.info("Creating new auto backup: " + str(current_time))
        try:
            copytree(f"{cwd}\\ServerFiles-{version}",
                    f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\{version}\\AutomaticBackup-{str(current_time)}\\")
            last_auto_backup_file = open(
                f"{user_dir}\\Documents\\EasyMinecraftServer\\Backups\\Data\\last_auto_backup_{version}.txt", 'w+')
            last_auto_backup_file.write(str(current_time))
            last_auto_backup_file.close()
            logging.info("Auto Server Backup Complete")
            pass
        except Exception as e:
            logging.error("Auto Server Backup Failed: " + str(e))
            pass


cwd = str(which("EasyMinecraftServer")).replace("\\EasyMinecraftServer.EXE", "")
if cwd == ".":
    cwd = os.getcwd()
    pass
else:
    pass
os.chdir(cwd)
user_dir = os.path.expanduser("~")
logging.basicConfig(filename=f'{user_dir}\\Documents\\EasyMinecraftServer\\Logs\\app.log', level="DEBUG",
                    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
logging.info("Starting Auto Server Backup Process")
version_file = open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Temp\\launch_version.txt", "r")
version = version_file.read()
version_file.close()
settings_json = json.load(open(f"{user_dir}\\Documents\\EasyMinecraftServer\\Settings\\settings.json", "r"))
interval = settings_json["backup_interval"]
main()
