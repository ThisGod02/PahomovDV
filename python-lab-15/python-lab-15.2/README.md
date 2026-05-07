# Lab 15.2 - Kafka Demo

This folder contains two ways to demonstrate the Kafka lab:

- real Kafka via `docker-compose.yml`
- local mock transport via `demo_runner.py`

Quick local demo:

```bash
pip install -r requirements.txt
python demo_runner.py
```

Real Kafka path:

```bash
docker compose up -d
python producer.py --mode kafka --count 10
python consumer.py --mode kafka --max-messages 10
```
