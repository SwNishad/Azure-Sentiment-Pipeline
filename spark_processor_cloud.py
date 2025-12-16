%pip install textblob
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from textblob import TextBlob

# CONFIGURATION --
connectionString = "Endpoint=sb://sentimentprojectrg.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YOUR_KEY_HERE"


eh_sasl = f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{connectionString}";'

#  DEFINE THE AI
def get_sentiment(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0.0

sentiment_udf = F.udf(get_sentiment, DoubleType())

# DEFINE DATA STRUCTURE ---
schema = StructType(
    StructField("review_id", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("product_id", StringType(), True),
    StructField("review_text", StringType(), True),
    StructField("timestamp", StringType(), True)
])

#  READ STREAM ---
print("⏳ Connecting to Azure Event Hubs...")
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "sentimentprojectrg.servicebus.windows.net:9093") \
    .option("subscribe", "user_reviews") \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.security.protocol", "SASL_SSL") \
    .option("kafka.sasl.jaas.config", eh_sasl) \
    .option("startingOffsets", "latest") \
    .load()

# PROCESS & APPLY AI 
parsed_df = df.select(F.from_json(F.col("value").cast("string"), schema).alias("data")).select("data.*")

processed_df = parsed_df.withColumn("sentiment_score", sentiment_udf(F.col("review_text"))) \
    .withColumn("sentiment_label", 
                F.when(F.col("sentiment_score") > 0, "Positive")
                .when(F.col("sentiment_score") < 0, "Negative")
                .otherwise("Neutral"))

# SAVE TO DELTA TABLE (The Bridge to Power BI) 

query = processed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/checkpoints/sentiment_v1") \
    .table("sentiment_live_data")