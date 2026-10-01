resource "aws_s3_bucket" "data" { bucket = "demo-public" acl = "public-read" }
