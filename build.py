import os
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
copytree(f"{cwd}\\ServerFiles-1.8.9\\", f"{cwd}\\dist\\EasyMinecraftServer\\ServerFiles-1.8.9\\")
copytree(f"{cwd}\\ServerFiles-1.12.2\\", f"{cwd}\\dist\\EasyMinecraftServer\\ServerFiles-1.12.2\\")
copytree(f"{cwd}\\ServerFiles-1.16.5\\", f"{cwd}\\dist\\EasyMinecraftServer\\ServerFiles-1.16.5\\")
copytree(f"{cwd}\\ServerFiles-1.17.1\\", f"{cwd}\\dist\\EasyMinecraftServer\\ServerFiles-1.17.1\\")
copytree(f"{cwd}\\ServerFiles-1.18.1\\", f"{cwd}\\dist\\EasyMinecraftServer\\ServerFiles-1.18.1\\")
copytree(f"{cwd}\\ngrok\\", f"{cwd}\\dist\\EasyMinecraftServer\\ngrok\\")
copytree(f"{cwd}\\JDK\\", f"{cwd}\\dist\\EasyMinecraftServer\\JDK\\")
copy(f"{cwd}\\dist\\MinecraftServerElevator.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerElevator.exe")
copy(f"{cwd}\\CHANGELOG.txt", f"{cwd}\\dist\\EasyMinecraftServer\\CHANGELOG.txt")
copy(f"{cwd}\\LICENSE.txt", f"{cwd}\\dist\\EasyMinecraftServer\\LICENSE.txt")
copy(f"{cwd}\\README.md", f"{cwd}\\dist\\EasyMinecraftServer\\README.md")
if not os.path.exists(f"{cwd}\\dist\\EasyMinecraftServer\\1.8.9-recovery\\"):
    os.mkdir(f"{cwd}\\dist\\EasyMinecraftServer\\1.8.9-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.8.9\\server.properties", f"{cwd}\\dist\\EasyMinecraftServer\\1.8.9"
                                                                         f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.8.9\\eula.txt", f"{cwd}\\dist\\EasyMinecraftServer\\1.8.9-recovery\\eula.txt")
    pass
else:
    pass
if not os.path.exists(f"{cwd}\\dist\\EasyMinecraftServer\\1.12.2-recovery\\"):
    os.mkdir(f"{cwd}\\dist\\EasyMinecraftServer\\1.12.2-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.12.2\\server.properties", f"{cwd}\\dist\\EasyMinecraftServer\\1.12.2"
                                                                           f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.12.2\\eula.txt", f"{cwd}\\dist\\EasyMinecraftServer\\1.12.2-recovery"
                                                                  f"\\eula.txt")
    pass
else:
    pass
if not os.path.exists(f"{cwd}\\dist\\EasyMinecraftServer\\1.16.5-recovery\\"):
    os.mkdir(f"{cwd}\\dist\\EasyMinecraftServer\\1.16.5-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.16.5\\server.properties", f"{cwd}\\dist\\EasyMinecraftServer\\1.16.5"
                                                                           f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.16.5\\eula.txt", f"{cwd}\\dist\\EasyMinecraftServer\\1.16.5-recovery"
                                                                  f"\\eula.txt")
    pass
else:
    pass
if not os.path.exists(f"{cwd}\\dist\\EasyMinecraftServer\\1.17.1-recovery\\"):
    os.mkdir(f"{cwd}\\dist\\EasyMinecraftServer\\1.17.1-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.17.1\\server.properties", f"{cwd}\\dist\\EasyMinecraftServer\\1.17.1"
                                                                           f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.17.1\\eula.txt", f"{cwd}\\dist\\EasyMinecraftServer\\1.17.1-recovery"
                                                                  f"\\eula.txt")
    pass
if not os.path.exists(f"{cwd}\\dist\\EasyMinecraftServer\\1.18.1-recovery\\"):
    os.mkdir(f"{cwd}\\dist\\EasyMinecraftServer\\1.18.1-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.18.1\\server.properties", f"{cwd}\\dist\\EasyMinecraftServer\\1.18.1"
                                                                           f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.18.1\\eula.txt", f"{cwd}\\dist\\EasyMinecraftServer\\1.18.1-recovery"
                                                                  f"\\eula.txt")
    pass
else:
    pass
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
os.mkdir(f"{cwd}\\dist\\EasyMinecraftServer\\ServerLaunchers\\")
os.chdir(f"{cwd}\\ServerLaunchers\\")
os.system("pyinstaller --onefile MinecraftServer-nogui.py")
os.system("pyinstaller --onefile MinecraftServerGUI.pyw")
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServer-nogui.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServer-nogui.exe")
copy(f"{cwd}\\ServerLaunchers\\dist\\MinecraftServerGUI.exe", f"{cwd}\\dist\\EasyMinecraftServer\\MinecraftServerGUI.exe")
print("Done!")
