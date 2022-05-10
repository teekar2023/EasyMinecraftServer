import os
import sys
from shutil import copytree, copy, rmtree

cwd = os.getcwd()
print("Current working directory: " + cwd)
print("Removing old builds...")
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
print("Compiling EasyMinecraftServer.py to EasyMinecraftServer.exe...")
print("Executing pyinstaller -i mc.ico EasyMinecraftServer.pyw")
os.system("pyinstaller -i mc.ico EasyMinecraftServer.pyw")
print("Compiling mcserver.py to mcserver.exe...")
print("Executing pyinstaller --onefile mcserver.py")
os.system("pyinstaller --onefile mcserver.py")
print("Compiling MinecraftServerElevator.py to MinecraftServerElevator.exe...")
print("Executing pyinstaller --onefile MinecraftServerElevator.py")
os.system("pyinstaller --onefile MinecraftServerElevator.py")
copytree(f"{cwd}\\UniversalServerFilesDefaults\\", f"{cwd}\\dist\\EasyMinecraftServer\\UniversalServerFilesDefaults\\")
print(f"Copied UniversalServerFilesDefaults to {cwd}\\dist\\EasyMinecraftServer\\UniversalServerFilesDefaults\\")
copytree(f"{cwd}\\ngrok\\", f"{cwd}\\dist\\EasyMinecraftServer\\ngrok\\")
print(f"Copied ngrok to {cwd}\\dist\\EasyMinecraftServer\\ngrok\\")
copy(f"{cwd}\\dist\\mcserver.exe", f"{cwd}\\dist\\EasyMinecraftServer\\mcserver.exe")
print(f"Copied mcserver.exe to {cwd}\\dist\\EasyMinecraftServer\\mcserver.exe")
copy(f"{cwd}\\dist\\MinecraftServerElevator.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerElevator.exe")
print(f"Copied MinecraftServerElevator.exe to {cwd}\\dist\\EasyMinecraftServer\\MinecraftServerElevator.exe")
copy(f"{cwd}\\CHANGELOG.txt", f"{cwd}\\dist\\EasyMinecraftServer\\CHANGELOG.txt")
print(f"Copied CHANGELOG.txt to {cwd}\\dist\\EasyMinecraftServer\\CHANGELOG.txt")
copy(f"{cwd}\\LICENSE.txt", f"{cwd}\\dist\\EasyMinecraftServer\\LICENSE.txt")
print(f"Copied LICENSE.txt to {cwd}\\dist\\EasyMinecraftServer\\LICENSE.txt")
copy(f"{cwd}\\README.md", f"{cwd}\\dist\\EasyMinecraftServer\\README.md")
print(f"Copied README.md to {cwd}\\dist\\EasyMinecraftServer\\README.md")
copy(f"{cwd}\\mc.ico", f"{cwd}\\dist\\EasyMinecraftServer\\mc.ico")
print(f"Copied mc.ico to {cwd}\\dist\\EasyMinecraftServer\\mc.ico")
copy(f"{cwd}\\mc.png", f"{cwd}\\dist\\EasyMinecraftServer\\mc.png")
print(f"Copied mc.png to {cwd}\\dist\\EasyMinecraftServer\\mc.png")
print("Removiing old ServerLaunchers builds...")
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
print("New working directory: " + os.getcwd())
print("Compiling MinecraftServer-nogui.py to MinecraftServer-nogui.exe...")
os.system("pyinstaller --onefile MinecraftServer-nogui.py")
print("Compiling MinecraftServerGUI.pyw to MinecraftServerGUI.exe...")
os.system("pyinstaller --onefile MinecraftServerGUI.pyw")
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServer-nogui.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServer-nogui.exe")
print(f"Copied MinecraftServer-nogui.exe to {cwd}\\dist\\EasyMinecraftServer\\MinecraftServer-nogui.exe")
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServerGUI.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerGUI.exe")
print(f"Copied MinecraftServerGUI.exe to {cwd}\\dist\\EasyMinecraftServer\\MinecraftServerGUI.exe")
print(f"Launching Installer Compiler: {cwd}\\InstallerFiles\\MinecraftServerInstaller.iss")
os.startfile(f"{cwd}\\InstallerFiles\\MinecraftServerInstaller.iss")
print("Done!")
print("Exiting...")
sys.exit(0)
