from fastapi import FastAPI
import subprocess

app = FastAPI()

def get_cpu_temp():
    try:
        result = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'], capture_output=True, text=True, check=True)
        temp_str = result.stdout.strip()
        return float(temp_str) / 1000.0
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
