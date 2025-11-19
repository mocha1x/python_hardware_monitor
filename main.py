import psutil
import subprocess
import platform
import time
import sys
import os
import datetime

# Start log
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H.%M.%S")
filename = f"log-{timestamp}.txt"
timestamp_hr = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-4]
timestamp_d = datetime.datetime.now().strftime("%Y-%m-%d")

with open(filename, "w") as f:
    f.write(f"({timestamp_hr}) Log started at {timestamp_hr} on {timestamp_d}.\n")

def log(message):
    timestamp_hr = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-4]
    with open(filename, "a") as f:
        f.write(f"({timestamp_hr}) {message}\n")
        time.sleep(0.5)

# OS info
os.system("cls" if os.name == "nt" else "clear")

if platform.system() == "Windows":
    log(f"Microsoft {platform.system()} operating system detected.")
elif platform.system() == "Linux":
    log(f"{platform.system()} operating system detected.")
elif platform.system() == "Darwin":
    log(f"{platform.system()} macOS operating system detected.")
else:
    log(f"No supported operating system detected.")
    sys.exit(1)

# CPU info
def get_cpu_name():
    if platform.system() == "Windows":
        try:
            # Use regedit to detect CPU
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            return cpu_name
        except Exception:
            return "Unknown CPU"
    
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except:
            return "Unknown CPU"
        
    if platform.system() == "Darwin":
        try:
            result = subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                text=True
            )
            return result.strip()
        except:
            return "Unknown CPU"
    return "Unkown CPU (Unsupported OS)"

cpu_name = get_cpu_name()
log(f"CPU detected as {cpu_name}")

# GPU info
def get_gpu_usage():
    result = subprocess.run(
        ["nvidia-smi", # only works with NVIDIA GPUs
         "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
         "--format=csv,noheader,nounits"],
        capture_output=True, text=True
    )
    line = result.stdout.strip()
    if not line:
        return None
    gpus = []
    for l in line.split("\n"):
        parts = [x.strip() for x in l.split(",")]
        name = parts[0]  # keep as string
        util = int(parts[1])
        mem_used_gb = int(parts[2]) / 1024
        mem_total_gb = int(parts[3]) / 1024
        temp = int(parts[4])
        gpus.append((name, util, mem_used_gb, mem_total_gb, temp))
    return gpus

try:
    prev_lines = 0
    gpus = get_gpu_usage()
    if gpus:
        for i, (name, _, _, _, _,) in enumerate(gpus):
            log(f"GPU {i} detected as: {name}")
    else:
        log("GPU information not available.")

    while True:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        gpus = get_gpu_usage()
        if gpus:
            for i, (name, util, mem_used_gb, mem_total_gb, temp) in enumerate(gpus):
                lines = [
                    f"GPU {i}: {util:7d}% {temp:4d}°C",
                    f"CPU: {cpu:9.1f}%",
                    f"VRAM: {mem_used_gb:6.2f} GB / {mem_total_gb} GB",
                    f"RAM: {ram.used / (1024**3):7.2f} GB / {ram.total / (1024**3):.2f} GB",
                ]
        else:
            lines.append("GPU info not available")
        
        # Continuously logs
        log(f"GPU {i}: {util}%, {temp}°C|CPU: {cpu:.0f}%|VRAM: {mem_used_gb:.2f} GB/{mem_total_gb:.2f} GB|RAM: {ram.used / (1024**3):.2f} GB/{ram.total / (1024**3):.2f} GB")

        # Overwrite previous lines
        if prev_lines:
            sys.stdout.write("\033[F" * prev_lines)

        for line in lines:
            print(line)

        prev_lines = len(lines)
        time.sleep(1)

# End program
except KeyboardInterrupt:
    os.system("cls" if os.name == "nt" else "clear")
    print("Exiting...")
    log(f"Log finished at {timestamp_hr} on {timestamp_d}.")
