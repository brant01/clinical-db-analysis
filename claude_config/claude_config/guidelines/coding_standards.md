# Coding Standards

## General Principles
1. **Readability First** - Code is read more than written
2. **Consistent Style** - Follow project conventions
3. **Self-Documenting** - Clear names and structure
4. **Test Coverage** - Aim for >80% coverage
5. **Type Safety** - Use type hints/strong typing

## Python Standards
- Follow PEP 8 with Black formatter (88 char lines)
- Type hints on all functions
- Comprehensive docstrings
- Use polars for dataframes (never pandas)
- Prefer pathlib over os.path

## Rust Standards
- Follow official Rust style guide
- Use `cargo fmt` and `cargo clippy`
- Document public APIs
- Prefer Result<T, E> for error handling
- Use thiserror for error types

## Code Organization
- One concept per file
- Group related functionality in modules
- Clear public/private boundaries
- Dependency injection over hard-coding

## Testing Standards
- Unit tests for all public functions
- Integration tests for workflows
- Use fixtures for test data
- Mock external dependencies
- Test edge cases and errors

## Performance Guidelines
- Profile before optimizing
- Document performance requirements
- Use appropriate data structures
- Consider memory usage
- Benchmark critical paths

## Documentation Requirements
- Explain why, not what
- Include examples for complex functions
- Document assumptions and constraints
- Link to relevant papers/standards
- Keep docs in sync with code