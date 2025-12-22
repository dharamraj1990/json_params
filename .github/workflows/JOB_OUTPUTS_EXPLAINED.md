# How Job Outputs Work in GitHub Actions

## Overview

Lines 23-25 in `lambda-build-push.yml` define **job outputs** that pass data from one job to another in the workflow.

```yaml
outputs:
  folders: ${{ steps.changes.outputs.folders }}
  folders-json: ${{ steps.changes.outputs.folders-json }}
```

## The Flow: Step → Job → Next Job

### Step 1: Step Outputs (Lines 103, 113, 126)

In the `Detect changed folders` step (id: `changes`), we write outputs to `$GITHUB_OUTPUT`:

```bash
# Step writes outputs
echo "folders=$EXISTING_FOLDERS" >> $GITHUB_OUTPUT
echo "folders-json=$JSON_FOLDERS" >> $GITHUB_OUTPUT
```

This creates **step outputs** accessible as:
- `${{ steps.changes.outputs.folders }}`
- `${{ steps.changes.outputs.folders-json }}`

### Step 2: Job Outputs (Lines 23-25)

The job takes step outputs and makes them available to **other jobs**:

```yaml
outputs:
  folders: ${{ steps.changes.outputs.folders }}
  folders-json: ${{ steps.changes.outputs.folders-json }}
```

This creates **job outputs** accessible as:
- `${{ needs.detect-changes.outputs.folders }}`
- `${{ needs.detect-changes.outputs.folders-json }}`

### Step 3: Using Job Outputs in Next Job (Line 144, 148)

The `build-and-push` job uses these outputs:

```yaml
build-and-push:
  needs: detect-changes  # Wait for detect-changes job to complete
  if: needs.detect-changes.outputs.folders != ''  # Condition check
  strategy:
    matrix:
      folder: ${{ fromJson(needs.detect-changes.outputs.folders-json) }}  # Use JSON output
```

## Visual Flow Diagram

```
┌─────────────────────────────────────┐
│  detect-changes Job                 │
│                                     │
│  Step: Detect changed folders      │
│  (id: changes)                      │
│                                     │
│  Writes to $GITHUB_OUTPUT:         │
│  ├─ folders="lambda-function-1"    │
│  └─ folders-json='["lambda-..."]' │
│                                     │
│  Job Outputs (lines 23-25):        │
│  ├─ folders: ${{ steps.changes... }}│
│  └─ folders-json: ${{ steps... }}  │
└─────────────────────────────────────┘
              │
              │ Passes outputs
              ▼
┌─────────────────────────────────────┐
│  build-and-push Job                  │
│                                     │
│  Uses outputs via:                  │
│  needs.detect-changes.outputs.*    │
│                                     │
│  - Condition check                  │
│  - Matrix strategy                  │
│  - Build Docker images              │
└─────────────────────────────────────┘
```

## Why This Pattern?

### Problem
- Jobs run in parallel or sequentially
- Each job has its own isolated environment
- Data doesn't automatically transfer between jobs

### Solution
- **Step outputs**: Share data within a job
- **Job outputs**: Share data between jobs
- **needs**: Define job dependencies

## Example Values

When `lambda-function-1` is changed:

**Step outputs:**
```yaml
steps.changes.outputs.folders = "lambda-function-1"
steps.changes.outputs.folders-json = '["lambda-function-1"]'
```

**Job outputs:**
```yaml
needs.detect-changes.outputs.folders = "lambda-function-1"
needs.detect-changes.outputs.folders-json = '["lambda-function-1"]'
```

**Used in build job:**
```yaml
# Condition check
if: needs.detect-changes.outputs.folders != ''  # "lambda-function-1" != '' → true

# Matrix strategy (creates parallel jobs)
matrix:
  folder: ${{ fromJson(needs.detect-changes.outputs.folders-json) }}
  # fromJson('["lambda-function-1"]') → ["lambda-function-1"]
  # Creates one matrix job with folder="lambda-function-1"
```

## Key Points

1. **Step outputs** (`steps.*.outputs.*`) are only available within the same job
2. **Job outputs** (`needs.*.outputs.*`) make data available to dependent jobs
3. The `needs` keyword creates a dependency and allows access to outputs
4. Job outputs must reference step outputs (can't create new values directly)
5. Outputs are strings, so JSON needs `fromJson()` to parse

## Real Example from Workflow

```yaml
# Job 1: detect-changes
jobs:
  detect-changes:
    outputs:
      folders: ${{ steps.changes.outputs.folders }}  # "lambda-function-1"
      folders-json: ${{ steps.changes.outputs.folders-json }}  # '["lambda-function-1"]'
    steps:
      - id: changes
        run: |
          echo "folders=lambda-function-1" >> $GITHUB_OUTPUT
          echo "folders-json=[\"lambda-function-1\"]" >> $GITHUB_OUTPUT

# Job 2: build-and-push (depends on detect-changes)
  build-and-push:
    needs: detect-changes  # Wait for detect-changes to finish
    if: needs.detect-changes.outputs.folders != ''  # Check if any folders changed
    strategy:
      matrix:
        folder: ${{ fromJson(needs.detect-changes.outputs.folders-json) }}
        # Creates: folder="lambda-function-1"
        # This runs the build job once for each folder
```

## Summary

Lines 23-25 create a **bridge** that:
1. Takes step outputs from the `changes` step
2. Makes them available as job-level outputs
3. Allows the `build-and-push` job to access them via `needs.detect-changes.outputs.*`

This enables the workflow to:
- Detect which Lambda functions changed
- Pass that information to the build job
- Build only the changed functions in parallel

