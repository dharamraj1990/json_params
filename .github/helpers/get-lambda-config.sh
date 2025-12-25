#!/bin/bash
# Dynamic Lambda Configuration Helper
# Usage: ./get-lambda-config.sh <folder_name> <environment> <commit_sha>

set -e

MAP_FILE=".github/lambda-repo-map.json"
FOLDER_NAME="${1:-lambda-function-1}"
ENVIRONMENT="${2:-dev}"
COMMIT_SHA="${3:-${GITHUB_SHA:-latest}}"

# Load base config
REGION=$(jq -r '.aws_base_config.region' "$MAP_FILE")
ENV_CONFIG=$(jq -r ".aws_base_config.environments.$ENVIRONMENT" "$MAP_FILE")
ACCOUNT_ID=$(echo "$ENV_CONFIG" | jq -r '.account_id')
ENV_PREFIX=$(echo "$ENV_CONFIG" | jq -r '.env_prefix')

# Load function config
FUNCTION=$(jq -r ".lambda_functions[] | select(.folder_name == \"$FOLDER_NAME\")" "$MAP_FILE")
FUNCTION_NUMBER=$(echo "$FUNCTION" | jq -r '.function_number')
ECR_REF=$(echo "$FUNCTION" | jq -r ".ecr_repository_ref.$ENVIRONMENT")

# Get ECR repository name
ECR_REPO_NAME=$(jq -r ".ecr_config.repositories.$ECR_REF.name" "$MAP_FILE")

# Construct values dynamically
OIDC_ROLE_NAME=$(jq -r '.oidc_config.role_name' "$MAP_FILE")
OIDC_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${OIDC_ROLE_NAME}"

ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO_NAME}"

LAMBDA_NAME="${ENV_PREFIX}-${REGION}-lambda-${FUNCTION_NUMBER}"
LAMBDA_ARN="arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${LAMBDA_NAME}"

IMAGE_TAG="${LAMBDA_NAME}-${COMMIT_SHA}"
IMAGE_URI="${ECR_URI}:${IMAGE_TAG}"

# Output as JSON for easy parsing
jq -n \
  --arg folder_name "$FOLDER_NAME" \
  --arg environment "$ENVIRONMENT" \
  --arg account_id "$ACCOUNT_ID" \
  --arg region "$REGION" \
  --arg env_prefix "$ENV_PREFIX" \
  --arg oidc_arn "$OIDC_ARN" \
  --arg ecr_repo_name "$ECR_REPO_NAME" \
  --arg ecr_uri "$ECR_URI" \
  --arg lambda_name "$LAMBDA_NAME" \
  --arg lambda_arn "$LAMBDA_ARN" \
  --arg image_tag "$IMAGE_TAG" \
  --arg image_uri "$IMAGE_URI" \
  --arg commit_sha "$COMMIT_SHA" \
  '{
    folder_name: $folder_name,
    environment: $environment,
    account_id: $account_id,
    region: $region,
    env_prefix: $env_prefix,
    oidc_arn: $oidc_arn,
    ecr_repository_name: $ecr_repo_name,
    ecr_uri: $ecr_uri,
    lambda_name: $lambda_name,
    lambda_arn: $lambda_arn,
    image_tag: $image_tag,
    image_uri: $image_uri,
    commit_sha: $commit_sha
  }'

