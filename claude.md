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

## Recent Accomplishments (2025-06-07):
- ✅ Successfully renamed directory from NSQIP-analysis to clinical-db-analysis
- ✅ Created unified `db` wrapper scripts (Unix and Windows)
- ✅ Removed old scripts (nsqip, clinical-db)
- ✅ Updated all documentation to reference `./db`
- ✅ Tested wrapper scripts - working correctly
- ✅ Fixed quickstart.py Path.ctime() error

## Notes:
- The `db_helper.py` file contains all the logic for the wrapper scripts
- Both Unix (`db`) and Windows (`db.bat`) wrappers simply call this Python helper
- The system is now consistent with the new `./db` command across all documentation

For full navigation and details, see `claude_config/README.md`
