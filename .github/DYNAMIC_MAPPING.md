# Dynamic Lambda Mapping - Usage Guide

## Overview

The mapping file uses **dynamic construction patterns** instead of hardcoded values. All ARNs, URIs, and names are built from base configurations and patterns.

## Structure

### Base Configuration
- **AWS Base Config**: Region, account IDs, and environment prefixes
- **OIDC Config**: Role name and ARN pattern
- **ECR Config**: Registry pattern, repository pattern, and image tagging
- **Lambda Config**: Name and ARN patterns

### Lambda Functions
Each function only contains:
- Basic metadata (id, folder_name, function_number)
- ECR repository reference (which ECR repo to use per environment)
- Deployment settings

## Dynamic Construction

### 1. OIDC ARN
```bash
# Pattern: arn:aws:iam::{account_id}:role/{role_name}
# Example: arn:aws:iam::533269020590:role/oidc-github-action

ACCOUNT_ID=$(jq -r ".aws_base_config.environments.$ENV.account_id" map.json)
ROLE_NAME=$(jq -r '.oidc_config.role_name' map.json)
OIDC_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"
```

### 2. ECR URI
```bash
# Pattern: {account_id}.dkr.ecr.{region}.amazonaws.com/{repo_name}
# Example: 533269020590.dkr.ecr.us-east-1.amazonaws.com/dev-us-east-1-repo

ACCOUNT_ID=$(jq -r ".aws_base_config.environments.$ENV.account_id" map.json)
REGION=$(jq -r '.aws_base_config.region' map.json)
ECR_REF=$(jq -r ".lambda_functions[] | select(.folder_name == \"$FOLDER\") | .ecr_repository_ref.$ENV" map.json)
REPO_NAME=$(jq -r ".ecr_config.repositories.$ECR_REF.name" map.json)
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"
```

### 3. Lambda Name
```bash
# Pattern: {env_prefix}-{region}-lambda-{function_number}
# Example: dev-us-east-1-lambda-1

ENV_PREFIX=$(jq -r ".aws_base_config.environments.$ENV.env_prefix" map.json)
REGION=$(jq -r '.aws_base_config.region' map.json)
FUNCTION_NUMBER=$(jq -r ".lambda_functions[] | select(.folder_name == \"$FOLDER\") | .function_number" map.json)
LAMBDA_NAME="${ENV_PREFIX}-${REGION}-lambda-${FUNCTION_NUMBER}"
```

### 4. Lambda ARN
```bash
# Pattern: arn:aws:lambda:{region}:{account_id}:function:{lambda_name}
# Example: arn:aws:lambda:us-east-1:533269020590:function:dev-us-east-1-lambda-1

REGION=$(jq -r '.aws_base_config.region' map.json)
ACCOUNT_ID=$(jq -r ".aws_base_config.environments.$ENV.account_id" map.json)
LAMBDA_NAME="..." # from above
LAMBDA_ARN="arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${LAMBDA_NAME}"
```

### 5. Image Tag
```bash
# Pattern: {lambda_name}-{commit_sha}
# Example: dev-us-east-1-lambda-1-abc123def456

LAMBDA_NAME="..." # from above
COMMIT_SHA="${GITHUB_SHA}"
IMAGE_TAG="${LAMBDA_NAME}-${COMMIT_SHA}"
```

### 6. Image URI
```bash
# Pattern: {ecr_uri}:{image_tag}
# Example: 533269020590.dkr.ecr.us-east-1.amazonaws.com/dev-us-east-1-repo:dev-us-east-1-lambda-1-abc123

ECR_URI="..." # from above
IMAGE_TAG="..." # from above
IMAGE_URI="${ECR_URI}:${IMAGE_TAG}"
```

## Using the Helper Script

The helper script (`helpers/get-lambda-config.sh`) constructs all values automatically:

```bash
# Get all configuration for a function
./helpers/get-lambda-config.sh lambda-function-1 dev abc123def456

# Output (JSON):
{
  "folder_name": "lambda-function-1",
  "environment": "dev",
  "account_id": "533269020590",
  "region": "us-east-1",
  "env_prefix": "dev",
  "oidc_arn": "arn:aws:iam::533269020590:role/oidc-github-action",
  "ecr_repository_name": "dev-us-east-1-repo",
  "ecr_uri": "533269020590.dkr.ecr.us-east-1.amazonaws.com/dev-us-east-1-repo",
  "lambda_name": "dev-us-east-1-lambda-1",
  "lambda_arn": "arn:aws:lambda:us-east-1:533269020590:function:dev-us-east-1-lambda-1",
  "image_tag": "dev-us-east-1-lambda-1-abc123def456",
  "image_uri": "533269020590.dkr.ecr.us-east-1.amazonaws.com/dev-us-east-1-repo:dev-us-east-1-lambda-1-abc123def456",
  "commit_sha": "abc123def456"
}
```

## GitHub Actions Usage

```yaml
- name: Get Lambda Configuration
  id: lambda-config
  run: |
    CONFIG=$(./.github/helpers/get-lambda-config.sh ${{ matrix.folder }} ${{ env.ENVIRONMENT }} ${{ github.sha }})
    echo "oidc_arn=$(echo $CONFIG | jq -r '.oidc_arn')" >> $GITHUB_OUTPUT
    echo "ecr_uri=$(echo $CONFIG | jq -r '.ecr_uri')" >> $GITHUB_OUTPUT
    echo "lambda_name=$(echo $CONFIG | jq -r '.lambda_name')" >> $GITHUB_OUTPUT
    echo "lambda_arn=$(echo $CONFIG | jq -r '.lambda_arn')" >> $GITHUB_OUTPUT
    echo "image_uri=$(echo $CONFIG | jq -r '.image_uri')" >> $GITHUB_OUTPUT

- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ steps.lambda-config.outputs.oidc_arn }}
    aws-region: us-east-1

- name: Deploy Lambda
  run: |
    aws lambda update-function-code \
      --function-name ${{ steps.lambda-config.outputs.lambda_name }} \
      --image-uri ${{ steps.lambda-config.outputs.image_uri }} \
      --region us-east-1
```

## Benefits

1. **Single Source of Truth**: All values constructed from base config
2. **No Duplication**: Patterns defined once, used everywhere
3. **Easy Updates**: Change account ID or region in one place
4. **Standard Patterns**: Consistent naming across all resources
5. **Dynamic**: Works for any environment/function combination
6. **Maintainable**: Clear separation of config and data

## Adding New Functions

To add a new function, simply add to `lambda_functions` array:

```json
{
  "id": "lambda-6",
  "folder_name": "lambda-function-6",
  "function_number": "6",
  "description": "Lambda Function 6",
  "team": "backend-team",
  "ecr_repository_ref": {
    "dev": "dev",
    "staging": "staging",
    "prod": "staging"
  },
  "deployment": {
    "enabled": true,
    "deployment_order": 6,
    "dependencies": []
  }
}
```

All ARNs, names, and URIs will be automatically constructed using the patterns!

