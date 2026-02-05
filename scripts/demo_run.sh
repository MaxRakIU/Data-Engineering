#!/usr/bin/env bash
set -euo pipefail

RAW_S3_KEY="${RAW_S3_KEY:-big_ok.csv}"
LOCAL_FILE_PATH="${LOCAL_FILE_PATH:-/opt/data/source/big_ok.csv}"
SKIP_IF_EXISTS="${SKIP_IF_EXISTS:-false}"

docker compose up -d minio minio-mc airflow trino

docker compose exec -T airflow \
  airflow dags trigger lakehouse_batch_pipeline \
  -c "{\"RAW_S3_KEY\":\"${RAW_S3_KEY}\",\"LOCAL_FILE_PATH\":\"${LOCAL_FILE_PATH}\",\"SKIP_IF_EXISTS\":\"${SKIP_IF_EXISTS}\"}"

echo "DAG gestartet mit RAW_S3_KEY=${RAW_S3_KEY}"
echo "Fortschritt in der Airflow-UI: http://localhost:8082"
