# Claude Configuration System

## Purpose
This configuration system guides Claude in understanding project context, maintaining standards, and providing expert-level guidance across different domains.

## Structure Overview

### Core Components (Protected - Do Not Edit)
- `core/` - Fundamental principles and version tracking
- `guidelines/` - Technical standards and workflows
- `experts/` - Specialized knowledge bases

### Project Components (Editable)
- `project/` - Project-specific information and logs
- Custom configurations as needed

### Workflow Tools
- `checklists/` - Step-by-step guides for common tasks

## How Claude Should Use This

### Session Start
1. Read `CLAUDE.md` for current status
2. Check `project/log.md` for recent changes
3. Review relevant checklists

### During Development
1. Consult appropriate experts for specialized tasks
2. Follow guidelines for code standards
3. Update project log with decisions

### Session End
1. Update `project/log.md`
2. Update status in main `CLAUDE.md`
3. Note any unresolved issues

## For Humans
- Keep `project/` files updated
- Don't modify `core/` files
- Propose new experts in `experts/proposed/`
- Version updates come from project management tool