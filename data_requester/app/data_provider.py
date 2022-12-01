"""
Main file for data requester
"""

import uuid, logging, faust, json
from prometheus_client import start_http_server
from kafka import KafkaProducer
from fastapi import FastAPI

# Producer variables
SERIVCE_NAME = "data-requester"
BROKER_HOST = "127.0.0.1:9093"
KAFKA_TOPIC = "src-data"

# Logging:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s"
)
logger = logging.getLoger(__name__)

# KafkaProducer:
kafka_producer_obj = KafkaProducer(
    bootstrap_servers="127.0.0.1:9093",
    value_serializer=lambda x: x.encode("utf-8")
)

app = FastAPI(
    title="Prometheus Server",
    description="Prometheus Server for checking metrics",
    version="0.0.1"
)

async def request_data() -> None:
    ...

if __name__ == "__main__":
    logger.info("Starting prometheus server")
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)
