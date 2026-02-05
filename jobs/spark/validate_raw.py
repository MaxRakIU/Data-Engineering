"""Validiert Raw-Daten mit Great Expectations und verschiebt Fehler in Quarantaene."""

import io
import json
import os
from datetime import datetime, timezone

import boto3
import pandas as pd
import great_expectations as ge


def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER", "minioadmin"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
        region_name="us-east-1",
    )


def validate_small(df: pd.DataFrame, min_cols: int):
    cols = list(df.columns)
    row_count = int(len(df))
    non_null_counts = {c: int(df[c].notna().sum()) for c in cols}
    ge_df = ge.from_pandas(df)
    results = [
        ge_df.expect_table_row_count_to_be_between(min_value=1),
        ge_df.expect_table_column_count_to_be_between(min_value=min_cols),
    ]
    success = all(r["success"] for r in results) and row_count > 0 and len(cols) >= min_cols
    report = {
        "success": success,
        "row_count": row_count,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "columns": sorted(cols),
        "expectations": [
            {
                "expectation_type": r["expectation_config"]["expectation_type"],
                "success": r["success"],
                "unexpected_count": int(r["result"].get("unexpected_count", 0)),
            }
            for r in results
        ],
        "non_null_counts": non_null_counts,
        "note": "Basis-Validierung",
    }
    return success, report


def validate_large(body, cols: list, chunk_size: int, min_cols: int):
    row_count = 0
    non_null_counts = {c: 0 for c in cols}
    for chunk in pd.read_csv(body, chunksize=chunk_size, on_bad_lines="skip"):
        row_count += len(chunk)
        for c in cols:
            if c in chunk.columns:
                non_null_counts[c] += int(chunk[c].notna().sum())

    success = row_count > 0 and len(cols) >= min_cols
    report = {
        "success": success,
        "row_count": int(row_count),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "columns": sorted(cols),
        "expectations": [],
        "non_null_counts": non_null_counts,
        "note": "Basis-Validierung (Chunked)",
    }
    return success, report


def upload_report(s3, bucket: str, key: str, report: dict) -> None:
    payload = json.dumps(report, indent=2).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=payload, ContentType="application/json")


if __name__ == "__main__":
    bucket_raw = os.getenv("MINIO_BUCKET_RAW", "raw")
    bucket_quarantine = os.getenv("MINIO_BUCKET_QUARANTINE", "quarantine")
    bucket_reports = os.getenv("MINIO_BUCKET_REPORTS", "quality")
    key = os.getenv("RAW_S3_KEY", "tips/tips.csv")
    report_key = f"reports/{key}.json"
    max_mb = int(os.getenv("VALIDATE_MAX_MB", "50"))
    chunk_size = int(os.getenv("VALIDATE_CHUNK_SIZE", "200000"))
    min_cols = int(os.getenv("VALIDATE_MIN_COLUMNS", "2"))

    s3 = s3_client()
    obj = s3.get_object(Bucket=bucket_raw, Key=key)
    content_len = int(obj.get("ContentLength", 0))

    if content_len > max_mb * 1024 * 1024:
        header_line = obj["Body"].readline().decode("utf-8").strip()
        cols = [c.strip() for c in header_line.split(",") if c.strip()]
        obj = s3.get_object(Bucket=bucket_raw, Key=key)
        ok, report = validate_large(obj["Body"], cols, chunk_size, min_cols)
    else:
        df = pd.read_csv(io.BytesIO(obj["Body"].read()), on_bad_lines="skip")
        if df.empty:
            raise SystemExit("Validierung fehlgeschlagen: Datensatz nach Parsing leer.")
        ok, report = validate_small(df, min_cols)
    if not ok:
        report["status"] = "failed"
        # in Quarantaene verschieben
        s3.copy_object(
            Bucket=bucket_quarantine,
            CopySource={"Bucket": bucket_raw, "Key": key},
            Key=key,
        )
        s3.delete_object(Bucket=bucket_raw, Key=key)
        upload_report(s3, bucket_reports, report_key, report)
        raise SystemExit("Validierung fehlgeschlagen. Batch nach Quarantaene verschoben.")

    report["status"] = "success"
    upload_report(s3, bucket_reports, report_key, report)
    print("Validierung erfolgreich")
