# GitHub Workflows Explanation

## Active Workflow

### `lambda-build-push.yml` (Main Workflow)
**Status:** ✅ Active and working

**Features:**
- Uses **bash scripts** for change detection (lightweight, fast)
- Has **path filters** to only trigger on `lambda-functions/**` changes
- Supports **both IAM role and access keys** (currently configured for access keys)
- Uses modern `$GITHUB_OUTPUT` syntax (no deprecation warnings)
- Includes comprehensive debugging and error handling
- Fixed JSON output formatting issues
- Proper job output naming

**Use this workflow** - It's the production-ready version with all fixes applied.

## Workflow Features

The single workflow (`lambda-build-push.yml`) includes:

