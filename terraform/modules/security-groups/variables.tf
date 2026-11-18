variable "project_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "allowed_cidr" {
  description = "IP range allowed to access the web application"
  type        = string
  default     = "0.0.0.0/0"
}
