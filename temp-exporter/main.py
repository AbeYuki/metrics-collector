from fastapi import FastAPI, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil
import asyncio

app = FastAPI()

def fetch_metrics():
    # CPUの温度を返す関数
    CPU_TEMP = Gauge('cpu_temperature', 'Temperature of the CPU')
    CPU_TEMP.set(psutil.sensors_temperatures()['cpu_thermal'][0].current)
    return {"message": "Metrics updated"}

@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.on_event("startup")
async def start_periodic_metrics_update():
    asyncio.create_task(periodic_metrics_update())

async def periodic_metrics_update():
    while True:
        fetch_metrics()
        await asyncio.sleep(60)