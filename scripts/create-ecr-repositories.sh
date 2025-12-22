#!/bin/bash
# Script to create ECR repositories based on lambda-ecr-mapping.txt
# This script reads the mapping file and creates all ECR repositories

set -e

# Configuration
MAPPING_FILE=".github/lambda-ecr-mapping.txt"
AWS_REGION="${AWS_REGION:-us-east-1}"
ENABLE_SCAN_ON_PUSH="${ENABLE_SCAN_ON_PUSH:-true}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "ECR Repository Creation Script"
echo "=========================================="
echo "Region: $AWS_REGION"
echo "Mapping File: $MAPPING_FILE"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}ERROR: AWS CLI is not installed${NC}"
    echo "Please install AWS CLI: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if mapping file exists
if [ ! -f "$MAPPING_FILE" ]; then
    echo -e "${RED}ERROR: Mapping file not found: $MAPPING_FILE${NC}"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}ERROR: AWS credentials not configured${NC}"
    echo "Please configure AWS credentials using:"
    echo "  aws configure"
    echo "  OR"
    echo "  export AWS_ACCESS_KEY_ID=..."
    echo "  export AWS_SECRET_ACCESS_KEY=..."
    exit 1
fi

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}AWS Account ID: $AWS_ACCOUNT_ID${NC}"
echo ""

# Function to create ECR repository
create_ecr_repo() {
    local repo_name=$1
    local region=$2
    
    echo -n "Creating repository: $repo_name ... "
    
    # Check if repository already exists
    if aws ecr describe-repositories --repository-names "$repo_name" --region "$region" &> /dev/null; then
        echo -e "${YELLOW}Already exists${NC}"
        return 0
    fi
    
    # Create repository
    if aws ecr create-repository \
        --repository-name "$repo_name" \
        --region "$region" \
        --image-scanning-configuration scanOnPush=$ENABLE_SCAN_ON_PUSH \
        --encryption-configuration encryptionType=AES256 \
        &> /dev/null; then
        echo -e "${GREEN}✓ Created${NC}"
        
        # Get repository URI
        REPO_URI=$(aws ecr describe-repositories \
            --repository-names "$repo_name" \
            --region "$region" \
            --query 'repositories[0].repositoryUri' \
            --output text)
        echo "  Repository URI: $REPO_URI"
        return 0
    else
        echo -e "${RED}✗ Failed${NC}"
        return 1
    fi
}

# Read mapping file and create repositories
SUCCESS_COUNT=0
FAILED_COUNT=0
FAILED_REPOS=()

echo "Reading ECR repository mappings..."
echo ""

while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue
    
    # Parse mapping: folder:repo-name
    if [[ "$line" =~ ^([^:]+):(.+)$ ]]; then
        FOLDER_NAME="${BASH_REMATCH[1]}"
        REPO_NAME="${BASH_REMATCH[2]// /}"  # Remove spaces
        
        if [ -n "$REPO_NAME" ]; then
            if create_ecr_repo "$REPO_NAME" "$AWS_REGION"; then
                ((SUCCESS_COUNT++))
            else
                ((FAILED_COUNT++))
                FAILED_REPOS+=("$REPO_NAME")
            fi
            echo ""
        fi
    fi
done < "$MAPPING_FILE"

# Summary
echo "=========================================="
echo "Summary"
echo "=========================================="
echo -e "${GREEN}Successfully created/exists: $SUCCESS_COUNT${NC}"
if [ $FAILED_COUNT -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_COUNT${NC}"
    echo "Failed repositories:"
    for repo in "${FAILED_REPOS[@]}"; do
        echo "  - $repo"
    done
else
    echo -e "${GREEN}All repositories ready!${NC}"
fi
echo ""

# Display all repository URIs
echo "=========================================="
echo "ECR Repository URIs"
echo "=========================================="
while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue
    
    if [[ "$line" =~ ^([^:]+):(.+)$ ]]; then
        REPO_NAME="${BASH_REMATCH[2]// /}"
        if [ -n "$REPO_NAME" ]; then
            REPO_URI=$(aws ecr describe-repositories \
                --repository-names "$REPO_NAME" \
                --region "$AWS_REGION" \
                --query 'repositories[0].repositoryUri' \
                --output text 2>/dev/null || echo "Not found")
            echo "$REPO_NAME: $REPO_URI"
        fi
    fi
done < "$MAPPING_FILE"

echo ""
echo "=========================================="
echo "Next Steps:"
echo "1. Verify repositories in AWS Console:"
echo "   https://console.aws.amazon.com/ecr/repositories?region=$AWS_REGION"
echo "2. Configure GitHub Secrets with AWS credentials"
echo "3. Test the workflow by pushing code changes"
echo "=========================================="

