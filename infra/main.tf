resource "aws_s3_bucket" "bronze" {
  bucket = "bronze"
  acl    = "private"

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket" "silver" {
  bucket = "silver"
  acl    = "private"

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket" "gold" {
  bucket = "gold"
  acl    = "private"

  versioning {
    enabled = true
  }
}

module "jobs" {
  source        = "./jobs"
  bronze = aws_s3_bucket.bronze.bucket
  silver = aws_s3_bucket.silver.bucket
}