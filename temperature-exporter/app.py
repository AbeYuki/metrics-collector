from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

def get_cpu_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_string = f.readline()
            cpu_temp = float(temp_string) / 1000.0
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} [info] CPU Temperature: {cpu_temp} C")
        return cpu_temp
    except FileNotFoundError:
        print("ファイルが見つかりません。")
    except PermissionError:
        print("このファイルを開く権限がありません。")
    except OSError as e:
        # その他のOSエラーをキャッチ
        print(f"エラーが発生しました: {e}")
    except ValueError:
        # floatへの変換に失敗した場合
        print("数値変換エラー。ファイルの内容が不正です。")