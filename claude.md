# CLAUDE.md - Project Navigation Hub

## Quick Start
- **First time?** Read `claude_config/README.md`
- **Starting work?** Check `claude_config/claude_config/checklists/session_start.md`
- **Project details?** See `claude_config/claude_config/project/details.md`
- **Version:** See `claude_config/claude_config/VERSION.md`

## Project: Clinical Database Collaborative Analysis Repository
- **Purpose:** Help clinical researchers collaborate on NSQIP and NCDB data analysis
- **Status:** Active development
- **Last Updated:** 2025-01-21

## Recent Updates (2025-01-21):
- ✅ Created marimo expert agent for notebook best practices
- ✅ Developed three optimized analysis templates:
  - Adult NSQIP (`nsqip_analysis.py`)
  - Pediatric NSQIP (`pnsqip_analysis.py`)
  - NCDB cancer data (`ncdb_analysis.py`)
- ✅ Simplified workflow - removed quickstart.py and setup scripts
- ✅ Updated documentation for manual project creation
- ✅ All templates now include interactive UI components
- ✅ Added .env configuration for data paths

## Workflow Summary:
1. **Clone repository**: `git clone` → `cd clinical-db-analysis`
2. **Create project**: `mkdir projects/name` → copy template
3. **Start analyzing**: `uv run marimo edit --sandbox projects/name/analysis.py`

## Key Features:
- **Marimo notebooks**: Interactive, reactive Python notebooks
- **Sandboxed execution**: Clean environment via `uv run marimo --sandbox`
- **Three templates**: Adult NSQIP, Pediatric NSQIP, NCDB
- **Simplified workflow**: Direct uv commands, no custom scripts
- **No data sharing**: Users provide their own data paths

For full navigation and details, see `claude_config/README.md`
