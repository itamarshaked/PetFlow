module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = "${var.project_name}-cluster"
  kubernetes_version = "1.33"

  endpoint_public_access                   = true
  enable_cluster_creator_admin_permissions = true

  addons = {
    vpc-cni = {
      most_recent    = true
      before_compute = true
    }

    kube-proxy = {
      most_recent = true
    }

    coredns = {
      most_recent = true
    }
  }

  vpc_id = aws_vpc.main.id

  subnet_ids = aws_subnet.private[*].id

  eks_managed_node_groups = {

    default = {

      instance_types = ["t3.medium"]

      min_size     = 1
      desired_size = 1
      max_size     = 3

      capacity_type = "ON_DEMAND"
    }
  }

  tags = {
    Project = var.project_name
    Managed = "Terraform"
  }
}
