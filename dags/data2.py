from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 15),
    'retries': 3,  # Number of retries for the task
    'retry_delay': timedelta(seconds=30),  # Delay between retries
}

dag = DAG('spark_dag_v9', default_args=default_args, schedule_interval=None)

task_spark_job = SparkSubmitOperator(
    task_id='run_spark_job',
    application='/opt/airflow/spark/names.py',
    name='SparkJob',
    conn_id='spark_default',
    conf={'spark.master': 'spark://spark:7077'},
    dag=dag,
)

task_spark_job