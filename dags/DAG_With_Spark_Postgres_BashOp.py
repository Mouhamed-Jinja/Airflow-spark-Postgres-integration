from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='DAG_With_Spark_Postgres_BashOp_v1.2',
    default_args=default_args,
    start_date=datetime(2023, 10, 18),
    schedule_interval='0 0 * * *' #every day
) as dag:

    read_csv_load_into_postgres= BashOperator(
        task_id='Extract_Load_v1',
        bash_command='spark-submit --jars /opt/airflow/spark/resources/postgres_jars/postgresql-42.jar /opt/airflow/spark/app/load-postgres.py',
        
    )
    
   
    read_from_postgres= BashOperator(
        task_id='Transform_Save_v1',
        bash_command='spark-submit --jars /opt/airflow/spark/resources/postgres_jars/postgresql-42.jar /opt/airflow/spark/app/read-postgres.py',
    )
    
    read_csv_load_into_postgres >> read_from_postgres