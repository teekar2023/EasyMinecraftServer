#  Copyright (c) 2022. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

import os
import sys
from shutil import copy, copytree, rmtree

cwd = os.getcwd()
print("Current working directory: " + cwd)
print("Removing old builds...")
if os.path.exists(f"{cwd}\\ngrok\\.ngrok.exe.old"):
    os.remove(f"{cwd}\\ngrok\\.ngrok.exe.old")
    print("Removed old ngrok.exe")
    pass
else:
    pass
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
print("Removing cv2 folder in EasyMinecraftServer.exe dist folder...")
if os.path.exists(f"{cwd}\\dist\\EasyMinecraftServer\\cv2\\"):
    rmtree(f"{cwd}\\dist\\EasyMinecraftServer\\cv2\\")
    print("Removed cv2 folder...")
    pass
else:
    print("Folder not found...")
    pass
print("Copying Sun Valley tcl theme files...")
os.mkdir(f"{cwd}\\dist\\EasyMinecraftServer\\sv_ttk\\")
copy(f"{cwd}\\SunValleyThemes\\sun-valley.tcl", f"{cwd}\\dist\\EasyMinecraftServer\\sv_ttk\\sun-valley.tcl")
copytree(f"{cwd}\\SunValleyThemes\\theme", f"{cwd}\\dist\\EasyMinecraftServer\\theme\\")
print("Compiling mcserver.py to mcserver.exe...")
print("Executing pyinstaller mcserver.py")
os.system("pyinstaller mcserver.py")
print("Compiling MinecraftServerElevator.py to MinecraftServerElevator.exe...")
print("Executing pyinstaller --onefile MinecraftServerElevator.py")
os.system("pyinstaller --onefile MinecraftServerElevator.py")
print("Compiling MinecraftServerUnelevator.py to MinecraftServerUnelevator.exe...")
print("Executing pyinstaller --onefile MinecraftServerUnelevator.py")
os.system("pyinstaller --onefile MinecraftServerUnelevator.py")
print("Compiling SecretManager.py to SecretManager.exe")
print("Executing pyinstaller --onefile SecretManager.py")
os.system("pyinstaller --onefile SecretManager.py")
print("Compliling ServerAutoBackup.pyw to ServerAutoBackup.exe")
print("Executing pyinstaller --onefile ServerAutoBackup.pyw")
os.system("pyinstaller --onefile ServerAutoBackup.pyw")
print("Compiling SystemOptimizer.pyw to SystemOptimizer.exe")
os.system("pyinstaller --onefile SystemOptimizer.pyw")
copytree(f"{cwd}\\UniversalServerFilesDefaults\\", f"{cwd}\\dist\\EasyMinecraftServer\\UniversalServerFilesDefaults\\")
print(f"Copied UniversalServerFilesDefaults to {cwd}\\dist\\EasyMinecraftServer\\UniversalServerFilesDefaults\\")
copytree(f"{cwd}\\ngrok\\", f"{cwd}\\dist\\EasyMinecraftServer\\ngrok\\")
print(f"Copied ngrok to {cwd}\\dist\\EasyMinecraftServer\\ngrok\\")
copy(f"{cwd}\\dist\\mcserver\\mcserver.exe", f"{cwd}\\dist\\EasyMinecraftServer\\mcserver.exe")
print(f"Copied mcserver.exe to {cwd}\\dist\\mcserver.exe")
if os.path.exists(f"{cwd}\\dist\\mcserver\\"):
    print("Removing mcserver.exe dist directory...")
    rmtree(f"{cwd}\\dist\\mcserver\\")
    print("Removed mcserver.exe dist directory...")
    pass
else:
    print("mcserver.exe dist directory not found...")
    pass
copy(f"{cwd}\\dist\\MinecraftServerElevator.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerElevator.exe")
print(f"Copied MinecraftServerElevator.exe to {cwd}\\dist\\EasyMinecraftServer\\MinecraftServerElevator.exe")
copy(f"{cwd}\\dist\\MinecraftServerUnelevator.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerUnelevator.exe")
print(f"Copied MinecraftServerUnelevator.exe to {cwd}\\dist\\EasyMinecraftServer\\MinecraftServerUnelevator.exe")
copy(f"{cwd}\\dist\\SecretManager.exe", f"{cwd}\\dist\\EasyMinecraftServer\\SecretManager.exe")
print(f"Copied SecretManager.exe to {cwd}\\dist\\EasyMinecraftServer\\SecretManager.exe")
copy(f"{cwd}\\dist\\ServerAutoBackup.exe", f"{cwd}\\dist\\EasyMinecraftServer\\ServerAutoBackup.exe")
print(f"Copied ServerAutoBackup.exe to {cwd}\\dist\\EasyMinecraftServer\\ServerAutoBackup.exe")
copy(f"{cwd}\\dist\\SystemOptimizer.exe", f"{cwd}\\dist\\EasyMinecraftServer\\SystemOptimizer.exe")
print(f"Copied SystemOptimizer.exe to {cwd}\\dist\\EasyMinecraftServer\\SystemOptimizer.exe")
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
copy(f"{cwd}\\mc.bmp", f"{cwd}\\dist\\EasyMinecraftServer\\mc.bmp")
print(f"Copied mc.bmp to {cwd}\\dist\\EasyMinecraftServer\\mc.bmp")
print("Removing old ServerLaunchers builds...")
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
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServer-nogui.exe",
     f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServer-nogui.exe")
print(f"Copied MinecraftServer-nogui.exe to {cwd}\\dist\\EasyMinecraftServer\\MinecraftServer-nogui.exe")
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServerGUI.exe",
     f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerGUI.exe")
print(f"Copied MinecraftServerGUI.exe to {cwd}\\dist\\EasyMinecraftServer\\MinecraftServerGUI.exe")
os.chdir("C:\\Program Files (x86)\\Inno Setup 6\\")
print("New working directory: " + os.getcwd())
print("Compiling installer...")
os.system(f'ISCC "{cwd}\\InstallerFiles\\MinecraftServerInstaller.iss"')
print("Done!")
print("Exiting...")
sys.exit(0)
