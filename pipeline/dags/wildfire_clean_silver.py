from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.models import Variable
from datetime import datetime

with DAG('wildfire_clean_silver',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    bronze_to_silver = DatabricksSubmitRunOperator(
        task_id='wildfire_to_silver_job',
        databricks_conn_id='databricks_default',
        job_id=Variable.get("wildfire_clean_silver_job"),
    )
