resource "aws_db_instance" "rdspublic2" {
  allocated_storage = 20
  engine = "postgres"
  instance_class = "db.t3.micro"
  username = "admin"
  password = "change-me-for-test-only"
  skip_final_snapshot = true
  publicly_accessible = true
  storage_encrypted = true
}
