resource "aws_ecr_repository" "api" {
  name = "${var.project_name}-api"

  image_tag_mutability = "MUTABLE"  #IMMUTABLE to fix Checkov CKV_AWS_293

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.common_tags
}
