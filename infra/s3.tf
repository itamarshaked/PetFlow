resource "aws_s3_bucket" "pet_images" {
  bucket = "${var.project_name}-pet-images-${data.aws_caller_identity.current.account_id}"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-pet-images"
  })
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket_public_access_block" "pet_images" {
  bucket = aws_s3_bucket.pet_images.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
