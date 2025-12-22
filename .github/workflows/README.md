# GitHub Workflows Explanation

## Current Workflows

### 1. `lambda-build-push.yml` (Main - Active)
**Status:** ✅ Currently active and working

**Features:**
- Uses **bash scripts** for change detection (lightweight, fast)
- Has **path filters** to only trigger on `lambda-functions/**` changes
- Supports **both IAM role and access keys** (currently configured for access keys)
- Uses modern `$GITHUB_OUTPUT` syntax (no deprecation warnings)
- Includes comprehensive debugging and error handling
- Fixed JSON output formatting issues
- Proper job output naming

**Use this workflow** - It's the production-ready version with all fixes applied.

### 2. `alternative-workflow.yml` (Alternative - Reference)
**Status:** ⚠️ Not recommended - has issues

**Original Purpose:**
- Alternative implementation using **Python** for change detection
- Meant to be more robust for complex scenarios
- Includes `workflow_dispatch` for manual triggering

**Issues:**
- ❌ Uses **deprecated `::set-output` syntax** (will break in future)
- ❌ Has **output name mismatch** (`changed-folders` vs `folders`)
- ❌ Only configured for **IAM role** (not access keys)
- ❌ Missing recent fixes and improvements
- ❌ No path filters (triggers on all pushes)

## Recommendation

**Delete the alternative workflow** since:
1. The main workflow is working and has all fixes
2. The alternative has deprecated syntax that will break
3. Having two workflows can cause confusion
4. The main workflow can be enhanced with manual trigger if needed

## If You Want to Keep Both

If you want to keep the alternative workflow for reference or future use:

1. **Update it** to match the main workflow:
   - Fix deprecated `::set-output` → use `$GITHUB_OUTPUT`
   - Fix output names (`changed-folders` → `folders`)
   - Add access key support
   - Add path filters
   - Apply all fixes from main workflow

2. **Disable it** by removing triggers or renaming to `.yml.disabled`

3. **Use different triggers** - e.g., only manual trigger for alternative

## Quick Comparison

| Feature | Main Workflow | Alternative Workflow |
|---------|--------------|---------------------|
| Change Detection | Bash scripts | Python script |
| Path Filters | ✅ Yes | ❌ No |
| Manual Trigger | ❌ No | ✅ Yes |
| IAM Role Support | ✅ Yes | ✅ Yes |
| Access Keys Support | ✅ Yes | ❌ No |
| Modern Syntax | ✅ Yes | ❌ No (deprecated) |
| Debugging | ✅ Comprehensive | ⚠️ Basic |
| Status | ✅ Active & Working | ⚠️ Needs Updates |

## Action Items

1. **Use `lambda-build-push.yml`** as your main workflow
2. **Delete `alternative-workflow.yml`** (or rename to `.disabled` if you want to keep for reference)
3. If you need manual triggering, we can add `workflow_dispatch` to the main workflow

