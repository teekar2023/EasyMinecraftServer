import os
import sys
from shutil import copytree, copy, rmtree

cwd = os.getcwd()
if os.path.exists(f"{cwd}\\dist\\"):
    rmtree(f"{cwd}\\dist\\")
    pass
else:
    pass
if os.path.exists(f"{cwd}\\build\\"):
    rmtree(f"{cwd}\\build\\")
    pass
else:
    pass
if os.path.exists(f"{cwd}\\__pycache__\\"):
    rmtree(f"{cwd}\\__pycache__\\")
    pass
else:
    pass
os.system("pyinstaller -i mc.ico EasyMinecraftServer.pyw")
os.system("pyinstaller --onefile MinecraftServerElevator.py")
copytree(f"{cwd}\\UniversalServerFilesDefaults\\", f"{cwd}\\dist\\EasyMinecraftServer\\UniversalServerFilesDefaults\\")
copytree(f"{cwd}\\ngrok\\", f"{cwd}\\dist\\EasyMinecraftServer\\ngrok\\")
copy(f"{cwd}\\dist\\MinecraftServerElevator.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerElevator.exe")
copy(f"{cwd}\\CHANGELOG.txt", f"{cwd}\\dist\\EasyMinecraftServer\\CHANGELOG.txt")
copy(f"{cwd}\\LICENSE.txt", f"{cwd}\\dist\\EasyMinecraftServer\\LICENSE.txt")
copy(f"{cwd}\\README.md", f"{cwd}\\dist\\EasyMinecraftServer\\README.md")
copy(f"{cwd}\\mc.ico", f"{cwd}\\dist\\EasyMinecraftServer\\mc.ico")
copy(f"{cwd}\\mc.png", f"{cwd}\\dist\\EasyMinecraftServer\\mc.png")
if os.path.exists(f"{cwd}\\ServerLaunchers\\dist\\"):
    rmtree(f"{cwd}\\ServerLaunchers\\dist\\")
    pass
else:
    pass
if os.path.exists(f"{cwd}\\ServerLaunchers\\build\\"):
    rmtree(f"{cwd}\\ServerLaunchers\\build\\")
    pass
else:
    pass
os.chdir(f"{cwd}\\ServerLaunchers\\")
os.system("pyinstaller --onefile MinecraftServer-nogui.py")
os.system("pyinstaller --onefile MinecraftServerGUI.pyw")
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServer-nogui.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServer-nogui.exe")
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServerGUI.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerGUI.exe")
print("Done!")
os.startfile(f"{cwd}\\InstallerFiles\\MinecraftServerInstaller.iss")
sys.exit(0)
