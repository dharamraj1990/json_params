# Lambda Deployment Setup Guide

## Overview

The workflow automatically deploys Lambda functions to three environments:
- **Dev**: Automatic deployment (no approval needed)
- **Staging**: Requires manual approval (input required)
- **Production**: Requires manual approval

## GitHub Environment Setup

### 1. Create GitHub Environments

Go to: Repository → Settings → Environments

Create three environments:
- `dev` - No protection rules (automatic deployment)
- `staging` - With required reviewers (manual approval)
- `production` - With required reviewers (manual approval)

### 2. Configure Environment Protection Rules

#### For Staging Environment:
1. Go to: Settings → Environments → `staging`
2. Add **Required reviewers** (who can approve deployments)
3. Optionally add deployment branches (e.g., `main` only)

#### For Production Environment:
1. Go to: Settings → Environments → `production`
2. Add **Required reviewers** (who can approve deployments)
3. Optionally add deployment branches (e.g., `main` only)
4. Consider adding wait timer for additional safety

## AWS IAM Roles Setup

### 1. Create Lambda Execution Roles

Create IAM roles for each environment:

#### Dev Role
```bash
aws iam create-role \
  --role-name lambda-execution-role-dev \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name lambda-execution-role-dev \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

#### Staging Role
```bash
aws iam create-role \
  --role-name lambda-execution-role-staging \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name lambda-execution-role-staging \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

#### Production Role
```bash
aws iam create-role \
  --role-name lambda-execution-role-prod \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name lambda-execution-role-prod \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

### 2. Get Role ARNs

```bash
# Get Dev Role ARN
aws iam get-role --role-name lambda-execution-role-dev --query 'Role.Arn' --output text

# Get Staging Role ARN
aws iam get-role --role-name lambda-execution-role-staging --query 'Role.Arn' --output text

# Get Production Role ARN
aws iam get-role --role-name lambda-execution-role-prod --query 'Role.Arn' --output text
```

### 3. Update Workflow File

Update the workflow file (`.github/workflows/lambda-build-push.yml`) with your role ARNs:

```yaml
env:
  DEV_LAMBDA_ROLE: arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role-dev
  STAGING_LAMBDA_ROLE: arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role-staging
  PROD_LAMBDA_ROLE: arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role-prod
```

## Lambda Function Naming

Functions are automatically named:
- Dev: `<lambda-folder-name>-dev` (e.g., `lambda-function-1-dev`)
- Staging: `<lambda-folder-name>-staging` (e.g., `lambda-function-1-staging`)
- Production: `<lambda-folder-name>-prod` (e.g., `lambda-function-1-prod`)

## Deployment Flow

1. **Build & Push**: Images are built and pushed to ECR
2. **Deploy Dev**: Automatically deploys to dev environment
3. **Deploy Staging**: Waits for manual approval, then deploys
4. **Deploy Production**: Waits for manual approval, then deploys

## Required AWS Permissions

The GitHub Actions IAM user/role needs:
- `lambda:CreateFunction`
- `lambda:UpdateFunctionCode`
- `lambda:GetFunction`
- `lambda:ListFunctions`
- `ecr:GetAuthorizationToken`
- `ecr:BatchGetImage`
- `ecr:GetDownloadUrlForLayer`

## Testing

1. Make a change to a Lambda function
2. Push to GitHub
3. Workflow will:
   - Build and push image
   - Auto-deploy to dev
   - Wait for approval for staging
   - Wait for approval for production

