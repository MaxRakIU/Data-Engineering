from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

DATA_DIR = "/opt/airflow/data"

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="batch_lakehouse_daily",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    description="Demo-Flow: extract -> validate -> transform -> publish",
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command=(
            "python /opt/airflow/jobs/ingest/ingest.py "
        "--src /opt/airflow/data/source/big.csv "     # <— WICHTIG: absolute Quelle
        "--out /opt/airflow/data/raw/{{ ds }}/data.csv"
        ),
    )

    validate = BashOperator(
        task_id="validate",
        bash_command=(
            "python /opt/airflow/jobs/validate/run_checks.py "
            f"--inp {DATA_DIR}/raw/{{{{ ds }}}}/data.csv "
            f"--quarantine {DATA_DIR}/quarantine/{{{{ ds }}}}/"
        ),
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=(
            "python /opt/airflow/jobs/transform/spark_job.py "
            f"--inp {DATA_DIR}/raw/{{{{ ds }}}}/data.csv "
            f"--out {DATA_DIR}/staging/{{{{ ds }}}}/agg.csv"
        ),
    )

    publish = BashOperator(
        task_id="publish",
        bash_command=(
            "mkdir -p {data}/curated/{{{{ ds }}}} && "
            "cp {data}/staging/{{{{ ds }}}}/agg.csv {data}/curated/{{{{ ds }}}}/facts.csv"
        ).format(data=DATA_DIR),
    )

    extract >> validate >> transform >> publish
