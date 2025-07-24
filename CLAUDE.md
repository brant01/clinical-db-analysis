# CLAUDE.md - Project Navigation Hub

## 🚨 SESSION START CHECKLIST
1. **Check directory name**: Should be `clinical-db-analysis` (not NSQIP-analysis)
2. **If wrong name**: Exit and run `mv NSQIP-analysis clinical-db-analysis`
3. **Then continue** with normal workflow

## Quick Start
- **First time?** Read `claude_config/README.md`
- **Starting work?** Check `claude_config/checklists/session_start.md`
- **Project details?** See `claude_config/project/details.md`
- **Version:** See `claude_config/VERSION.md`

## Project: Clinical Database Collaborative Analysis Repository
- **Purpose:** Help clinical researchers collaborate on NSQIP and NCDB data analysis
- **Status:** Active development
- **Last Updated:** 2025-06-07

## Recent Accomplishments (2025-07-16):
- ✅ Successfully renamed directory from NSQIP-analysis to clinical-db-analysis
- ✅ Simplified workflow by removing custom wrapper scripts
- ✅ Updated all documentation to use `uv run marimo edit --sandbox`
- ✅ Removed db_helper.py, db, and db.bat files
- ✅ Updated README with cleaner getting started instructions
- ✅ Fixed template comments to reference new workflow

## Current Issues (2025-07-24):

### nsqip_tools Issues
- **Bug in filter_by_cpt()**: Empty column name reference causes `ColumnNotFoundError: unable to find column ""`
- **Version inconsistency**: nsqip_tools 0.2.2 published but uv still resolves to 0.1.0
- **Workaround**: Use direct polars approach with `pl.scan_parquet()` instead of nsqip_tools

### Parquet Schema Issues
- **Schema mismatches**: Different years have inconsistent column types (Float32 vs Float64)
- **Invalid data**: Empty strings `" "` in numeric columns prevent type conversion
- **Impact**: Cannot use `pl.scan_parquet("*.parquet")` directly across all years
- **Current workaround**: Manual schema unification with data cleaning

### Suggested Solutions
1. **nsqip_tools**: Update filter_by_cpt to properly handle LazyFrame column access
2. **Parquet files**: Standardize schema across all years and clean invalid data during creation
3. **Alternative**: Consider direct polars approach as primary method

## Notes:
- Users now use standard `uv run marimo edit --sandbox` commands directly
- No more custom scripts or platform-specific instructions
- Workflow is now transparent and uses standard Python tooling
- All templates work with the new simplified approach
- **Temporary**: Use direct polars loading for multi-year NSQIP data

For full navigation and details, see `claude_config/README.md`
