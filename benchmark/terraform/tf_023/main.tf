resource "aws_iam_policy" "iam3" {
  name = "iam3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{Effect = "Allow", Action = "*", Resource = "*"}]
  })
}
