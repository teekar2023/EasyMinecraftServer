#  Copyright (c) 2022. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

import ctypes
import os
import subprocess
from shutil import which
import sys
import time
import click


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if is_admin():
    print("Removing Anti-Virus Exceptions For EasyMinecraftServer...")
    cwd_0 = which("EasyMinecraftServer").replace("\\EasyMinecraftServer.EXE", "")
    if str(cwd_0) == "None" or str(cwd_0) == "" or str(cwd_0) == " " or str(cwd_0) == ".":
        cwd = os.getcwd()
        pass
    else:
        cwd = cwd_0
        pass
    user_dir = os.path.expanduser('~')
    print("Current Working Directory: " + cwd)
    print("User Directory: " + user_dir)
    print(f"Executing system command: powershell -Command Remove-MpPreference -ExclusionPath '{cwd}'")
    subprocess.call(f"powershell -Command Remove-MpPreference -ExclusionPath '{cwd}'")
    print(
        f"Executing system command: powershell -Command Remove-MpPreference -ExclusionPath '{user_dir}\\Documents\\EasyMinecraftServer\\'")
    subprocess.call(
        f"powershell -Command Remove-MpPreference -ExclusionPath '{user_dir}\\Documents\\EasyMinecraftServer\\'")
    print(
        f"Executing system command: powershell -Command Remove-MpPreference -Exclusionprocess 'EasyMinecraftServer.exe'")
    subprocess.call(f"powershell -Command Remove-MpPreference -Exclusionprocess 'EasyMinecraftServer.exe'")
    print(f"Executing system command: powershell -Command Remove-MpPreference -Exclusionprocess 'mcserver.exe'")
    subprocess.call(f"powershell -Command Remove-MpPreference -Exclusionprocess 'mcserver.exe'")
    print(
        f"Executing system command: powershell -Command Remove-MpPreference -Exclusionprocess 'MinecraftServerGUI.exe'")
    subprocess.call(f"powershell -Command Remove-MpPreference -Exclusionprocess 'MinecraftServerGUI.exe'")
    print(
        f"Executing system command: powershell -Command Remove-MpPreference -Exclusionprocess 'MinecraftServer-nogui.exe'")
    subprocess.call(f"powershell -Command Remove-MpPreference -Exclusionprocess 'MinecraftServer-nogui.exe'")
    print(f"Executing system command: powershell -Command Remove-MpPreference -Exclusionprocess 'java.exe'")
    subprocess.call(f"powershell -Command Remove-MpPreference -Exclusionprocess 'java.exe'")
    print(f"Executing system command: powershell -Command Remove-MpPreference -Exclusionprocess 'javaw.exe'")
    subprocess.call(f"powershell -Command Remove-MpPreference -Exclusionprocess 'javaw.exe'")
    print("Finished Removing Anti-Virus Exceptions...")
    time.sleep(1)
    start_confirm = click.confirm("Would you like to start EasyMinecraftServer?", default=True)
    if start_confirm:
        print("Starting EasyMinecraftServer...")
        os.startfile(f"EasyMinecraftServer.exe")
        pass
    else:
        pass
    print("Exiting...")
    time.sleep(1)
    sys.exit(0)
else:
    print("Error: Restart With Admin Privileges...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)
