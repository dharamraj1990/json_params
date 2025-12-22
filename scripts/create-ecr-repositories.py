#!/usr/bin/env python3
"""
Python script to create ECR repositories based on lambda-ecr-mapping.txt
This script reads the mapping file and creates all ECR repositories
"""

import boto3
import sys
import os
from pathlib import Path

# Configuration
MAPPING_FILE = Path(".github/lambda-ecr-mapping.txt")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
ENABLE_SCAN_ON_PUSH = os.environ.get("ENABLE_SCAN_ON_PUSH", "true").lower() == "true"


def parse_mapping_file(mapping_file):
    """Parse the ECR mapping file and return list of (folder, repo_name) tuples."""
    mappings = []
    
    if not mapping_file.exists():
        print(f"ERROR: Mapping file not found: {mapping_file}")
        sys.exit(1)
    
    with open(mapping_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse mapping: folder:repo-name
            if ':' in line:
                parts = line.split(':', 1)
                folder = parts[0].strip()
                repo_name = parts[1].strip()
                if folder and repo_name:
                    mappings.append((folder, repo_name))
    
    return mappings


def create_ecr_repository(ecr_client, repo_name, region):
    """Create an ECR repository if it doesn't exist."""
    try:
        # Check if repository already exists
        try:
            response = ecr_client.describe_repositories(
                repositoryNames=[repo_name]
            )
            repo_uri = response['repositories'][0]['repositoryUri']
            print(f"  ✓ Repository '{repo_name}' already exists")
            print(f"    URI: {repo_uri}")
            return True, repo_uri
        except ecr_client.exceptions.RepositoryNotFoundException:
            pass
        
        # Create repository
        response = ecr_client.create_repository(
            repositoryName=repo_name,
            imageScanningConfiguration={
                'scanOnPush': ENABLE_SCAN_ON_PUSH
            },
            encryptionConfiguration={
                'encryptionType': 'AES256'
            }
        )
        
        repo_uri = response['repository']['repositoryUri']
        print(f"  ✓ Created repository '{repo_name}'")
        print(f"    URI: {repo_uri}")
        return True, repo_uri
        
    except Exception as e:
        print(f"  ✗ Failed to create repository '{repo_name}': {str(e)}")
        return False, None


def main():
    print("=" * 50)
    print("ECR Repository Creation Script")
    print("=" * 50)
    print(f"Region: {AWS_REGION}")
    print(f"Mapping File: {MAPPING_FILE}")
    print()
    
    # Check AWS credentials
    try:
        sts_client = boto3.client('sts', region_name=AWS_REGION)
        identity = sts_client.get_caller_identity()
        account_id = identity['Account']
        print(f"✓ AWS Account ID: {account_id}")
        print()
    except Exception as e:
        print(f"ERROR: AWS credentials not configured: {str(e)}")
        print("Please configure AWS credentials using:")
        print("  aws configure")
        print("  OR")
        print("  export AWS_ACCESS_KEY_ID=...")
        print("  export AWS_SECRET_ACCESS_KEY=...")
        sys.exit(1)
    
    # Parse mapping file
    mappings = parse_mapping_file(MAPPING_FILE)
    
    if not mappings:
        print("No repository mappings found in mapping file")
        sys.exit(1)
    
    print(f"Found {len(mappings)} repository mappings")
    print()
    
    # Create ECR client
    ecr_client = boto3.client('ecr', region_name=AWS_REGION)
    
    # Create repositories
    success_count = 0
    failed_count = 0
    failed_repos = []
    repo_uris = {}
    
    for folder, repo_name in mappings:
        print(f"Processing: {folder} -> {repo_name}")
        success, repo_uri = create_ecr_repository(ecr_client, repo_name, AWS_REGION)
        
        if success:
            success_count += 1
            repo_uris[repo_name] = repo_uri
        else:
            failed_count += 1
            failed_repos.append(repo_name)
        print()
    
    # Summary
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    print(f"✓ Successfully created/exists: {success_count}")
    if failed_count > 0:
        print(f"✗ Failed: {failed_count}")
        print("Failed repositories:")
        for repo in failed_repos:
            print(f"  - {repo}")
    else:
        print("✓ All repositories ready!")
    print()
    
    # Display all repository URIs
    print("=" * 50)
    print("ECR Repository URIs")
    print("=" * 50)
    for repo_name, repo_uri in sorted(repo_uris.items()):
        print(f"{repo_name}: {repo_uri}")
    
    print()
    print("=" * 50)
    print("Next Steps:")
    print(f"1. Verify repositories in AWS Console:")
    print(f"   https://console.aws.amazon.com/ecr/repositories?region={AWS_REGION}")
    print("2. Configure GitHub Secrets with AWS credentials")
    print("3. Test the workflow by pushing code changes")
    print("=" * 50)


if __name__ == "__main__":
    main()

