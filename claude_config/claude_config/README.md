# Claude Configuration System

## Purpose
This configuration system guides Claude in understanding the clinical database analysis project, maintaining standards, and providing expert-level guidance for medical research and marimo notebook development.

## Structure Overview

### Core Components (Protected - Do Not Edit)
- `core/` - Fundamental principles and version tracking
- `guidelines/` - Technical standards and workflows
- `experts/` - Specialized knowledge bases including new marimo expert

### Project Components (Editable)
- `project/` - Clinical database project details and architecture
- Custom configurations for medical research

### Workflow Tools
- `checklists/` - Updated guides for simplified workflow

## How Claude Should Use This

### Session Start
1. Read `CLAUDE.md` for current project status
2. Check `checklists/session_start.md` for workflow
3. Review template options (NSQIP, P-NSQIP, NCDB)

### During Development
1. Consult marimo expert for notebook best practices
2. Use medical research expert for clinical guidance
3. Follow data handling guidelines for PHI protection
4. Update project log with significant changes

### For Template Work
1. Review marimo expert guidance
2. Ensure interactive UI components
3. Follow reactive programming patterns
4. Test with sample data paths

## Key Updates in v2.2.0
- Simplified workflow (no quickstart.py)
- Three specialized templates with interactive UI
- Marimo expert agent added
- Manual project creation process
- Updated checklists for new workflow

## For Humans
- Templates are in `shared/templates/`
- Create projects manually in `projects/`
- Use `./db edit` to run notebooks
- Keep data paths local to your system