# Quick ECR Setup Guide

## 🚀 Fastest Way to Create ECR Repositories

### Step 1: Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter default output format (json)
```

### Step 2: Run the Creation Script

```bash
# Make script executable (if not already)
chmod +x scripts/create-ecr-repositories.sh

# Set region if different from us-east-1
export AWS_REGION=us-east-1

# Run the script
./scripts/create-ecr-repositories.sh
```

That's it! The script will:
- ✅ Read all repository names from `.github/lambda-ecr-mapping.txt`
- ✅ Create all 10 ECR repositories
- ✅ Enable image scanning on push
- ✅ Show you all repository URIs

## 📋 What Gets Created

The script creates these repositories (based on your mapping file):
- `lambda-function-1-repo`
- `lambda-function-2-repo`
- `lambda-function-3-repo`
- ... (up to 10)

Each repository is configured with:
- **Image Scanning:** Enabled (automatically scans on push)
- **Encryption:** AES256
- **Tag Mutability:** Mutable

## 🔍 Verify Creation

### Option 1: AWS Console
Visit: https://console.aws.amazon.com/ecr/repositories

### Option 2: AWS CLI
```bash
aws ecr describe-repositories --region us-east-1
```

### Option 3: Check Specific Repository
```bash
aws ecr describe-repositories \
  --repository-names lambda-function-1-repo \
  --region us-east-1
```

## 🛠️ Alternative Methods

### Using Python Script
```bash
pip install boto3
python3 scripts/create-ecr-repositories.py
```

### Using Terraform
```bash
cd scripts
terraform init
terraform plan
terraform apply
```

### Using CloudFormation
```bash
aws cloudformation create-stack \
  --stack-name lambda-ecr-repos \
  --template-body file://scripts/ecr-cloudformation.yaml \
  --region us-east-1
```

## ⚠️ Troubleshooting

### "AWS credentials not configured"
```bash
aws configure
# OR
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

### "Access Denied"
You need IAM permissions. See `.github/IAM_POLICY_EXAMPLE.json` for required permissions.

### "Repository already exists"
This is fine! The script will skip existing repositories and continue.

## 📝 Next Steps After Creating Repositories

1. ✅ Verify repositories exist in AWS Console
2. ✅ Configure GitHub Secrets:
   - Go to: Repository → Settings → Secrets and variables → Actions
   - Add: `AWS_ROLE_TO_ASSUME` (IAM Role ARN) OR `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`
3. ✅ Test the workflow by pushing code changes to a Lambda function folder

## 🎯 Example Output

When you run the script, you'll see:

```
==========================================
ECR Repository Creation Script
==========================================
Region: us-east-1
Mapping File: .github/lambda-ecr-mapping.txt

AWS Account ID: 123456789012

Reading ECR repository mappings...

Processing: lambda-function-1 -> lambda-function-1-repo
  ✓ Created repository 'lambda-function-1-repo'
    URI: 123456789012.dkr.ecr.us-east-1.amazonaws.com/lambda-function-1-repo

...

==========================================
Summary
==========================================
✓ Successfully created/exists: 10
✓ All repositories ready!

==========================================
ECR Repository URIs
==========================================
lambda-function-1-repo: 123456789012.dkr.ecr.us-east-1.amazonaws.com/lambda-function-1-repo
...
```

## 💡 Pro Tips

1. **Custom Region:** Set `export AWS_REGION=eu-west-1` before running
2. **Dry Run:** Check the mapping file first: `cat .github/lambda-ecr-mapping.txt`
3. **Verify Permissions:** Test with: `aws sts get-caller-identity`
4. **Re-run Safe:** The script is idempotent - safe to run multiple times

