import os
import platform
import subprocess

def open_netease_music():
    system = platform.system()
    
    if system == "Windows":
        # Windows 系统：假设网易云音乐安装在默认路径
        netease_path = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
        if os.path.exists(netease_path):
            subprocess.Popen([netease_path])
        else:
            print("未找到网易云音乐安装路径，请检查是否安装或路径是否正确。")
    elif system == "Darwin":
        # macOS 系统：通过命令行打开网易云音乐
        try:
            subprocess.Popen(["open", "-a", "NeteaseMusic"])
        except FileNotFoundError:
            print("未找到网易云音乐应用，请检查是否安装。")
    elif system == "Linux":
        # Linux 系统：假设通过命令行启动
        try:
            subprocess.Popen(["netease-cloud-music"])
        except FileNotFoundError:
            print("未找到网易云音乐应用，请检查是否安装。")
    else:
        print("不支持的操作系统。")

# 调用函数打开网易云音乐
open_netease_music()