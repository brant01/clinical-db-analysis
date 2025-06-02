# NSQIP Repository Development Guidelines

## Critical Reminders

- **Always use Polars**, never pandas
- **No emojis** in any documentation or code
- **PHI Protection** is paramount - all data must be treated as containing PHI
- **Beginner-friendly** - assume users have minimal technical knowledge
- **Use the helper scripts** - `./nsqip edit` ensures sandbox mode

## Repository Principles

### 1. Simplicity First
- Clear, commented code that beginners can understand
- Avoid advanced Python patterns
- Explicit is better than clever
- Use the helper functions in `shared/utils/nsqip_helpers.py`

### 2. Data Security
- Never commit data files (handled by .gitignore)
- Data paths should be set in notebooks, not environment variables
- Each researcher manages their own data access
- Always use LazyFrames when possible for large data

### 3. Collaboration Patterns
- Researchers work in their own `projects/` folders
- Shared utilities go in `shared/utils/`
- Only repository maintainer modifies `shared/` resources
- Direct commits to main branch (no complex branching)

## Technical Standards

### Package Management
```bash
# Always use uv for package management
uv add [package]
uv run [command]
```

### Running Notebooks
```bash
# Always use the helper script (ensures sandbox mode)
./nsqip edit notebook.py    # Mac/Linux
nsqip.bat edit notebook.py  # Windows
```

### Code Style
- Polars for all data manipulation
- Type hints where helpful but not required
- Extensive comments explaining medical/statistical concepts
- Function names should be descriptive (e.g., `calculate_composite_ssi`)

### NSQIP Data Specifics
- Outcomes are text strings (e.g., "No Complication", "Pneumonia")
- Adult and pediatric datasets have different variable names
- Helper functions auto-detect dataset type using age columns
- Years may have different variable availability

## Adding New Features

### New Helper Functions
1. Add to `shared/utils/nsqip_helpers.py`
2. Must support both DataFrame and LazyFrame
3. Must auto-detect adult vs pediatric when relevant
4. Include comprehensive docstrings with examples
5. Test with actual NSQIP data

### New Templates
1. Copy existing template as starting point
2. Include extensive comments
3. Import helper utilities
4. Set clear data path variable for users to modify

### Documentation
1. Write for absolute beginners
2. Include examples for every concept
3. Explain medical/statistical terms
4. Keep it concise but complete

## Common Tasks

### Checking Data Structure
```python
# Use LazyFrame for exploration
import polars as pl
df = pl.scan_parquet("/path/to/data/*.parquet")
print(df.columns)
sample = df.head(100).collect()
```

### Working with Outcomes
```python
# Remember outcomes are text, not binary
# Example: checking for SSI
has_ssi = pl.col("SUPINFEC") != "No Complication"
```

### Dataset Detection
```python
from nsqip_helpers import detect_dataset_type
dataset_type = detect_dataset_type(df)  # Returns "adult" or "pediatric"
```

## Repository Maintenance

### Adding Collaborators
1. GitHub Settings → Manage access → Add people
2. Update README if needed
3. Ensure they run `quickstart.py` for setup

### Reviewing Contributions
- Check for PHI exposure risk
- Ensure Polars usage (not pandas)
- Verify beginner-friendly documentation
- Test with both adult and pediatric data if applicable

### Version Control
- Commit messages should be descriptive
- No co-author tags in commits
- Regular small commits preferred over large changes

## Remember

1. **Clinical relevance first** - statistical significance isn't always clinically meaningful
2. **Reproducibility is critical** - others must be able to replicate
3. **Document everything** - methods, assumptions, limitations  
4. **Security is not optional** - treat all data as PHI
5. **Support beginners** - this may be their first coding experience

When in doubt about implementation, prioritize clarity and safety over elegance or performance.