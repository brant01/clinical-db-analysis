# Claude Config Version

**TEMPLATE_VERSION:** 2.2.0  
**LAST_UPDATED:** 2025-01-21  
**COMPATIBLE_WITH:** pm_tool_v1.5+

## Version Check
If this version differs from your project management tool:
1. Check `claude_config/core/version_info.md` for changes
2. Alert user about available updates
3. Review migration requirements

## Changes in 2.2.0
- Simplified workflow: removed quickstart.py and setup scripts
- Added marimo expert agent for notebook best practices
- Created three specialized templates (NSQIP, P-NSQIP, NCDB)
- All templates now include interactive UI components
- Updated documentation for manual project creation
- Improved template structure with consistent patterns

## Changes in 2.1.0
- Added cross-platform .env support with @REMOTE_DRIVE@ placeholder
- Automatic path conversion for Mac/WSL/Linux environments
- Enhanced .env templates with platform examples

## Breaking Changes in 2.0.0
- Restructured from single file to modular system
- Added expert agents system
- Enhanced data safety guidelines
- Separated protected vs editable content

## Quick Version History
- **2.2.0** - Simplified workflow, marimo templates
- **2.1.0** - Cross-platform .env support
- **2.0.0** - Modular system with experts
- **1.0.0** - Original single-file template

For full history: `claude_config/core/version_info.md`