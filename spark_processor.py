import sys
import os
import ctypes
import shutil 
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from textblob import TextBlob

# CONFIGURATION
TARGET_PYTHON = r"C:\Program Files\Python314\python.exe"


def get_windows_short_path(long_path):
    r"""
    Converts "C:\Program Files\..." to "C:\PROGRA~1\..."
    This prevents Spark from crashing on the space.
    """
    if not os.path.exists(long_path):
        print(f"❌ Error: Could not find Python at {long_path}")
        print("Please check if the path is correct!")
        return long_path
        
    buffer_size = ctypes.windll.kernel32.GetShortPathNameW(long_path, None, 0)
    buffer = ctypes.create_unicode_buffer(buffer_size)
    ctypes.windll.kernel32.GetShortPathNameW(long_path, buffer, buffer_size)
    return buffer.value

# Calculate the safe path
safe_python_path = get_windows_short_path(TARGET_PYTHON)

print(f"🔧 Target Path: {TARGET_PYTHON}")
print(f"🔧 Safe Path:   {safe_python_path}")

# Force Spark to use the Safe Path
os.environ['PYSPARK_PYTHON'] = safe_python_path
os.environ['PYSPARK_DRIVER_PYTHON'] = safe_python_path

# FORCE LOCALHOST NETWORKING ---
os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'

# USE SAFE TEMP DIR ---
safe_tmp_dir = "C:\\hadoop\\tmp"
if not os.path.exists(safe_tmp_dir):
    try:
        os.makedirs(safe_tmp_dir)
    except:
        pass

# GET VERSIONS AUTOMATICALLY
spark_version = pyspark.__version__
scala_version = "2.13" if int(spark_version.split('.')[0]) >= 4 else "2.12"
print(f"🧠 Detected Spark {spark_version} (Scala {scala_version})")

kafka_package = f"org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}"

# INITIALIZE SPARK
spark = SparkSession.builder \
    .appName("SentimentStream") \
    .config("spark.jars.packages", kafka_package) \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .config("spark.local.dir", safe_tmp_dir) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# DEFINE SCHEMA
schema = StructType([
    StructField("review_id", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("product_id", StringType(), True),
    StructField("review_text", StringType(), True),
    StructField("timestamp", StringType(), True)
])

#DEFINE AI FUNCTION
def get_sentiment(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0.0

sentiment_udf = udf(get_sentiment, DoubleType())

#CONNECT TO KAFKA
print(f"⏳ Connecting to Kafka with driver: {kafka_package}...")
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user_reviews") \
    .option("startingOffsets", "latest") \
    .load()

#PROCESS DATA
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

processed_df = parsed_df.withColumn("sentiment_score", sentiment_udf(col("review_text"))) \
    .withColumn("sentiment_label", 
                when(col("sentiment_score") > 0, "Positive")
                .when(col("sentiment_score") < 0, "Negative")
                .otherwise("Neutral"))

#OUTPUT TO CONSOLE
query = processed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()