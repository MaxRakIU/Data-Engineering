"""Publiziert Staging-Daten als Iceberg Curated-Tabelle."""

import os
from pyspark.sql import SparkSession

STAGING_BUCKET = os.getenv("MINIO_BUCKET_STAGING", "staging")
CURATED_BUCKET = os.getenv("MINIO_BUCKET_CURATED", "curated")

RAW_KEY = os.getenv("RAW_S3_KEY", "tips/tips.csv")
DATASET_NAME = os.path.splitext(os.path.basename(RAW_KEY))[0]

STAGING_PATH = f"s3a://{STAGING_BUCKET}/{DATASET_NAME}"


def spark_session() -> SparkSession:
    master_url = os.getenv("SPARK_MASTER_URL", "spark://spark-master:7077")
    return (
        SparkSession.builder
        .appName("publish_staging_to_curated")
        .master(master_url)
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2",
        )
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.lakehouse", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.lakehouse.type", "hive")
        .config("spark.sql.catalog.lakehouse.uri", "thrift://hive-metastore:9083")
        .config("spark.sql.catalog.lakehouse.warehouse", f"s3a://{CURATED_BUCKET}/warehouse")
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

    df = spark.read.parquet(STAGING_PATH)

    spark.sql("CREATE NAMESPACE IF NOT EXISTS lakehouse.curated")
    (
        df.writeTo(f"lakehouse.curated.{DATASET_NAME}")
        .using("iceberg")
        .tableProperty("format-version", "2")
        .createOrReplace()
    )

    print(f"Curated.{DATASET_NAME} in Iceberg publiziert")
    spark.stop()
