# Communication Rules - PROTECTED

## Code Communication

### Comments & Documentation
- **Purpose over mechanics** - Explain WHY, not WHAT
- **No decorative elements** - No ASCII art, emojis, or symbols
- **Professional tone** - Technical, clear, direct

### Git Commits
- **Format:** `type: brief description`
- **Types:** feat, fix, docs, refactor, test, perf
- **NO** co-authored-by tags
- **NO** emoji in commit messages
- **Reference** issues when applicable

Examples:
```
feat: add patient cohort filtering by diagnosis
fix: handle missing audiometry data gracefully
docs: update IRB protocol references
refactor: extract statistical tests to separate module
```

### Function/Variable Naming
- **Descriptive** over brief (within reason)
- **Domain-appropriate** terminology
- **Consistent** with project conventions

### Error Messages
- **Actionable** - Tell user what to do
- **Specific** - Include relevant details
- **Professional** - No casual language

### Documentation Standards
- Docstrings for all public functions
- Type hints everywhere (Python)
- Examples for complex functions
- Link to relevant papers/protocols