#!/usr/bin/env bash
set -euo pipefail

RAW_S3_KEY="${RAW_S3_KEY:-big_ok.csv}"

echo "Smoke-Check laeuft..."
docker compose exec -T airflow env RAW_S3_KEY="${RAW_S3_KEY}" /opt/scripts/smoke_check.sh

echo "Trino-Abfrage laeuft..."
docker compose exec -T trino /usr/bin/trino \
  --server http://localhost:8080 \
  --catalog iceberg \
  --schema curated \
  --execute "SELECT count(*) AS cnt FROM ${RAW_S3_KEY%%.*}"

echo "Abgabe-Checks bestanden"
