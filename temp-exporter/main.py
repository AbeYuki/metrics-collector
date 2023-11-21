from fastapi import FastAPI, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil
import asyncio

app = FastAPI()

CPU_TEMP = Gauge('cpu_temperature', 'Temperature of the CPU')

def fetch_metrics():
    # CPUの温度を返す関数
    CPU_TEMP.set(psutil.sensors_temperatures()['cpu_thermal'][0].current)
    return {"message": "Metrics updated"}

@app.get("/metrics")
def get_metrics():
    fetch_metrics() 
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
