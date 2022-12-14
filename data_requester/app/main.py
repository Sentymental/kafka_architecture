"""
Main file for data requester
"""

import json
import logging
import uuid
import data_provider

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from kafka import KafkaProducer
from prometheus_client import start_http_server

# Logging:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s",
)
logger = logging.getLogger(__name__)

# KafkaProducer:
kafka_producer_obj = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092", value_serializer=lambda x: x.encode("utf-8")
)

# Faust Application init:
app = FastAPI(
    title="Data Producer application",
    description="Data producer",
    version="0.0.1"
)

@app.on_event("startup")
@repeat_every(seconds=1, raise_exceptions=True)
async def request_data() -> None:
    """Function that generates new pairs of currency"""
    logger.info("Preparing environment to start")
    message = data_provider.DataProvider(base_url="http://localhost:8002/pairs")
    pairs = await message.get_pairs()
    logger.info(f"Reveiced new pairs: {pairs}")
    logger.info(f"Type of the output: {type(pairs)}")
    if pairs:
        logger.info(f"Sending pair: {pairs}")
        kafka_producer_obj.send("src-data", key=uuid.uuid1().bytes, value=json.dumps(pairs))
    else:
        logger.info("There is no valid pairs or is the problem with producer")


@app.on_event("startup")
async def on_started() -> None:
    """On Startup run prometheus"""
    logger.info("Starting prometheus server")
    start_http_server(port=7003)
