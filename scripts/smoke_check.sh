#!/bin/sh
set -e

python3 - <<'PY'
import os
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
    aws_access_key_id=os.getenv("MINIO_ROOT_USER", "minioadmin"),
    aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
    region_name="us-east-1",
)

report_bucket = os.getenv("MINIO_BUCKET_REPORTS", "quality")
raw_key = os.getenv("RAW_S3_KEY", "tips/tips.csv")
dataset_name = os.path.splitext(os.path.basename(raw_key))[0]

checks = {
    "raw": raw_key,
    "staging": dataset_name + "/",
    report_bucket: f"reports/{raw_key}.json",
}

curated_prefixes = [
    "warehouse/curated/" + dataset_name + "/metadata/",
    "warehouse/curated.db/" + dataset_name + "/metadata/",
]

for bucket, prefix in checks.items():
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if "Contents" not in resp:
        raise SystemExit(f"Missing {bucket}/{prefix}")
    print(f"OK {bucket}/{prefix}")

curated_ok = False
for prefix in curated_prefixes:
    resp = s3.list_objects_v2(Bucket="curated", Prefix=prefix)
    if "Contents" in resp:
        print(f"OK curated/{prefix}")
        curated_ok = True
        break

if not curated_ok:
    raise SystemExit("Curated-Metadaten fuer das Dataset fehlen")

print("Smoke-Check bestanden")
PY
