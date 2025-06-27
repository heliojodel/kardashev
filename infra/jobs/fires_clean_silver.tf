resource "databricks_dbfs_file" "wildfire_clean_silver" {
  source = "${path.root}/scripts/wildfire_clean_silver.py"
  path   = "dbfs:/jobs/wildfire_clean_silver.py"
}

resource "databricks_job" "wildfire_clean_silver" {
  new_cluster {
    spark_version = "14.3.x-scala2.12"
    node_type_id  = "i3.xlarge"
    num_workers   = 2
  }

  spark_python_task {
    python_file = "dbfs:/jobs/wildfire_clean_silver.py"
    parameters  = [
      "--input_path", "s3://${var.bronze}/",
      "--output_path", "s3://${var.silver}/"
    ]
  }

  depends_on = [databricks_dbfs_file.wildfire_clean_silver]

}

resource "airflow_variable" "wildfire_clean_silver" {
  key   = "wildfire_clean_silver_job"
  value = databricks_job.wildfire_clean_silver.id
}