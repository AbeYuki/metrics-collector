from influxdb_client import InfluxDBClient, Point
from influxdb_client.rest import ApiException
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import os
import time
import requests
import socket
import yaml

# config 
config_path = os.getenv("CONFIG_PATH")

# exporter settings
exporter_url = os.getenv("EXPORTER_URL")

# InfluxDB settings
url = os.getenv("INFLUXDB_URL")
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("INFLUXDB_ORG")
bucket = os.getenv("INFLUXDB_BUCKET")

# Get system hostname
hostname = socket.gethostname()

config_file = config_path

def load_hosts_from_file(config_file):
    try:
        with open(config_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        return data_loaded.get('hosts', [])
    except FileNotFoundError:
        print("{current_time} [error] ファイルが見つかりません。")
    except PermissionError:
        print("{current_time} [error] このファイルを開く権限がありません。")
    except OSError as e:
        # その他のOSエラーをキャッチ
        print(f"{current_time} [error] エラーが発生しました: {e}")
    except ValueError:
        # floatへの変換に失敗した場合
        print("{current_time} [error] 数値変換エラー。ファイルの内容が不正です。")

hosts = load_hosts_from_file(config_file)

def connect_to_influxdb(url, token, org, max_retries=5, wait_seconds=10):
    for _ in range(max_retries):
        try:
            client = InfluxDBClient(url=url, token=token, org=org)
            return client
        except (requests.exceptions.ConnectionError, ApiException, requests.exceptions.Timeout) as e:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} [error] 接続エラー: {e}, 再試行します...")
            time.sleep(wait_seconds)
    raise Exception(f"{current_time} [error] InfluxDBへの接続に失敗しました。")

def get_temperature_from_host(host):
    try:
        # URLを構築する際には、'http://'を明示的に追加する
        url = f"http://{host}:8000/temperature"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPエラーがあればここで例外を投げる
        return response.json()["temperature"]
    except requests.exceptions.RequestException as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} [error] ホスト{host}からのデータ取得エラー: {e}")
        return None

client = connect_to_influxdb(url, token, org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_temp_to_influx(temp, host, write_api, bucket, org):
    point = Point("cpu_temp")\
        .tag("unit", "celsius")\
        .tag("host", host)\
        .field("value", temp)
    write_api.write(bucket=bucket, org=org, record=point)

while True:
    for host in hosts:
        temp = get_temperature_from_host(host)  # ホスト名のみを渡す
        if temp is not None:
            write_temp_to_influx(temp, host, write_api, bucket, org)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} [info] write success {host}:{temp}")
    time.sleep(60)  # 各ホストからの読み取り間隔