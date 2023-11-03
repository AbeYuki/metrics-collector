from fastapi import FastAPI
from app import get_cpu_temp

app = FastAPI()

@app.get("/temperature")
def read_temperature():
    temp = get_cpu_temp()
    return {"temperature": temp}