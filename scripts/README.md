# ECR Repository Creation Scripts

This directory contains scripts to create ECR repositories for your Lambda functions.

## Available Methods

### 1. Bash Script (Recommended - Simple)

**File:** `create-ecr-repositories.sh`

**Usage:**
```bash
# Set AWS region (optional, defaults to us-east-1)
export AWS_REGION=us-east-1

# Run the script
./scripts/create-ecr-repositories.sh
```

**Features:**
- Reads from `.github/lambda-ecr-mapping.txt`
- Creates all repositories automatically
- Checks if repositories already exist
- Shows repository URIs after creation
- Color-coded output

### 2. Python Script

**File:** `create-ecr-repositories.py`

**Usage:**
```bash
# Install boto3 if needed
pip install boto3

# Set AWS region (optional)
export AWS_REGION=us-east-1

# Run the script
python3 scripts/create-ecr-repositories.py
```

**Features:**
- Same functionality as bash script
- Better error handling
- Requires Python 3 and boto3

### 3. Terraform (Infrastructure as Code)

**File:** `ecr-terraform.tf`

**Usage:**
```bash
cd scripts
terraform init
terraform plan
terraform apply
```

**Features:**
- Infrastructure as Code approach
- Version controlled
- Can be integrated into CI/CD
- Easy to destroy and recreate

### 4. CloudFormation (AWS Native)

**File:** `ecr-cloudformation.yaml`

**Usage:**
```bash
aws cloudformation create-stack \
  --stack-name lambda-ecr-repositories \
  --template-body file://scripts/ecr-cloudformation.yaml \
  --region us-east-1
```

**Features:**
- AWS native solution
- Managed through AWS Console
- Easy to update

## Prerequisites

### For Bash/Python Scripts:
- AWS CLI installed and configured
- Appropriate IAM permissions (see `.github/IAM_POLICY_EXAMPLE.json`)

### For Terraform:
- Terraform installed
- AWS credentials configured
- Appropriate IAM permissions

### For CloudFormation:
- AWS CLI installed and configured
- CloudFormation permissions

## IAM Permissions Required

The user/role needs the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:CreateRepository",
        "ecr:DescribeRepositories",
        "ecr:PutImageScanningConfiguration"
      ],
      "Resource": "*"
    }
  ]
}
```

## Quick Start

1. **Configure AWS credentials:**
   ```bash
   aws configure
   ```

2. **Set AWS region (if different from us-east-1):**
   ```bash
   export AWS_REGION=your-region
   ```

3. **Run the bash script:**
   ```bash
   ./scripts/create-ecr-repositories.sh
   ```

4. **Verify repositories:**
   - Check AWS Console: https://console.aws.amazon.com/ecr
   - Or run: `aws ecr describe-repositories --region us-east-1`

## Troubleshooting

### "AWS credentials not configured"
- Run `aws configure` to set up credentials
- Or set environment variables: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

### "Repository already exists"
- This is normal if you run the script multiple times
- The script will skip existing repositories

### "Access Denied"
- Check IAM permissions
- Ensure you have `ecr:CreateRepository` permission

## Repository Configuration

All repositories are created with:
- **Image Scanning:** Enabled (scan on push)
- **Encryption:** AES256
- **Tag Mutability:** Mutable (allows overwriting tags)

## Next Steps

After creating repositories:
1. Update `.github/lambda-ecr-mapping.txt` if repository names differ
2. Configure GitHub Secrets with AWS credentials
3. Test the workflow by pushing code changes

