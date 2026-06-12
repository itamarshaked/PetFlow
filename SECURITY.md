# Security Policy

## Security Features

PetFlow includes:

- HTTPS using AWS ACM and ALB
- JWT-based authentication
- Kubernetes Secrets for runtime configuration
- IAM Roles for Service Accounts (IRSA)
- Private RDS access inside the VPC
- Least-privilege IAM policy for S3 access

## Secrets

Sensitive values must not be committed to Git.

Examples:

- Database passwords
- JWT secrets
- AWS access keys
- Terraform tfvars files
- Local .env files

## Reporting Security Issues

This is a portfolio project. Security issues should be fixed directly through pull requests or private communication with the project owner.
