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
os.system("pyinstaller -i mc.ico MinecraftServer.py")
os.system("pyinstaller --onefile MinecraftServerElevator.py")
copytree(f"{cwd}\\ServerFiles-1.8.9\\", f"{cwd}\\dist\\MinecraftServer\\ServerFiles-1.8.9\\")
copytree(f"{cwd}\\ServerFiles-1.12.2\\", f"{cwd}\\dist\\MinecraftServer\\ServerFiles-1.12.2\\")
copytree(f"{cwd}\\ServerFiles-1.16.5\\", f"{cwd}\\dist\\MinecraftServer\\ServerFiles-1.16.5\\")
copytree(f"{cwd}\\ServerFiles-1.17.1\\", f"{cwd}\\dist\\MinecraftServer\\ServerFiles-1.17.1\\")
copytree(f"{cwd}\\ngrok\\", f"{cwd}\\dist\\MinecraftServer\\ngrok\\")
copytree(f"{cwd}\\JDK\\", f"{cwd}\\dist\\MinecraftServer\\JDK\\")
copy(f"{cwd}\\dist\\MinecraftServerElevator.exe", f"{cwd}\\dist\\MinecraftServer\\MinecraftServerElevator.exe")
copy(f"{cwd}\\CHANGELOG.txt", f"{cwd}\\dist\\MinecraftServer\\CHANGELOG.txt")
copy(f"{cwd}\\LICENSE.txt", f"{cwd}\\dist\\MinecraftServer\\LICENSE.txt")
copy(f"{cwd}\\README.md", f"{cwd}\\dist\\MinecraftServer\\README.md")
if not os.path.exists(f"{cwd}\\dist\\MinecraftServer\\1.8.9-recovery\\"):
    os.makedirs(f"{cwd}\\dist\\MinecraftServer\\1.8.9-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.8.9\\server.properties", f"{cwd}\\dist\\MinecraftServer\\1.8.9"
                                                                         f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.8.9\\eula.txt", f"{cwd}\\dist\\MinecraftServer\\1.8.9-recovery\\eula.txt")
    pass
else:
    pass
if not os.path.exists(f"{cwd}\\dist\\MinecraftServer\\1.12.2-recovery\\"):
    os.makedirs(f"{cwd}\\dist\\MinecraftServer\\1.12.2-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.12.2\\server.properties", f"{cwd}\\dist\\MinecraftServer\\1.12.2"
                                                                           f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.12.2\\eula.txt", f"{cwd}\\dist\\MinecraftServer\\1.12.2-recovery"
                                                                  f"\\eula.txt")
    pass
else:
    pass
if not os.path.exists(f"{cwd}\\dist\\MinecraftServer\\1.16.5-recovery\\"):
    os.makedirs(f"{cwd}\\dist\\MinecraftServer\\1.16.5-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.16.5\\server.properties", f"{cwd}\\dist\\MinecraftServer\\1.16.5"
                                                                           f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.16.5\\eula.txt", f"{cwd}\\dist\\MinecraftServer\\1.16.5-recovery"
                                                                  f"\\eula.txt")
    pass
else:
    pass
if not os.path.exists(f"{cwd}\\dist\\MinecraftServer\\1.17.1-recovery\\"):
    os.makedirs(f"{cwd}\\dist\\MinecraftServer\\1.17.1-recovery\\")
    copy(f"{cwd}\\ServerFiles-1.17.1\\server.properties", f"{cwd}\\dist\\MinecraftServer\\1.17.1"
                                                                           f"-recovery\\server.properties")
    copy(f"{cwd}\\ServerFiles-1.17.1\\eula.txt", f"{cwd}\\dist\\MinecraftServer\\1.17.1-recovery"
                                                                  f"\\eula.txt")
    pass
else:
    pass
