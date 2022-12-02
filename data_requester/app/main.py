"""
Main file for data requester
"""

import json
import logging
import uuid
import data_provider

from fastapi import FastAPI
from kafka import KafkaProducer
from prometheus_client import start_http_server


# Producer variables
SERIVCE_NAME = "data-requester"
BROKER_HOST = "127.0.0.1:9093"
KAFKA_TOPIC = "src-data"

# Logging:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s",
)
logger = logging.getLoger(__name__)

# KafkaProducer:
kafka_producer_obj = KafkaProducer(
    bootstrap_servers="127.0.0.1:9093", value_serializer=lambda x: x.encode("utf-8")
)

app = FastAPI(
    title="Prometheus Server",
    description="Prometheus Server for checking metrics",
    version="0.0.1",
)

@app.get("/get_currency_pairs", tags=["pairs", "currency pairs", "kafka producer"])
async def request_data() -> None:
    """Function that generates new pairs of currency"""
    logger.info("Preparing environment to start")
    message = data_provider.DataProvider(base_url="http://localhost:8002/pairs")
    pairs = await message.get_pairs()
    logger.info(f"Reveiced new pairs: {pairs}")
    if pairs:
        logger.info(f"Sending pair: {pair}")
        kafka_producer_obj.send(KAFKA_TOPIC, pairs)
    else:
        logger.info("There is no valid pairs or " "is the problem with producer")


if __name__ == "__main__":
    logger.info("Starting prometheus server")
    start_http_server(port=7003)
