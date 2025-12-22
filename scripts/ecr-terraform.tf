# Terraform configuration to create ECR repositories
# Usage: terraform init && terraform plan && terraform apply

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for ECR repositories"
  type        = string
  default     = "us-east-1"
}

variable "repositories" {
  description = "List of ECR repository names"
  type        = list(string)
  default = [
    "lambda-function-1-repo",
    "lambda-function-2-repo",
    "lambda-function-3-repo",
    "lambda-function-4-repo",
    "lambda-function-5-repo",
    "lambda-function-6-repo",
    "lambda-function-7-repo",
    "lambda-function-8-repo",
    "lambda-function-9-repo",
    "lambda-function-10-repo"
  ]
}

# Create ECR repositories
resource "aws_ecr_repository" "lambda_repos" {
  for_each = toset(var.repositories)

  name                 = each.value
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name        = each.value
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

# Output repository URIs
output "ecr_repository_urls" {
  description = "URLs of the ECR repositories"
  value = {
    for k, v in aws_ecr_repository.lambda_repos : k => v.repository_url
  }
}

output "ecr_repository_arns" {
  description = "ARNs of the ECR repositories"
  value = {
    for k, v in aws_ecr_repository.lambda_repos : k => v.arn
  }
}

