from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 15),
}

dag = DAG('spark_with_Bahs_v2', default_args=default_args, schedule_interval=None)

# task_submit_spark_job = BashOperator(
#     task_id='submit_spark_job',
#     bash_command='spark-submit /opt/airflow/spark/names.py',
#     dag=dag,
# )

task_submit_spark_job2 = BashOperator(
    task_id='submit_spark2',
    bash_command='spark-submit /opt/airflow/spark/app/test.py',
    dag=dag,
)
task_submit_spark_job2