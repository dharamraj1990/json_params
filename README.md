# Lambda Functions CI/CD Workflow

This repository contains a GitHub Actions workflow that automatically builds Docker images and pushes them to AWS ECR when Lambda function code changes are detected.

## Features

- ✅ **Automatic Change Detection**: Detects which Lambda function folders have changed
- ✅ **Parallel Builds**: Builds multiple Lambda functions in parallel when multiple folders are changed
- ✅ **ECR Integration**: Pushes images to respective ECR repositories for each Lambda function
- ✅ **Smart Tagging**: Tags images with commit SHA and Lambda function name
- ✅ **Fail-Safe**: Continues building other images even if one fails
- ✅ **Multi-Environment Deployment**: Auto-deploy to dev, manual approval for staging and production
- ✅ **Error Handling**: Automatic retry logic and conflict resolution for Lambda updates

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
  --repository-name lambda-function-1-repo \
  --region $AWS_REGION \
  --image-scanning-configuration scanOnPush=true
```

**Note:** 
- Only **one ECR repository** is needed for all Lambda functions
- Images are tagged with the Lambda function name (e.g., `lambda-function-1-<commit-sha>`)
- Make sure AWS credentials are configured (`aws configure`) before running commands

### 2. Image Tagging Convention

The workflow uses a **single ECR repository** and tags images by Lambda function name:

- **ECR Repository**: `lambda-function-1-repo` (single repository for all functions)
- **Image Tag**: `<lambda-function-name>-<commit-sha>`

**Examples:**
- `lambda-function-1` → `lambda-function-1-repo:lambda-function-1-abc123def456`
- `lambda-function-2` → `lambda-function-1-repo:lambda-function-2-abc123def456`
- `lambda-function-3` → `lambda-function-1-repo:lambda-function-3-abc123def456`

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

### 4. Manual Approval Setup (Works on Free GitHub Accounts)

**IMPORTANT**: The workflow uses manual approval via GitHub Issues, which works on **free GitHub accounts** (no Enterprise required).

#### How Manual Approval Works:

The workflow automatically creates GitHub Issues for staging and production deployments that require approval:

1. **Staging Deployment**:
   - After images are built and pushed, an approval job runs
   - A GitHub Issue is created with title: "🚀 Staging Deployment Approval Required"
   - The workflow pauses and waits for approval

2. **Production Deployment**:
   - After images are built and pushed, an approval job runs
   - A GitHub Issue is created with title: "🚀 Production Deployment Approval Required"
   - The workflow pauses and waits for approval

#### How to Approve or Reject:

When an approval issue is created:

1. **Go to the Issues tab** in your repository
2. **Find the approval issue** (it will be automatically created)
3. **Comment on the issue**:
   - Type `/approve` to approve the deployment
   - Type `/reject` to reject the deployment
4. **The workflow will automatically continue** once approved (or fail if rejected)

#### Configuration:

The approval is configured to use the person who triggered the workflow (`${{ github.actor }}`) as the approver. To change this:

1. Edit `.github/workflows/lambda-build-push.yml`
2. Find the `approve-staging` and `approve-production` jobs
3. Update the `approvers` field with GitHub usernames (comma-separated):
   ```yaml
   approvers: username1,username2,username3
   ```
4. Adjust `minimum-approvals` if you need multiple approvals

#### Deployment Flow:

- **Dev Environment**: Deploys automatically (no approval needed)
- **Staging Environment**: Requires manual approval via GitHub Issue
- **Production Environment**: Requires manual approval via GitHub Issue

**Note**: This approach works on free GitHub accounts and doesn't require GitHub Enterprise or paid plans.

### 5. Configure Workflow Settings

Edit `.github/workflows/lambda-build-push.yml`:

- Update `AWS_REGION` in the `env` section (default: `us-east-1`)
- Update branch names if different from `main` or `develop`
- Adjust paths if your Lambda functions are in a different directory

### 6. Create Lambda Function Folders

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
4. **ECR Push**: Images are tagged with `<lambda-name>-<commit-sha>`, then pushed to the ECR repository
5. **Deployment**:
   - **Dev**: Automatically deploys to Lambda functions (no approval)
   - **Staging**: Waits for manual approval, then deploys
   - **Production**: Waits for manual approval, then deploys

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
- **Lambda Name + Commit SHA**: `<lambda-function-name>-<commit-sha>` (for traceability)

Example:
- `123456789.dkr.ecr.us-east-1.amazonaws.com/lambda-function-1-repo:lambda-function-1-abc123def456`
- `123456789.dkr.ecr.us-east-1.amazonaws.com/lambda-function-1-repo:lambda-function-2-abc123def456`

## Deployment Flow

### Automatic Deployment (Dev)
- Triggers on push to `main` or `develop` branches
- No approval required
- Updates existing Lambda functions: `lambda-function-1`, `lambda-function-2`, etc.

### Manual Approval (Staging & Production)
- Triggers on push to `main` branch only
- Requires manual approval from configured reviewers
- Workflow pauses at the deployment step
- Reviewers receive notifications and can approve/reject
- Once approved, deployment proceeds automatically

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
