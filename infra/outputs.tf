output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "nat_gateway_id" {
  value = aws_nat_gateway.main.id
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "rds_db_name" {
  value = aws_db_instance.postgres.db_name
}

output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "pet_images_bucket" {
  value = aws_s3_bucket.pet_images.bucket
}
output "petflow_api_irsa_role_arn" {
  value = module.petflow_api_irsa.arn
}
