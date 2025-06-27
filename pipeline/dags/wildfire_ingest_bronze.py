from airflow import DAG
from airflow.providers.amazon.aws.transfers.http_to_s3 import HttpToS3Operator
from datetime import datetime

with DAG("wildfire_ingest_bronze",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    http_to_s3_task = HttpToS3Operator(
        task_id="wildfire_to_bronze_job",
        http_conn_id="usda_http",
        endpoint="/rds/archive/products/RDS-2013-0009.6/RDS-2013-0009.6_Data_Format4_SQLITE.zip",
        s3_bucket="bronze",
        s3_key="usda/wildfire.zip",
        aws_conn_id="aws_default",
        replace=True,
    )
