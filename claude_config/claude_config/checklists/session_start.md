# Session Start Checklist

## Environment Setup
- [ ] Navigate to project root: `cd clinical-db-analysis`
- [ ] Pull latest changes: `git pull`
- [ ] Check current branch: `git branch`
- [ ] Verify uv installed: `uv --version`

## Context Review
- [ ] Read `CLAUDE.md` for current status
- [ ] Check active projects: `ls projects/`
- [ ] Review recent commits: `git log --oneline -5`
- [ ] Note any incomplete analyses

## For New Analysis
- [ ] Create project folder: `mkdir projects/lastname-topic`
- [ ] Choose appropriate template:
  - **Adult NSQIP**: `nsqip_analysis.py` - General surgery
  - **Pediatric NSQIP**: `pnsqip_analysis.py` - Pediatric surgery
  - **NCDB**: `ncdb_analysis.py` - Cancer outcomes
- [ ] Copy template: `cp shared/templates/[template] projects/lastname-topic/analysis.py`
- [ ] Create project README

## For Continuing Work
- [ ] Navigate to your project folder
- [ ] Open notebook: `./db edit analysis.py`
- [ ] Verify data path is still valid
- [ ] Check previous results in `results/`

## Quick Checks
```bash
# Verify setup
uv --version
python --version

# Check projects
ls projects/

# Git status
git status

# View templates
ls shared/templates/
```

## Common Tasks
```bash
# Start new analysis
mkdir projects/smith-mortality
cp shared/templates/nsqip_analysis.py projects/smith-mortality/analysis.py
./db edit projects/smith-mortality/analysis.py

# Continue existing
./db edit projects/existing-project/analysis.py

# Save work
git add projects/my-project/
git commit -m "Updated analysis results"
git push
```

**Today's Focus:** [Fill after review]