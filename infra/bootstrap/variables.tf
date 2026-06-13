variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "state_bucket_name" {
  type    = string
  default = "petflow-terraform-state-160885257498"
}

variable "lock_table_name" {
  type    = string
  default = "petflow-terraform-locks"
}
