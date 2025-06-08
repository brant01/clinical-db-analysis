# Coding Standards

## General Principles
1. **Readability First** - Code is read more than written
2. **Consistent Style** - Follow project conventions
3. **Self-Documenting** - Clear names and structure
4. **Test Coverage** - Aim for >80% coverage
5. **Type Safety** - Use type hints/strong typing

## Python Standards
- Follow PEP 8 with Black formatter (88 char lines)
- Type hints where helpful but not required
- Comprehensive docstrings with examples
- **ALWAYS use polars for dataframes (NEVER pandas)**
- Prefer pathlib over os.path
- Use marimo for notebooks (not Jupyter)
- Import nsqip_tools or ncdb_tools for data loading
- Avoid advanced Python patterns - write for beginners
- Explicit is better than clever

## Package Management
- **Always use uv for package management**
  ```bash
  uv add [package]      # Add new package
  uv run [command]      # Run commands
  ```

## Running Notebooks
- **ALWAYS use the helper script (ensures sandbox mode)**
  ```bash
  ./db edit notebook.py    # Mac/Linux
  db.bat edit notebook.py  # Windows
  ```

## Helper Function Requirements
When adding new helper functions:
- Must support both DataFrame and LazyFrame
- Must auto-detect adult vs pediatric datasets when relevant
- Include comprehensive docstrings with examples
- Test with actual clinical data
- Place in `shared/utils/` directory

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
- **Use LazyFrames when possible for large data**
  ```python
  # Exploration with LazyFrame
  import polars as pl
  df = pl.scan_parquet("/path/to/data/*.parquet")
  print(df.columns)
  sample = df.head(100).collect()
  ```

## Documentation Requirements
- Explain why, not what
- Include examples for complex functions
- Document assumptions and constraints
- Link to relevant papers/standards
- Keep docs in sync with code