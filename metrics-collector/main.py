from influxdb_client import InfluxDBClient, Point
from influxdb_client.rest import ApiException
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time
import requests
import socket

# exporter settings
exporter_url = os.getenv("EXPORTER_URL")

# InfluxDB settings
url = os.getenv("INFLUXDB_URL")
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("INFLUXDB_ORG")
bucket = os.getenv("INFLUXDB_BUCKET")

# Get system hostname
hostname = socket.gethostname()


def connect_to_influxdb(url, token, org, max_retries=5, wait_seconds=10):
    for _ in range(max_retries):
        try:
            client = InfluxDBClient(url=url, token=token, org=org)
            return client
        except (requests.exceptions.ConnectionError, ApiException, requests.exceptions.Timeout) as e:
            print(f"接続エラー: {e}, 再試行します...")
            time.sleep(wait_seconds)
    raise Exception("InfluxDBへの接続に失敗しました。")

def get_temperature_from_reader():
    response = requests.get( exporter_url + "/temperature")
    if response.status_code == 200:
        return response.json()["temperature"]
    else:
        return None

client = connect_to_influxdb(url, token, org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_temp_to_influx(temp):
    point = Point("cpu_temp")\
        .tag("unit", "celsius")\
        .tag("host", hostname)\
        .field("value", temp)
    write_api.write(bucket=bucket, org=org, record=point)


while True:
    temp = get_temperature_from_reader()
    if temp is not None:
        write_temp_to_influx(temp)
    time.sleep(60)