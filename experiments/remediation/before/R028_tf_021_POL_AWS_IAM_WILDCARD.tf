resource "aws_iam_policy" "iam1" {
  name = "iam1"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{Effect = "Allow", Action = "*", Resource = "*"}]
  })
}
