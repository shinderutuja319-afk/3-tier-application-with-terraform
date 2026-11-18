output "instance_id" {
  description = "CloudTask EC2 instance ID"
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "CloudTask EC2 public IP"
  value       = aws_instance.app.public_ip
}

output "instance_role_name" {
  description = "IAM role attached to EC2"
  value       = aws_iam_role.ec2_role.name
}
