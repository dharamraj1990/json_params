# Self-Adapting Lambda Deployment System

## Overview

The deployment system is now **fully dynamic and self-adapting**. When new Lambda functions are added, **no workflow changes are required**. The system automatically detects and deploys new functions based on the mapping file.

## Key Features

### 1. Dynamic Configuration Loading
- All configuration loaded from `.github/lambda-repo-map.json`
- No hardcoded values in workflow
- Single source of truth for all deployments

### 2. Self-Adapting Detection
- Automatically detects changed Lambda function folders
- Reads function configuration from mapping file
- Constructs all ARNs, URIs, and names dynamically

### 3. Pattern-Based Construction
All values are constructed using patterns:
- **OIDC ARN**: `arn:aws:iam::{account_id}:role/{role_name}`
- **ECR URI**: `{account_id}.dkr.ecr.{region}.amazonaws.com/{repo_name}`
- **Lambda Name**: `{env_prefix}-{region}-lambda-{function_number}`
- **Lambda ARN**: `arn:aws:lambda:{region}:{account_id}:function:{lambda_name}`
- **Image Tag**: `{lambda_name}-{commit_sha}`

## How It Works

### Adding a New Lambda Function

**Step 1**: Create the function folder
```bash
mkdir -p lambda-functions/lambda-function-6
# Add Dockerfile, lambda_function.py, requirements.txt
```

**Step 2**: Add to mapping file
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

**Step 3**: Push to repository
```bash
git add lambda-functions/lambda-function-6
git add .github/lambda-repo-map.json
git commit -m "Add lambda-function-6"
git push origin develop
```

**That's it!** The workflow will:
- ✅ Automatically detect the new folder
- ✅ Load configuration from mapping file
- ✅ Construct all ARNs and URIs dynamically
- ✅ Build and deploy the function

### No Workflow Changes Required!

The workflow automatically:
1. Detects changed folders
2. Reads function config from mapping
3. Constructs OIDC ARN from account + role name
4. Constructs ECR URI from account + region + repo name
5. Constructs Lambda name from env prefix + region + function number
6. Constructs image tag from lambda name + commit SHA
7. Deploys to correct environment

## Workflow Updates

### Before (Hardcoded)
```yaml
env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY_DEV: dev-us-east-1-repo
  AWS_ACCOUNT_DEV: 533269020590
  OIDC_ROLE_NAME: oidc-github-action

# Hardcoded construction
LAMBDA_NAME="dev-us-east-1-lambda-1"
ECR_REPO="dev-us-east-1-repo"
```

### After (Dynamic)
```yaml
env:
  MAP_FILE: .github/lambda-repo-map.json

# Dynamic construction from mapping
FUNCTION=$(jq -r ".lambda_functions[] | select(.folder_name == \"$FOLDER\")" "$MAP_FILE")
ACCOUNT_ID=$(jq -r ".aws_base_config.environments.$ENV.account_id" "$MAP_FILE")
LAMBDA_NAME="${ENV_PREFIX}-${REGION}-lambda-${FUNCTION_NUMBER}"
```

## Benefits

### 1. Zero Workflow Maintenance
- Add new functions without touching workflow
- Change account IDs in one place
- Update region globally

### 2. Consistency
- All functions use same naming patterns
- Standardized ARN construction
- Uniform deployment process

### 3. Scalability
- Add unlimited functions
- No workflow complexity growth
- Self-documenting via mapping file

### 4. Maintainability
- Single source of truth
- Easy to understand structure
- Clear separation of config and code

## Example: Adding Lambda Function 10

```json
// Add to lambda-repo-map.json
{
  "id": "lambda-10",
  "folder_name": "lambda-function-10",
  "function_number": "10",
  "description": "Lambda Function 10",
  "team": "backend-team",
  "ecr_repository_ref": {
    "dev": "dev",
    "staging": "staging",
    "prod": "staging"
  },
  "deployment": {
    "enabled": true,
    "deployment_order": 10,
    "dependencies": []
  }
}
```

The system will automatically:
- Construct: `dev-us-east-1-lambda-10`
- Use ECR: `dev-us-east-1-repo`
- Deploy to: dev environment (on develop branch)
- Tag image: `dev-us-east-1-lambda-10-{commit_sha}`

## Validation

The system validates:
- ✅ Function exists in mapping file
- ✅ ECR repository reference is valid
- ✅ Environment configuration exists
- ✅ All required fields present

## Error Handling

If a function is missing from mapping:
```
❌ ERROR: Function lambda-function-6 not found in mapping file
```

If ECR reference is invalid:
```
❌ ERROR: ECR repository reference 'invalid' not found
```

## Summary

The system is now **truly self-adapting**:
- ✅ Add functions by updating mapping file only
- ✅ No workflow changes needed
- ✅ All values constructed dynamically
- ✅ Standard patterns ensure consistency
- ✅ Scales infinitely without complexity

**The workflow is future-proof!** 🚀

