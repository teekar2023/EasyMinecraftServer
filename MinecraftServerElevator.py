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
    print("Creating Anti-Virus Exception For EasyMinecraftServer...")
    cwd = os.getcwd()
    print(f"Exclusion Path: {cwd}")
    print(f"Executing system command: powershell -Command Add-MpPreference -ExclusionPath '{cwd}'")
    subprocess.call(f"powershell -Command Add-MpPreference -ExclusionPath '{cwd}'")
    print("Finished creating Anti-Virus Exception For EasyMinecraftServer...")
else:
    print("Error: Restart With Admin Privileges...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)
