"""
Data Processing microservice that will be responsible 
for consume the data and providing data processing
"""

import json
import logging
import uuid

import uvicorn
from fastapi import FastAPI
from kafka import KafkaConsumer, KafkaProducer
from prometheus_client import start_http_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Data Processing Microservice",
    description="Data Processing Microservice Application",
    version="0.0.1",
)

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"], value_serializer=lambda x: x.encode()
)

consumer = KafkaConsumer(
    "src-data",
    bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda message: json.loads(message.decode("utf-8")),
)


def on_stream(stream) -> None:
    """Function that receives data from producer and sent it to another topic"""
    for msg in stream:
        logger.info(f"Received a message from the producer {msg.value}")
        get_msg_items = msg.value.items()
        for pair_name, pair_value in get_msg_items:
            logger.info(f"Extracted pair: {pair_name}: {pair_value}")
            producer.send(
                "processed-data",
                key=uuid.uuid1().bytes,
                value=json.dumps({pair_name: pair_value}),
            )
            logger.info("Message is sucessfully send to producer")


# Need to make it diffrent way
while True:
    on_stream(consumer)


@app.on_event("startup")
async def on_started() -> None:
    logger.info("Prometheus server started")
    start_http_server(port=7003)
