# PetFlow

Production-grade pet management platform built with Flask, PostgreSQL, Docker, Kubernetes, Terraform, and AWS.

## Architecture

Internet ? Cloudflare ? AWS ALB ? EKS Ingress ? PetFlow API Pods ? PostgreSQL RDS  
Pet images are stored in Amazon S3.

## Tech Stack

- Python Flask
- PostgreSQL RDS
- Docker
- Amazon ECR
- Amazon EKS
- Kubernetes
- Helm
- Terraform
- GitHub Actions
- AWS S3
- AWS ACM
- AWS Load Balancer Controller
- Cloudflare DNS

## Features

- JWT authentication
- Register and login
- Pet CRUD API
- Chip number support
- Image upload support
- OpenAPI endpoint
- Horizontal Pod Autoscaling
- HTTPS with ACM and ALB

## API

OpenAPI:

```text
https://petflow.shaked.in/openapi.json

