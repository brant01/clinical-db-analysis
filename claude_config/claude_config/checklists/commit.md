# Commit Checklist

## Code Quality
- [ ] Follows style guide
- [ ] No commented code
- [ ] No debug prints
- [ ] TODOs have tickets
- [ ] Functions documented

## Security
- [ ] No hardcoded secrets
- [ ] No PHI/PII
- [ ] No absolute paths
- [ ] Input validated
- [ ] Queries parameterized

## Testing
- [ ] Tests written
- [ ] Tests passing
- [ ] Edge cases covered
- [ ] Errors handled

## Documentation
- [ ] Docstrings updated
- [ ] README current
- [ ] Complex logic explained

## Git
- [ ] Changes reviewed
- [ ] Commit message formatted
- [ ] Related changes only
- [ ] Issue referenced
- [ ] NO Claude or AI co-authorship mentions

## Final Commands
```bash
# Format & lint
black src/
pytest

# Check secrets
git diff --staged | grep -E "(password|key|token)"
```