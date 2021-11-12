import os
from shutil import copytree, copy

cwd = os.getcwd()
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
