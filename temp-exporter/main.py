from fastapi import FastAPI, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime
import psutil,logging

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
                    # センサー名と温度をメトリクスに追加
                    CPU_TEMP.labels(sensor=name).set(entry.current)
                    logger.info(f"{name}: {entry.current}°C")
    except RuntimeError as e:
        logger.error(f"エラーが発生しました: {e}")
        return None

# CollectorRegistryのインスタンスを作成
registry = CollectorRegistry()

# Gaugeのインスタンスを作成し、registryに登録する
if 'cpu_temperature' not in registry._names_to_collectors:
    # センサー名でラベルを追加
    CPU_TEMP = Gauge('cpu_temperature', 'Temperature of the CPU', ['sensor'], registry=registry)

@app.get("/metrics")
def get_metrics():
    fetch_metrics() 
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)