"""Laedt ein offenes Dataset und schreibt CSV als Raw nach MinIO."""

import io
import os

import boto3
import requests

DEFAULT_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"


def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER", "minioadmin"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
        region_name="us-east-1",
    )


if __name__ == "__main__":
    url = os.getenv("DATASET_URL", DEFAULT_URL)
    bucket = os.getenv("MINIO_BUCKET_RAW", "raw")
    key = os.getenv("RAW_S3_KEY", "tips/tips.csv")
    local_path = os.getenv("LOCAL_FILE_PATH", "").strip()
    skip_if_exists = os.getenv("SKIP_IF_EXISTS", "false").lower() in {"1", "true", "yes"}

    s3 = s3_client()
    if skip_if_exists:
        try:
            s3.head_object(Bucket=bucket, Key=key)
            print(f"Raw existiert bereits: s3a://{bucket}/{key}")
            raise SystemExit(0)
        except Exception:
            pass

    if local_path:
        with open(local_path, "rb") as f:
            s3.upload_fileobj(f, bucket, key)
        print(f"Lokale Datei hochgeladen nach s3a://{bucket}/{key}")
    else:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        s3.upload_fileobj(io.BytesIO(resp.content), bucket, key)
        print(f"Heruntergeladen und nach s3a://{bucket}/{key} hochgeladen")
