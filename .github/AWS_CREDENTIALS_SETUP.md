# AWS Credentials Setup for GitHub Actions

This guide explains how to configure AWS credentials for the Lambda CI/CD workflow.

## Option 1: IAM Role (Recommended - More Secure)

This method uses OIDC (OpenID Connect) to assume an IAM role without storing long-lived credentials.

### Step 1: Create IAM Role in AWS

1. Go to AWS IAM Console → Roles → Create Role
2. Select "Web Identity" as trusted entity type
3. Choose your identity provider:
   - **For GitHub.com**: `token.actions.githubusercontent.com`
   - **For GitHub Enterprise Server**: Your GitHub Enterprise Server URL
4. Configure the role:
   - Audience: `sts.amazonaws.com`
   - Add condition: `StringEquals` → `token.actions.githubusercontent.com:aud` = `sts.amazonaws.com`
   - Add condition: `StringLike` → `token.actions.githubusercontent.com:sub` = `repo:YOUR_GITHUB_USERNAME/YOUR_REPO_NAME:*`
5. Attach the policy from `.github/IAM_POLICY_EXAMPLE.json` or create a custom policy with ECR permissions
6. Note the Role ARN (e.g., `arn:aws:iam::123456789012:role/github-actions-role`)

### Step 2: Configure GitHub Repository

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add secret:
   - **Name**: `AWS_ROLE_TO_ASSUME`
   - **Value**: Your IAM Role ARN (e.g., `arn:aws:iam::123456789012:role/github-actions-role`)

### Step 3: Update Workflow (if needed)

The workflow should already be configured. Verify it uses:
```yaml
role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
```

## Option 2: Access Keys (Less Secure - Quick Setup)

This method uses AWS access keys stored in GitHub Secrets.

### Step 1: Create IAM User in AWS

1. Go to AWS IAM Console → Users → Create User
2. Name: `github-actions-user` (or your preferred name)
3. Select "Provide user access to the AWS Management Console" → **No** (programmatic access only)
4. Attach the policy from `.github/IAM_POLICY_EXAMPLE.json` or create a custom policy with ECR permissions
5. Create the user and **save the Access Key ID and Secret Access Key** (you won't see the secret again!)

### Step 2: Configure GitHub Repository

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Add two secrets:

   **Secret 1:**
   - **Name**: `AWS_ACCESS_KEY_ID`
   - **Value**: Your Access Key ID

   **Secret 2:**
   - **Name**: `AWS_SECRET_ACCESS_KEY`
   - **Value**: Your Secret Access Key

### Step 3: Update Workflow

If you want to use only access keys (not IAM role), update the workflow:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ env.AWS_REGION }}
```

## Required IAM Permissions

The IAM role or user needs the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeRepositories",
        "ecr:DescribeImages",
        "ecr:ListImages"
      ],
      "Resource": "arn:aws:ecr:*:*:repository/lambda-function-*"
    }
  ]
}
```

Or use the policy file: `.github/IAM_POLICY_EXAMPLE.json`

## Verification

After setting up credentials:

1. Make a test commit to a Lambda function folder
2. Check the GitHub Actions workflow run
3. The "Configure AWS credentials" step should succeed
4. If it fails, check:
   - Secret names match exactly (case-sensitive)
   - IAM role/user has correct permissions
   - Region is correct in workflow file

## Troubleshooting

### Error: "Credentials could not be loaded"
- **Check**: Secrets are configured in GitHub repository settings
- **Check**: Secret names match exactly (case-sensitive): `AWS_ROLE_TO_ASSUME` or `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`
- **Check**: IAM role/user exists and has correct permissions

### Error: "Access Denied" when pushing to ECR
- **Check**: IAM policy includes all required ECR permissions
- **Check**: ECR repository names match the mapping file
- **Check**: Repository exists in the correct AWS region

### Error: "Role cannot be assumed"
- **Check**: IAM role trust policy includes GitHub as a trusted entity
- **Check**: Repository name in trust policy matches your GitHub repository
- **Check**: Role ARN is correct in GitHub secret

## Security Best Practices

1. ✅ **Use IAM Roles** instead of access keys when possible
2. ✅ **Limit permissions** to only what's needed (ECR operations)
3. ✅ **Use conditions** in IAM role trust policy to restrict to specific repositories
4. ✅ **Rotate credentials** regularly if using access keys
5. ✅ **Never commit** AWS credentials to the repository

## Quick Setup Checklist

- [ ] IAM role created OR IAM user created with ECR permissions
- [ ] GitHub Secrets configured (`AWS_ROLE_TO_ASSUME` OR `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`)
- [ ] ECR repositories created (run `./scripts/create-ecr-repositories.sh`)
- [ ] Workflow file uses correct secret names
- [ ] Test commit pushed to verify credentials work

