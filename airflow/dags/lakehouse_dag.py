from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule

DEFAULT_ARGS = {
    "owner": "data-eng",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="lakehouse_batch_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["lakehouse"],
) as dag:
    extract = BashOperator(
        task_id="extract",
        bash_command=(
            "RAW_S3_KEY='{{ dag_run.conf.get(\"RAW_S3_KEY\", \"tips/tips.csv\") }}' "
            "LOCAL_FILE_PATH='{{ dag_run.conf.get(\"LOCAL_FILE_PATH\", \"\") }}' "
            "SKIP_IF_EXISTS='{{ dag_run.conf.get(\"SKIP_IF_EXISTS\", \"false\") }}' "
            "python /opt/jobs/spark/extract_raw.py"
        ),
    )

    validate = BashOperator(
        task_id="validate",
        bash_command=(
            "RAW_S3_KEY='{{ dag_run.conf.get(\"RAW_S3_KEY\", \"tips/tips.csv\") }}' "
            "python /opt/jobs/spark/validate_raw.py"
        ),
    )

    quarantine_notice = BashOperator(
        task_id="quarantine_notice",
        bash_command=(
            "RAW_S3_KEY='{{ dag_run.conf.get(\"RAW_S3_KEY\", \"tips/tips.csv\") }}' "
            "echo \"Validierung fehlgeschlagen; Batch in Quarantaene verschoben. "
            "Report: s3a://quality/reports/${RAW_S3_KEY}.json\""
        ),
        trigger_rule=TriggerRule.ONE_FAILED,
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=(
            "RAW_S3_KEY='{{ dag_run.conf.get(\"RAW_S3_KEY\", \"tips/tips.csv\") }}' "
            "SPARK_MASTER_URL='local[*]' "
            "python /opt/jobs/spark/transform_to_staging.py"
        ),
    )

    publish = BashOperator(
        task_id="publish",
        bash_command=(
            "RAW_S3_KEY='{{ dag_run.conf.get(\"RAW_S3_KEY\", \"tips/tips.csv\") }}' "
            "SPARK_MASTER_URL='local[*]' "
            "python /opt/jobs/spark/publish_to_curated.py"
        ),
    )

    extract >> validate >> transform >> publish
    validate >> quarantine_notice
