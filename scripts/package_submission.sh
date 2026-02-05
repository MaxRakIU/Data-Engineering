#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${OUT_DIR:-submission}"
ARCHIVE="${ARCHIVE:-lakehouse-new-submission.tar.gz}"

rm -rf "${OUT_DIR}"
mkdir -p "${OUT_DIR}"

rsync -a \
  --exclude ".git" \
  --exclude "airflow/logs" \
  --exclude "airflow/airflow.db" \
  --exclude "backups" \
  --exclude "data/raw" \
  --exclude "data/staging" \
  --exclude "data/curated" \
  --exclude "data/quarantine" \
  --exclude "data/source/*.csv" \
  --exclude "trino/data" \
  ./ "${OUT_DIR}/"

tar -czf "${ARCHIVE}" "${OUT_DIR}"
echo "Archiv erstellt: ${ARCHIVE}"
