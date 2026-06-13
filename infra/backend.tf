terraform {
  backend "s3" {
    bucket         = "petflow-terraform-state-160885257498"
    key            = "production/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "petflow-terraform-locks"
    encrypt        = true
  }
}
