from fastapi import FastAPI, Response

import logging
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime
import psutil

logger = logging.getLogger('uvicorn')

app = FastAPI()

def fetch_metrics():
    try:
        temperatures = psutil.sensors_temperatures()
        if not temperatures:
            logger.info("温度情報は利用できません。")
            return None
        else:
            for name, entries in temperatures.items():
                for entry in entries:
                    logger.info(f"{name}: {entry.current}°C")
    except RuntimeError as e:
        logger.error("エラーが発生しました: {e}")
        return None

# CollectorRegistryのインスタンスを作成
registry = CollectorRegistry()

# Gaugeのインスタンスを作成し、registryに登録する
if 'cpu_temperature' not in registry._names_to_collectors:
    CPU_TEMP = Gauge('cpu_temperature', 'Temperature of the CPU', registry=registry)

@app.get("/metrics")
def get_metrics():
    fetch_metrics() 
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)