resource "aws_db_instance" "rdsencryption4" {
  allocated_storage = 20
  engine = "postgres"
  instance_class = "db.t3.micro"
  username = "admin"
  password = "change-me-for-test-only"
  skip_final_snapshot = true
  publicly_accessible = false
  storage_encrypted = true
}
