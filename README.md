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
source test.env
```
```
docker compose up db -d
```
```
sh -c "cd temperature-exporter && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
```
```
sh -c "cd metrics-collector && uvicorn main:app --reload --host 0.0.0.0 --port 8001"
```