# Lambda Functions CI/CD Workflow

This repository contains a GitHub Actions workflow that automatically builds Docker images and pushes them to AWS ECR when Lambda function code changes are detected.

## Features

- ✅ **Automatic Change Detection**: Detects which Lambda function folders have changed
- ✅ **Parallel Builds**: Builds multiple Lambda functions in parallel when multiple folders are changed
- ✅ **ECR Integration**: Pushes images to respective ECR repositories for each Lambda function
- ✅ **Smart Tagging**: Tags images with commit SHA and `latest` tag
- ✅ **Fail-Safe**: Continues building other images even if one fails

## Repository Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── lambda-build-push.yml    # Main workflow file
├── lambda-functions/
│   ├── lambda-function-1/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── lambda_function.py
│   ├── lambda-function-2/
│   │   └── ...
│   └── ... (up to 10 lambda functions)
└── README.md
```

## Setup Instructions

### 1. Create ECR Repository

Create a **single ECR repository** for all Lambda functions:

```bash
# Set your AWS region
export AWS_REGION=us-east-1

# Create single ECR repository
aws ecr create-repository \
  --repository-name lambda-functions-repo \
  --region $AWS_REGION \
  --image-scanning-configuration scanOnPush=true
```

**Note:** 
- Only **one ECR repository** is needed for all Lambda functions
- Images are tagged with the Lambda function name (e.g., `lambda-function-1-<commit-sha>`)
- Make sure AWS credentials are configured (`aws configure`) before running commands

### 2. Image Tagging Convention

The workflow uses a **single ECR repository** and tags images by Lambda function name:

- **ECR Repository**: `lambda-functions-repo` (single repository for all functions)
- **Image Tags**: `<lambda-function-name>-<commit-sha>`, `<lambda-function-name>-<short-sha>`, `<lambda-function-name>-latest`

**Examples:**
- `lambda-function-1` → `lambda-functions-repo:lambda-function-1-abc123def456`
- `lambda-function-2` → `lambda-functions-repo:lambda-function-2-abc123def456`
- `lambda-function-3` → `lambda-functions-repo:lambda-function-3-abc123def456`

This allows you to:
- Store all Lambda images in one repository
- Easily identify which Lambda function each image belongs to
- Track versions using commit SHA in the tag

### 3. Set Up AWS Credentials in GitHub

You have two options:

#### Option A: IAM Role (Recommended - More Secure)

1. Create an IAM role in AWS with ECR permissions
2. Add the role ARN to GitHub Secrets as `AWS_ROLE_TO_ASSUME`

Required IAM permissions:
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `ecr:PutImage`
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`
- `ecr:DescribeRepositories`
- `ecr:DescribeImages`
- `ecr:ListImages`

These should be applied to resources: `arn:aws:ecr:*:*:repository/lambda-function-*`

#### Option B: Access Keys (Less Secure)

1. Create an IAM user with ECR permissions
2. Add to GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

Then update the workflow file to use access keys instead of IAM role.

### 4. Configure Workflow Settings

Edit `.github/workflows/lambda-build-push.yml`:

- Update `AWS_REGION` in the `env` section (default: `us-east-1`)
- Update branch names if different from `main` or `develop`
- Adjust paths if your Lambda functions are in a different directory

### 5. Create Lambda Function Folders

For each Lambda function, create a folder under `lambda-functions/` with:

- **Dockerfile**: Docker configuration for building the Lambda image
- **requirements.txt**: Python dependencies
- **lambda_function.py**: Your Lambda handler code

Example Dockerfile:
```dockerfile
FROM public.ecr.aws/lambda/python:3.11
WORKDIR ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "lambda_function.lambda_handler" ]
```

## How It Works

1. **Change Detection**: When code is pushed, the workflow detects which folders under `lambda-functions/` have changed
2. **Parallel Execution**: For each changed folder, a separate build job runs in parallel
3. **Image Building**: Each job builds a Docker image for its Lambda function
4. **ECR Push**: Images are tagged with the commit SHA and `latest`, then pushed to the respective ECR repository

## Workflow Triggers

The workflow runs on:
- Push to `main` or `develop` branches (only if files in `lambda-functions/` change)
- Pull requests to `main` or `develop` branches (only if files in `lambda-functions/` change)

## Example Scenarios

### Scenario 1: Single Folder Changed
- Change made to `lambda-functions/lambda-function-1/`
- Only `lambda-function-1` image is built and pushed to its ECR repo

### Scenario 2: Multiple Folders Changed
- Changes made to `lambda-functions/lambda-function-1/` and `lambda-functions/lambda-function-3/`
- Both images are built in parallel and pushed to their respective ECR repos

### Scenario 3: No Lambda Function Changes
- Changes made outside `lambda-functions/` directory
- Workflow detects no changes and skips execution

## Image Tags

Each image is tagged with:
- **Commit SHA**: `abc123def456...` (for traceability)
- **Latest**: `latest` (for convenience)

Example:
- `123456789.dkr.ecr.us-east-1.amazonaws.com/lambda-function-1-repo:abc123def456`
- `123456789.dkr.ecr.us-east-1.amazonaws.com/lambda-function-1-repo:latest`

## Troubleshooting

### Workflow not triggering
- Ensure changes are in `lambda-functions/` directory
- Check that workflow file is in `.github/workflows/` directory
- Verify branch names match your repository

### ECR push fails
- Verify AWS credentials are correctly configured
- Check IAM permissions for ECR operations
- Ensure ECR repositories exist and names match the mapping file

### Build fails
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt are valid
- Check Lambda handler path in Dockerfile CMD

## Customization

### Change AWS Region
Update `AWS_REGION` in the workflow file's `env` section.

### Change Branch Names
Update the `on.push.branches` section in the workflow file.

### Change Lambda Function Directory
Update the `paths` filter and folder detection logic in the workflow.

### Add Environment Variables
Add environment variables to the workflow or use GitHub Secrets for sensitive values.

## Security Best Practices

1. ✅ Use IAM roles instead of access keys when possible
2. ✅ Limit IAM permissions to only what's needed (ECR operations)
3. ✅ Use GitHub Secrets for sensitive information
4. ✅ Enable ECR image scanning in AWS
5. ✅ Use specific image tags (commit SHA) instead of `latest` in production

## Support

For issues or questions, please check:
- GitHub Actions logs for detailed error messages
- AWS CloudWatch logs for ECR operations
- IAM policy permissions
