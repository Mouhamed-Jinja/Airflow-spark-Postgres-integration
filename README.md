# Spark, Airflow, and Postgres Integration

The simplest way to set up a cluster environment that includes Spark, Airflow, and Postgres. This project demonstrates the integration of Spark, Airflow, and Postgres to create a data processing pipeline.

![architecture](https://github.com/Mouhamed-Jinja/Airflow-spark-integration/assets/132110499/262061d8-cf80-48bf-a66b-64f1039656b0)

## Prerequisites

Before running the pipeline, make sure you have the following components installed:

1. I have used the official Airflow docker-compose file. However, you can remove the services that are not needed and their dependencies. Follow the steps in the [official Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) for more details.

3. You don't need to create a new image to integrate with Spark. It already exists in the Airflow documentation. Here is the [link](https://airflow.apache.org/docs/docker-stack/build.html) to the documentation.


## Installation

1. Clone the repository:
  ```
    https://github.com/Mouhamed-Jinja/Airflow-spark-Postgres-integration.git
  ```

2. Build the expanded airflow image:
  ```
    docker build -t airspark:2.0 .
  ```

3. Run the docker-compose:
  ```
  docker compose up airflow-init
  ```
  ```
    docker compose up -d
  ```

4. If you wanna submit spark job to the cluster using CLI:
  ```
   spark-submit --jars path/to/postgres.jar path/to/spark-job.py
  ```
  - Example:
  ```
   spark-submit --jars /opt/airflow/spark/resources/postgres_jars/postgresql-42.jar /opt/airflow/spark/app/load-postgres.py
  ```

5. Create a Postgres database called `load_movies` or you can create it with any name, but make sure that you have changed the DB name in the spark scripts.


## Usage

- After testing the database connection, you can open the Airflow webserver to run the DAG `DAG_With_Spark_Postgres_BashOp_v1.2`.
- Make sure that you have edited the dag `start_date` and run it.

![Screenshot](https://github.com/Mouhamed-Jinja/Airflow-spark-integration/assets/132110499/cae99bd4-e5b0-4c15-b0aa-a7cd991a58eb)

## DAG Structure

The DAG `DAG_With_Spark_Postgres_BashOp_v1.2` consists of the following tasks:

1. `Extract_v1`: This task extracts data from a CSV file and loads it into Postgres using a BashOperator and the `load-postgres.py` script.

2. `Transform_Load_v1`: This task reads data from Postgres using a BashOperator and the `read-postgres.py` script, and performs any necessary transformations.

The tasks are connected in a linear fashion, where `Extract_v1` is executed first, followed by `Transform_Load_v1`.

## Customization

Feel free to customize the DAG and tasks according to your specific requirements. You can modify the bash commands, add additional tasks, or incorporate other Spark or Postgres functionalities.

- BTW, you can add more spark workers:
  ```
  spark-worker_N:
  image: bitnami/spark:3
  container_name: spark_worker_n
  hostname: spark-worker_n
  networks:
    - spark-net
  environment:
    - SPARK_MODE=worker
    - SPARK_MASTER_URL=spark://spark-service:7077
    - SPARK_WORKER_MEMORY=2g
    - SPARK_WORKER_CORES=2
  volumes:
    - ./spark/app:/opt/airflow/spark/app
    - ./spark/resources:/opt/airflow/spark/resources
    - ./spark/resources/postgres_jars:/opt/bitnami/spark/jars/postgres_jars
  ```

- And if you will use Jupyter Notebook, you can add this service:
  ```
    jupyter-spark:
    image: jupyter/pyspark-notebook:spark-3.1.2 
    networks:
        - spark-net
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work/notebooks/
      - ./spark/resources/data:/home/jovyan/work/data/
      - ./spark/resources/jars:/home/jovyan/work/jars/
  ```

## Acknowledgements

- [Apache Spark](https://spark.apache.org/)
- [Apache Airflow](https://airflow.apache.org/)
- [Postgres](https://www.postgresql.org/)

## Contact

For any questions or inquiries, please contact [Mouhamed-Jinja](https://github.com/Mouhamed-Jinja).
