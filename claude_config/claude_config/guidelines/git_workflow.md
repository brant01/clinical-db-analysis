# Git Workflow Guidelines

## Repository Setup

### Essential .gitignore
```gitignore
# Environment
.env
*.env

# Python
__pycache__/
venv/
*.pyc

# Data - CRITICAL
data/
*.csv
*.xlsx
*.parquet
*.db

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Project specific
logs/
results/
models/
```

## Branch Strategy
- `main` - Production ready
- `develop` - Integration branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `release/*` - Release prep

## Commit Standards

### Format
`type(scope): brief description`

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **refactor**: Code restructure
- **test**: Test changes
- **perf**: Performance
- **chore**: Maintenance

### Rules
- Present tense
- Under 50 chars
- No period at end
- Reference issues
- NO Claude/AI co-authorship mentions
- NO "Generated with" references

## Pre-commit Checks
- [ ] No sensitive data
- [ ] Tests passing
- [ ] Code formatted
- [ ] No debug code
- [ ] Documentation updated

## Code Review
- Check security first
- Verify logic
- Ensure tests exist
- Review performance
- Check style consistency

## Emergency Procedures

### Accidental PHI Commit
1. DO NOT PUSH
2. If pushed:
   - Notify immediately
   - Document exposure
   - Remove from history
   - Rotate any secrets

### Recovery Commands
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Find lost commits
git reflog

# Remove file from history
git filter-branch --index-filter 'git rm --cached --ignore-unmatch FILE'
```