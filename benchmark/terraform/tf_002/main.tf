resource "aws_s3_bucket" "logs" { bucket = "demo-private" acl = "private" }
