data "aws_iam_policy_document" "petflow_s3_policy" {
  statement {
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject"
    ]

    resources = [
      "${aws_s3_bucket.pet_images.arn}/*"
    ]
  }

  statement {
    actions = [
      "s3:ListBucket"
    ]

    resources = [
      aws_s3_bucket.pet_images.arn
    ]
  }
}

resource "aws_iam_policy" "petflow_s3_policy" {
  name        = "${var.project_name}-s3-policy"
  description = "Allow PetFlow API to access pet images bucket"
  policy      = data.aws_iam_policy_document.petflow_s3_policy.json
}

module "petflow_api_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts"
  version = "~> 6.0"

  name = "${var.project_name}-api-irsa"

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["default:petflow-api"]
    }
  }

  policies = {
    s3 = aws_iam_policy.petflow_s3_policy.arn
  }

  tags = local.common_tags
}
