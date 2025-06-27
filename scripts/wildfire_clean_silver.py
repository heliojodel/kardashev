# src/databricks_jobs/silver_cleaning_job.py
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, expr

def clean_data(df):
    df = df.withColumnRenamed("NWCG_CAUSE_CLASSIFICATION", "CAUSE_CLASS") \
           .withColumnRenamed("NWCG_GENERAL_CAUSE", "CAUSE") \
           .withColumnRenamed("NWCG_CAUSE_AGE_CATEGORY", "CAUSE_AGE")

    df = df.withColumn("DISCOVERY_DATETIME", to_timestamp(col("DISCOVERY_DATETIME"))) \
           .withColumn("CONT_DATETIME", to_timestamp(col("CONT_DATETIME")))
        
    df = df.withColumn("FIRE_DURATION_MINUTES", 
                       (col("CONT_DATETIME").cast("long") - col("DISCOVERY_DATETIME").cast("long")) / 60)
    
    return df.drop_duplicates()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path", required=True)
    args = parser.parse_args()

    spark = SparkSession.builder.appName("BronzeToSilver").getOrCreate()

    raw_df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(args.input_path)
    cleaned_df = clean_data(raw_df)
    cleaned_df.write.mode("overwrite").parquet(args.output_path)
    
    spark.stop()
