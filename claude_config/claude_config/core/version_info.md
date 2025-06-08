# Version History & Migration Guide

## Version 2.0.0 (2025-01-15)

### Overview
Major restructuring from monolithic to modular system with expert agents.

### Breaking Changes
1. **File Structure**: Single `CLAUDE.md` → modular `claude_config/`
2. **Expert System**: New concept requiring consultation workflow
3. **Version Tracking**: Formal version management system
4. **Protected Content**: Clear separation of editable vs protected

### New Features
- Expert agent system for specialized guidance
- Modular file organization
- Enhanced data safety guidelines
- Version compatibility checking
- Project-specific customization support

### Migration Steps
1. **Backup existing CLAUDE.md**
2. **Create new structure**:
   ```bash
   mkdir -p claude_config/{core,project,guidelines,checklists,experts/{core_experts,domain_experts,proposed}}
   ```
3. **Move content to appropriate modules**
4. **Update project management tool** to version 1.5+
5. **Add project-specific configuration**

### Compatibility Notes
- Requires pm_tool v1.5 or higher
- Not backward compatible with v1.0 parsers
- Expert consultation is optional but recommended

## Version 1.0.0 (2025-01-03)

### Overview
Initial template version with single-file configuration.

### Features
- Basic project structure
- Core principles
- Git workflow
- Session tracking
- Simple checklists

### Limitations (addressed in v2.0)
- Monolithic file structure
- No specialized domain guidance
- Limited customization options
- No version tracking