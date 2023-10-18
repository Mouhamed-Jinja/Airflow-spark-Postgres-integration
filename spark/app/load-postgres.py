import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime, col, to_timestamp
from pyspark.sql.types import DoubleType

# Create spark session
spark = (SparkSession \
    .builder \
    .config("spark.jars", "/opt/bitnami/spark/jars/postgres_jars/postgresql-42.jar") \
    .getOrCreate()
)
####################################
# Parameters
####################################
movies_file_path ="/opt/airflow/spark/resources/data/movies.csv" 
ratings_file_path ="/opt/airflow/spark/resources/data/ratings.csv" 
postgres_db = "jdbc:postgresql://postgres:5432/load_movies"
postgres_user = "airflow"
postgres_pwd = "airflow"

####################################
# Read CSV Data
####################################
print("######################################")
print("READING CSV FILES")
print("######################################")

df_movies_csv = (
    spark.read.csv(movies_file_path, header=True)
)

df_movies_csv.show(5)


df_ratings_csv = (
    spark.read \
        .csv(ratings_file_path, header=True) \
        .withColumnRenamed("timestamp","timestamp_epoch")
)

df_ratings_csv.show(5)

# Convert epoch to timestamp and rating to DoubleType
df_ratings_csv_fmt = (
    df_ratings_csv \
    .withColumn('rating', col("rating").cast(DoubleType())) \
    .withColumn('timestamp', to_timestamp(from_unixtime(col("timestamp_epoch")))) \
    .drop("timestamp_epoch")
)
df_ratings_csv_fmt.show(5)

####################################
# Load data to Postgres
####################################
print("######################################")
print("LOADING POSTGRES TABLES")
print("######################################")

(
    df_movies_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.movies")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .option("driver", "org.postgresql.Driver")
    .mode("overwrite")
    .save()
)


(
    df_ratings_csv_fmt.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.ratings")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .option("driver", "org.postgresql.Driver")
    .mode("overwrite")
    .save()
)
