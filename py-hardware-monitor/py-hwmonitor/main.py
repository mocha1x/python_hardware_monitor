import psutil
import subprocess
import platform
import time
import sys
import os
import datetime

# Warning: The GPU monitoring only works with NVIDIA GPUs

start_time = time.time()

# Create logs folder
root = os.path.dirname(os.path.dirname(__file__))
logs = os.path.join(root, "logs")
os.makedirs(logs, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d-%H.%M.%S")
filename = os.path.join(logs, f"log-{timestamp}.txt")

# Start log
timestamp_hr = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-4]
timestamp_d = datetime.datetime.now().strftime("%Y-%m-%d")
with open(filename, "w") as f:
    path = os.path.abspath(filename)
    f.write(f"File created at {path}\n")
    f.write(f"Log started at {timestamp_hr} on {timestamp_d}.\n")

# Append to file
def log(message):
    timestamp_hr = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-4]
    with open(filename, "a") as f:
        f.write(f"({timestamp_hr}) {message}\n")

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

# GPU info
def get_gpu_usage():
    # DEBUG
    try:
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
            name = parts[0]
            util = int(parts[1])
            mem_used_gb = int(parts[2]) / 1024
            mem_total_gb = int(parts[3]) / 1024
            temp = int(parts[4])
            gpus.append((name, util, mem_used_gb, mem_total_gb, temp))
        return gpus
    
    except:
        gpu = False
        print("GPU incompatible."
        "\nContinuing without GPU monitoring.", end="", flush=True)
        for _ in range(6):
            time.sleep(1)
            print(".", end="", flush=True)
        os.system("cls" if os.name == "nt" else "clear")
        return gpu

def main():
    os.system("cls" if os.name == "nt" else "clear")

    print("Press ^C at any time to end the program.", end="", flush=True)
    for _ in range(6):
        time.sleep(1)
        print(".", end="", flush=True)
    print()
    os.system("cls" if os.name == "nt" else "clear")
    
    # OS info
    if platform.system() == "Windows":
        log(f"Microsoft {platform.system()} operating system detected.")
    elif platform.system() == "Linux":
        log(f"{platform.system()} operating system detected.")
    elif platform.system() == "Darwin":
        log(f"{platform.system()} macOS operating system detected.")
    else:
        log(f"No supported operating system detected.")
        sys.exit(1)

    cpu_name = get_cpu_name()
    log(f"CPU detected as {cpu_name}")

    gpus = get_gpu_usage()
    if gpus is None:
            log("No NVIDIA GPU detected or drivers not installed.")
            gpus = []
    if gpus:
        for i, (name, _, _, _, _) in enumerate(gpus):
            log(f"GPU {i} detected as: {name}")
    else:
        log("GPU information not available.")

    prev_lines = 0

    while True:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()

        # if gpus != False:
        #     gpus = get_gpu_usage()
        # else:
        #     pass
    
        if gpus != False:
            gpus = get_gpu_usage()
            for i, (name, util, mem_used_gb, mem_total_gb, temp) in enumerate(gpus):
                lines = [
                    f"GPU {i}: {util:7d}% {temp:4d}°C",
                    f"CPU: {cpu:9.1f}%",
                    f"VRAM: {mem_used_gb:6.2f} GB / {mem_total_gb} GB",
                    f"RAM: {ram.used / (1024**3):7.2f} GB / {ram.total / (1024**3):.2f} GB",
                ]
        else:
            lines = [
                f"CPU: {cpu:9.1f}%",
                f"RAM: {ram.used / (1024**3):7.2f} GB / {ram.total / (1024**3):.2f} GB",
            ]
        
        # Continuous logging
        if gpus != False:
            log(f"GPU {i}: {util}%, {temp}°C|CPU: {cpu:.0f}%|VRAM: {mem_used_gb:.2f} GB/{mem_total_gb:.2f} GB|RAM: {ram.used / (1024**3):.2f} GB/{ram.total / (1024**3):.2f} GB")
        else:
            log(f"CPU: {cpu:.0f}%|RAM: {ram.used / (1024**3):.2f} GB/{ram.total / (1024**3):.2f} GB")

        # Overwrite previous lines
        if prev_lines:
            sys.stdout.write("\033[F" * prev_lines)
        for line in lines:
            print(line)

        prev_lines = len(lines)
        time.sleep(1)

# End program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        print("Exiting...")
        end_time = time.time()
        total_seconds = int(end_time - start_time)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        runtime_parts = []
        if hours > 0:
            runtime_parts.append(f"{hours} hours")
        if minutes > 0:
            runtime_parts.append(f"{minutes} minutes")
        runtime_parts.append(f"{seconds} seconds")
        runtime_total = " ".join(runtime_parts)

        final_timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-4]
        log(
            f"Program exited by user after {runtime_total}.\n"
            f"Log finished at {final_timestamp} on {timestamp_d}.\n"
            f"File saved to {path}"
        )
        # Print average CPU, average ram etc after however long program ran
        # Print file saved to location