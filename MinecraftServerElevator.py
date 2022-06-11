import ctypes
import os
from shutil import which
import subprocess
import sys
import time
import click


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if is_admin():
    print("Creating Anti-Virus Exceptions For EasyMinecraftServer...")
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
    print(f"Executing system command: powershell -Command Add-MpPreference -ExclusionPath '{cwd}'")
    subprocess.call(f"powershell -Command Add-MpPreference -ExclusionPath '{cwd}'")
    print(
        f"Executing system command: powershell -Command Add-MpPreference -ExclusionPath '{user_dir}\\Documents\\EasyMinecraftServer\\'")
    subprocess.call(
        f"powershell -Command Add-MpPreference -ExclusionPath '{user_dir}\\Documents\\EasyMinecraftServer\\'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'EasyMinecraftServer.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'EasyMinecraftServer.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'mcserver.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'mcserver.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServerGUI.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServerGUI.exe'")
    print(
        f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServer-nogui.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServer-nogui.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'java.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'java.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'javaw.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'javaw.exe'")
    print("Finished creating Anti-Virus Exceptions...")
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
