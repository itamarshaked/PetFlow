variable "project_name" {
  type    = string
  default = "petflow"
}

variable "aws_region" {
  type    = string
  default = "eu-west-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "db_name" {
  type    = string
  default = "petflow"
}

variable "db_username" {
  type    = string
  default = "petflow_admin"
}

variable "db_password" {
  type      = string
  sensitive = true
}
