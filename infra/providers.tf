provider "aws" {
  region = var.aws_region
}

provider "airflow" {
  base_url = "http://airflow-webserver:8080/"
  username = "admin"
  password = "admin"
}