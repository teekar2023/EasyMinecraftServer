import os
from shutil import copytree

cwd = os.getcwd()
os.system("pyinstaller MinecraftServer.py")
copytree(f"{cwd}\\ServerFiles\\", f"{cwd}\\dist\\MinecraftServer\\ServerFiles\\")
