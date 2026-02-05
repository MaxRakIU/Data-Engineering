#!/bin/sh
set -e

python /opt/jobs/spark/extract_raw.py
python /opt/jobs/spark/validate_raw.py
python /opt/jobs/spark/transform_to_staging.py
python /opt/jobs/spark/publish_to_curated.py
