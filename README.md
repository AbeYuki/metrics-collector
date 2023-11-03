# metrics-collector

## compose 

```
docker compose build --no-cache
```

```
docker compose up -d
```

## venv

```
python -m venv venv
```
```
pip install -r metrics-collector/requirements.txt
```
```
pip install -r temperature-exporter/requirements.txt
```
```
source metrics-collector/.env
```
```
uvicorn metrics-collector.main:app --reload --host 0.0.0.0 --port 8001
```
```
uvicorn temperature-exporter.main:app --reload --host 0.0.0.0 --port 8001
```