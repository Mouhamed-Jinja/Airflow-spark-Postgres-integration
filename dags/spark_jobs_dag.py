from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType

# Create a SparkSession
spark = SparkSession.builder \
    .appName("SparkETL") \
    .master("spark://localhost:18080") \
    .config("spark.ui.port", "18080") \
    .getOrCreate()

# Generate random data
data = spark.range(1000).select(col("id").cast(IntegerType()).alias("value"))

# Apply transformations
transformed_data = data.select(col("value"), (col("value") * 2).alias("doubled_value"))

# Save result as a CSV file in the build context
output_path = "outputs/output.csv"  # Assuming "outputs" is a directory in the build context
transformed_data.write.csv(output_path, header=True, mode="overwrite")

# Stop the SparkSession
spark.stop()
