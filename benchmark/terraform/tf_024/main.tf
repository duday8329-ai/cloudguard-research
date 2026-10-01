resource "aws_iam_policy" "iam4" {
  name = "iam4"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{Effect = "Allow", Action = "s3:GetObject", Resource = "*"}]
  })
}
