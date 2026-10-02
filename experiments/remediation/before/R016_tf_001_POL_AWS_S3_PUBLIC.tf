resource "aws_s3_bucket" "s31" {
  bucket = "cloudguard-s31"
  acl = "public-read"
}
