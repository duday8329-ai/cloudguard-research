resource "aws_db_instance" "demo" {
  identifier             = "cloudguard-demo"
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  publicly_accessible    = true
  storage_encrypted      = true
  skip_final_snapshot    = true
}
