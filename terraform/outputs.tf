output "vpc_id" {
  description = "CloudTask VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_id" {
  description = "CloudTask public subnet ID"
  value       = module.vpc.public_subnet_id
}

output "internet_gateway_id" {
  description = "CloudTask Internet Gateway ID"
  value       = module.vpc.internet_gateway_id
}

output "ec2_instance_id" {
  value = module.ec2.instance_id
}

output "ec2_public_ip" {
  value = module.ec2.public_ip
}

output "ec2_iam_role" {
  value = module.ec2.instance_role_name
}