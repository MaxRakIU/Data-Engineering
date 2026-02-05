#!/bin/sh
set -e

mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

mc mb -p local/"$MINIO_BUCKET_RAW" || true
mc mb -p local/"$MINIO_BUCKET_STAGING" || true
mc mb -p local/"$MINIO_BUCKET_CURATED" || true
mc mb -p local/"$MINIO_BUCKET_QUARANTINE" || true
mc mb -p local/"$MINIO_BUCKET_REPORTS" || true

mc anonymous set download local/"$MINIO_BUCKET_RAW" || true

if [ -n "$MINIO_READONLY_USER" ] && [ -n "$MINIO_READONLY_PASSWORD" ]; then
  cat > /tmp/readonly-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::${MINIO_BUCKET_CURATED}",
        "arn:aws:s3:::${MINIO_BUCKET_REPORTS}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": [
        "arn:aws:s3:::${MINIO_BUCKET_CURATED}/*",
        "arn:aws:s3:::${MINIO_BUCKET_REPORTS}/*"
      ]
    }
  ]
}
EOF

  mc admin policy create local readonly-policy /tmp/readonly-policy.json || true
  mc admin user add local "$MINIO_READONLY_USER" "$MINIO_READONLY_PASSWORD" || true
  mc admin policy attach local readonly-policy --user "$MINIO_READONLY_USER" || true
fi
