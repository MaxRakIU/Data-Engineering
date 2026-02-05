"""Bereinigt Raw-Daten und schreibt Staging als Parquet nach MinIO (S3)."""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, sha2

RAW_BUCKET = os.getenv("MINIO_BUCKET_RAW", "raw")
STAGING_BUCKET = os.getenv("MINIO_BUCKET_STAGING", "staging")

RAW_KEY = os.getenv("RAW_S3_KEY", "tips/tips.csv")
DATASET_NAME = os.path.splitext(os.path.basename(RAW_KEY))[0]
SENSITIVE_COLUMNS = [
    c.strip()
    for c in os.getenv("SENSITIVE_COLUMNS", "").split(",")
    if c.strip()
]
MASK_STRATEGY = os.getenv("MASK_STRATEGY", "hash").lower()

RAW_PATH = f"s3a://{RAW_BUCKET}/{RAW_KEY}"
STAGING_PATH = f"s3a://{STAGING_BUCKET}/{DATASET_NAME}"


def spark_session() -> SparkSession:
    master_url = os.getenv("SPARK_MASTER_URL", "spark://spark-master:7077")
    return (
        SparkSession.builder
        .appName("transform_raw_to_staging")
        .master(master_url)
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262",
        )
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("MINIO_ENDPOINT", "http://minio:9000"))
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("MINIO_ROOT_USER", "minioadmin"))
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"))
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .getOrCreate()
    )


if __name__ == "__main__":
    spark = spark_session()

    df = (
        spark.read
        .option("header", True)
        .option("mode", "DROPMALFORMED")
        .csv(RAW_PATH)
    )

    # simple cleanup
    df = df.dropna()
    if "timestamp" in df.columns:
        df = df.withColumn("timestamp", col("timestamp").cast("timestamp"))
    if "value" in df.columns:
        df = df.withColumn("value", col("value").cast("double"))
    if "total_bill" in df.columns:
        df = df.withColumn("total_bill", col("total_bill").cast("double"))
    if "tip" in df.columns:
        df = df.withColumn("tip", col("tip").cast("double"))
    if "size" in df.columns:
        df = df.withColumn("size", col("size").cast("int"))

    # Optionales Masking fuer sensitive Spalten (Datenschutz)
    for col_name in SENSITIVE_COLUMNS:
        if col_name not in df.columns:
            continue
        if MASK_STRATEGY == "redact":
            df = df.withColumn(col_name, lit("***MASKIERT***"))
        else:
            df = df.withColumn(col_name, sha2(col(col_name).cast("string"), 256))

    df.write.mode("overwrite").parquet(STAGING_PATH)
    print(f"Staging geschrieben nach {STAGING_PATH}")

    spark.stop()
