resource "aws_security_group" "web" { ingress { from_port = 22 to_port = 22 cidr_blocks = ["0.0.0.0/0"] } }
