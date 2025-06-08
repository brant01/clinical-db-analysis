# CLAUDE.md - Project Navigation Hub

## Quick Start
- **First time?** Read `claude_config/README.md`
- **Starting work?** Check `claude_config/checklists/session_start.md`
- **Project details?** See `claude_config/project/details.md`
- **Version:** See `claude_config/VERSION.md`

## Current Status
- **Active Task:** Ready for development
- **Last Updated:** 2025-06-07
- **Next Steps:** See `claude_config/project/log.md`

## Navigation by Purpose

### Project Information
- **What is this?** → `claude_config/project/details.md`
- **How is it built?** → `claude_config/project/architecture.md`
- **What's been done?** → `claude_config/project/log.md`

### How to Work
- **Starting session** → `claude_config/checklists/session_start.md`
- **Writing code** → `claude_config/checklists/before_coding.md`
- **Code standards** → `claude_config/guidelines/coding_standards.md`
- **Data handling** → `claude_config/guidelines/data_handling.md`

### Expert Consultation
- **Code quality** → `claude_config/experts/core_experts/software_engineer.md`
- **Medical research** → `claude_config/experts/domain_experts/medical_research.md`
- **ML/AI guidance** → `claude_config/experts/domain_experts/ml_ai_expert.md`
- **Data compliance** → `claude_config/experts/core_experts/data_compliance.md`
- **Claude usage** → `claude_config/experts/core_experts/claude_expert.md`

### Before Committing
- **Checklist** → `claude_config/checklists/commit.md`
- **Git workflow** → `claude_config/guidelines/git_workflow.md`

## Quick Commands

### Development
```bash
# Create new project
python3 quickstart.py

# Edit notebook (Mac/Linux)
./nsqip edit projects/your-name/analysis.py

# Edit notebook (Windows)
nsqip.bat edit projects\your-name\analysis.py

# Run notebook read-only
./nsqip run analysis.py
```

### Git Workflow
```bash
# Get latest changes
git pull

# Save your work
git add projects/your-project/
git commit -m "feat: add mortality analysis"
git push
```

### Testing
```bash
# Run linter (if configured)
ruff check .

# Type check
mypy shared/
```

## Remember
- Think first, code second (80/20 rule)
- Consult experts when needed
- Update log after each session