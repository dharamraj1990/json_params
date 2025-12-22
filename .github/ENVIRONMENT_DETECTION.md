# Environment Detection in GitHub Actions

## Current Behavior

Currently, the workflow deploys to **all three environments** (dev, staging, production) on every push:
- **dev**: Automatic deployment (no approval)
- **staging**: Requires manual approval
- **production**: Requires manual approval

## How GitHub Environments Work

The `environment:` keyword in GitHub Actions:
1. **Links to GitHub Environments** (Settings → Environments)
2. **Enforces protection rules** (approvals, wait timers, etc.)
3. **Does NOT automatically detect** which environment to deploy to

## Current Setup

```yaml
deploy-dev:
  environment:
    name: dev  # Links to GitHub "dev" environment

deploy-staging:
  environment:
    name: staging  # Links to GitHub "staging" environment (with approval)

deploy-prod:
  environment:
    name: production  # Links to GitHub "production" environment (with approval)
```

## Option 1: Branch-Based Deployment (Recommended)

Deploy based on branch:
- `develop` branch → Deploy to **dev only**
- `main` branch → Deploy to **staging and production** (with approvals)

## Option 2: Manual Selection

Use workflow inputs to manually select environment.

## Option 3: Keep Current (All Environments)

Deploy to all environments every time (current behavior).

