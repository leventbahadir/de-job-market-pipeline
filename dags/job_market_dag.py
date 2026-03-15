from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow')

from src.extract.adzuna import fetch_jobs
from src.load.raw_loader import load_raw
from src.transform.parse_skills import parse_skills

default_args = {
    'owner': 'levent',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='job_market_pipeline',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract = PythonOperator(
        task_id='extract_jobs',
        python_callable=lambda: fetch_jobs()
    )

    load = PythonOperator(
        task_id='load_raw',
        python_callable=lambda: load_raw(fetch_jobs())
    )

    transform = PythonOperator(
        task_id='transform_skills',
        python_callable=parse_skills
    )

    extract >> load >> transform
