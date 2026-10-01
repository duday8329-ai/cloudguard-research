resource "aws_iam_policy" "iam5" {
  name = "iam5"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{Effect = "Allow", Action = "s3:GetObject", Resource = "*"}]
  })
}
