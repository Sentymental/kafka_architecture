from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, FloatType
import pyspark.sql.functions as func

spark = (
    SparkSession
    .builder
    .appName("Data aggregator")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

read_data = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "processed-data")
    .option("startingOffsets", "latest")
    .load()
)

values = read_data.selectExpr("CAST(value as STRING)", "timestamp")

values.printSchema()

sample_schema = StructType([
    StructField("USDPLN", StringType(), False),
    StructField("EURPLN", StringType(), False)
])

info_dataframe = values.select(
    func.from_json(func.col("value"), sample_schema).alias("sample"), "timestamp"
)

info_df_fin = info_dataframe.select("sample.*", "timestamp")

info_dataframe.printSchema()

df = info_dataframe.select("sample.USDPLN", "sample.EURPLN")

write_data = (
    df
    .writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", "false")
    .start()
    .awaitTermination()
)