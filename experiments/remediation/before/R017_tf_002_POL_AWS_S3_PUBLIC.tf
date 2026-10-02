resource "aws_s3_bucket" "s32" {
  bucket = "cloudguard-s32"
  acl = "public-read"
}
