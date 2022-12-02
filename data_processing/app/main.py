"""
Data Processing microservice that will be responsible 
for consume the data and providing data processing
"""

import logging
import uvicorn

from fastapi import FastAPI
from kafka import KafkaConsumer, KafkaProducer
from pyspark.sql import SparkSession
from prometheus_client import start_http_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Data Processing Microservice",
    description="Data Processing Microservice Application",
    version="0.0.1"
)

# SparkSession init:
spark = SparkSession\
    .builder\
    .appName("Data Processing currency prices stream")\
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Spark ReadStream
read_data = spark.readStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "src-data")\
    .option("startingOffsets", "latest")\
    .load()

read_data_val = read_data.selectExpr("CAST(value AS STRING)", "timestamp")

write_stream_console = read_data_val.writeStream\
    .outputMode("append")\
    .format("console")\
    .option("truncate", "false")\
    .start()\
    .awaitTermination()

@app.on_event("startup")
async def on_started() -> None:
    logger.info("Prometheus server started")
    start_http_server(port=7003)
