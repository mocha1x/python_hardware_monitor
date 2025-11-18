import psutil
import WinTmp
import subprocess
import os
import time

while True:
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"\rCPU Usage: {cpu_usage}%")
    mem = psutil.virtual_memory()
    print(f"\rMemory: {mem}")
    disk_usage = psutil.disk_usage('/')
    print(disk_usage)
    # cpu_temp = WinTmp.CPU_Temp()
    # print(f"CPU Temperature: {cpu_temp} degrees C")
    # gpu_temp = WinTmp.GPU_Temp()
    # print(f"GPU Temperature: {gpu_temp} degrees C")

    # dxdiag_info = subprocess.run(['dxdiag', '/t', 'dxdiag_output.txt'], capture_output=True, text=True)