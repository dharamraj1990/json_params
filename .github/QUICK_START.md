# Quick Start Guide

## 5-Minute Setup

### Step 1: Create ECR Repositories

Run this script to create all 10 ECR repositories (or modify for your needs):

```bash
# Set your AWS region
REGION="us-east-1"

# Create repositories
for i in {1..10}; do
  aws ecr create-repository \
    --repository-name lambda-function-$i-repo \
    --region $REGION \
    --image-scanning-configuration scanOnPush=true
done
```

### Step 2: Update ECR Mapping

Edit `.github/lambda-ecr-mapping.txt` and ensure folder names match your actual folders:

```
lambda-function-1:lambda-function-1-repo
lambda-function-2:lambda-function-2-repo
...
```

### Step 3: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add:
- `AWS_ROLE_TO_ASSUME`: Your IAM Role ARN (if using IAM roles)
- OR `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (if using access keys)

### Step 4: Create Lambda Function Structure

Run the setup script:
```bash
./setup-example.sh
```

Or manually create folders:
```bash
mkdir -p lambda-functions/lambda-function-1
# Copy Dockerfile, requirements.txt, and lambda_function.py
```

### Step 5: Test the Workflow

1. Make a change to any file in `lambda-functions/lambda-function-1/`
2. Commit and push to `main` or `develop` branch
3. Check GitHub Actions tab to see the workflow run
4. Verify image in ECR console

## Verification Checklist

- [ ] ECR repositories created
- [ ] `.github/lambda-ecr-mapping.txt` updated with correct mappings
- [ ] GitHub Secrets configured (AWS credentials)
- [ ] At least one Lambda function folder created with Dockerfile
- [ ] Workflow file exists at `.github/workflows/lambda-build-push.yml`
- [ ] Test commit pushed and workflow triggered

## Common Issues

**Workflow not running?**
- Check that changes are in `lambda-functions/` directory
- Verify workflow file is in `.github/workflows/`

**ECR push failing?**
- Verify IAM permissions
- Check ECR repository names match mapping file
- Ensure repositories exist in the correct region

**Build failing?**
- Check Dockerfile syntax
- Verify requirements.txt has valid packages
- Check Lambda handler path in Dockerfile CMD

