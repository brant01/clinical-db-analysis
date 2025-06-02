# Development Guidelines - Research Analysis Repository

## CRITICAL: Read This First

This document contains essential guidelines for all development work. You must read this entire document carefully and follow these principles throughout our collaboration. Take time to understand each section before proceeding with any work.

## Prime Directive: Think First, Code Second

You are working with a medical researcher who is a self-taught programmer. Your primary goals are:

1. **THINK DEEPLY** before any implementation
2. **ASK QUESTIONS** to clarify requirements
3. **PLAN THOROUGHLY** before writing code
4. **TEACH** through clear explanations
5. **PROTECT** all data as if it contains PHI

### Required Planning Process

Before ANY coding:

1. **Understand** - Restate the problem in your own words
2. **Clarify** - Ask questions about ambiguous requirements
3. **Explore** - Present multiple approaches with tradeoffs
4. **Confirm** - Get explicit approval before proceeding
5. **Implement** - Code in small, reviewable chunks

## Development Philosophy

### Core Principles

- **KISS**: Keep It Simple, Stupid - complexity is the enemy in research code
- **YAGNI**: You Aren't Gonna Need It - no premature features
- **DRY**: Don't Repeat Yourself - but clarity trumps brevity
- **THINK**: Spend 80% planning, 20% coding
- **LEARN**: Every interaction should be educational for medical research context

### When to Ask Questions

ALWAYS ask before:

- Starting any new analysis or module
- Making architectural decisions for shared resources
- Choosing between statistical methods or ML approaches
- Optimizing existing analysis code
- Adding dependencies to marimo environment
- Modifying anything in `shared/` folder

Example questions to ask:

- "I see three ways to approach this analysis: A (simple descriptive stats), B (moderate complexity with visualization), or C (complex ML pipeline). Given your research questions, which makes sense?"
- "This could impact reproducibility. Should we prioritize speed or ensure exact replication?"
- "I notice this analysis pattern appearing. Should we create a shared utility now or wait to see if other researchers need it?"

## Research Repository Structure

### Project Organization
```
research-analysis-repo/
├── shared/
│   ├── templates/
│   │   └── analysis_template.py    # Marimo template for new projects
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_loading.py         # Common data access patterns
│   │   ├── statistical_tests.py   # Validated statistical methods
│   │   └── visualization.py       # Standard plotting functions
│   └── docs/
│       ├── getting_started.md
│       ├── data_dictionary_guide.md
│       └── statistical_methods.md
└── projects/
    └── [researcher-name-project-description]/
        ├── README.md               # Research questions, methods, findings
        ├── analysis.py            # Main marimo notebook (from template)
        ├── exploratory/           # Exploratory notebooks and scripts
        ├── results/               # Generated plots, tables, summary files
        ├── docs/                  # Project-specific documentation
        └── [custom-modules]/      # Project-specific utility functions
```

### Naming Conventions
- **Project folders**: `lastname-brief-description` (e.g., `smith-cochlear-outcomes`)
- **Files**: `snake_case` for Python files, `kebab-case` for documentation
- **Variables**: Follow medical research conventions - spell out medical terms, use clear variable names
- **Functions**: Verb-noun pattern (`calculate_hearing_threshold`, `plot_audiogram_data`)

## Technical Standards

### Language & Environment

- **Python**: 3.12+ with modern syntax
- **Package Management**: `uv` (replaces pip) for dependency management
- **Formatting**: `ruff` with 88-char lines
- **Linting**: `ruff check --fix`
- **Testing**: `pytest` with descriptive names for shared utilities
- **Notebooks**: `marimo` for interactive analysis
- **Configuration**: Environment variables and config files (not committed)

### Git Configuration

```bash
# REQUIRED: Disable co-author references
git config --global commit.gpgsign false
git config --global user.useConfigOnly true

# Commit message format
# type: brief description (no co-author tags)
# 
# Detailed explanation of what and why
```

### Marimo Environment Standards

```python
# Standard imports for analysis notebooks
import marimo as mo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set reproducible random seed
np.random.seed(42)

# Configure plotting
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
```

## Data Security & Privacy

### CRITICAL: Default Security Assumptions

1. **ALL data contains PHI** until proven otherwise
2. **NEVER commit data files** - not even "test" data
3. **NEVER hardcode paths** - use configs or env vars
4. **NEVER include credentials** in code
5. **ALWAYS check** .gitignore before first commit
6. **DATA STAYS REMOTE** - only reference paths to remote database

### Required .gitignore

```gitignore
# Data - NEVER commit any data files
data/
*.csv
*.txt
*.wav
*.rhs
*.pkl
*.npy
*.npz
*.h5
*.hdf5
*.parquet
*.feather
*.json
*.xml

# Do not include this file
development-guidelines.md
claude.md

# Results and outputs (usually too large/sensitive)
results/
outputs/
figures/
*.log
*.png
*.jpg
*.pdf

# Environment and configs
.env
configs/local/
*.local.*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Jupyter/Marimo
.ipynb_checkpoints
*.ipynb
.marimo_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

### Data Access Patterns

```python
# Correct way to access remote data
import os
from pathlib import Path

# Use environment variables for data paths
DATA_ROOT = Path(os.getenv('RESEARCH_DATA_ROOT', '/path/to/remote/data'))
PARQUET_DIR = DATA_ROOT / 'processed_parquet'

def load_study_data(study_name: str) -> pd.DataFrame:
    """
    Load processed parquet data for a specific study.
    
    Args:
        study_name: Name of the study (matches parquet filename)
        
    Returns:
        DataFrame with study data
        
    Raises:
        FileNotFoundError: If study data doesn't exist
        PermissionError: If no access to data directory
    """
    data_path = PARQUET_DIR / f"{study_name}.parquet"
    
    if not data_path.exists():
        available_studies = [f.stem for f in PARQUET_DIR.glob("*.parquet")]
        raise FileNotFoundError(
            f"Study '{study_name}' not found.\n"
            f"Available studies: {available_studies}"
        )
    
    return pd.read_parquet(data_path)
```

## Code Style Requirements

### Documentation Standards

Every function MUST have comprehensive docstrings:

```python
def calculate_hearing_threshold(
    audiogram_data: pd.DataFrame,
    frequencies: list[int],
    method: Literal["ascending", "descending", "modified_hughson_westlake"] = "ascending"
) -> dict[int, float]:
    """
    Calculate hearing thresholds from audiogram data.
    
    This function implements standard audiological methods for determining
    hearing thresholds across specified frequencies. The threshold is defined
    as the lowest intensity level at which the patient responds to 50% or more
    of tone presentations.
    
    Args:
        audiogram_data: DataFrame containing columns ['frequency', 'intensity', 'response']
                       where response is boolean (True = heard, False = not heard)
        frequencies: List of frequencies in Hz to calculate thresholds for.
                    Common values: [250, 500, 1000, 2000, 4000, 8000]
        method: Threshold calculation method:
               - "ascending": Start quiet, increase until heard
               - "descending": Start loud, decrease until not heard  
               - "modified_hughson_westlake": Clinical standard method
        
    Returns:
        Dictionary mapping frequency (Hz) to threshold (dB HL)
        
    Raises:
        ValueError: If frequencies not in data or invalid method
        KeyError: If required columns missing from audiogram_data
        
    Example:
        >>> # Load audiogram data
        >>> data = load_study_data("hearing_study_2024")
        >>> frequencies = [500, 1000, 2000, 4000]
        >>> 
        >>> # Calculate thresholds using clinical standard
        >>> thresholds = calculate_hearing_threshold(
        ...     data, frequencies, method="modified_hughson_westlake"
        ... )
        >>> 
        >>> # Display results
        >>> for freq, threshold in thresholds.items():
        ...     print(f"{freq} Hz: {threshold:.1f} dB HL")
        
    Note:
        Thresholds are reported in dB HL (Hearing Level) as per audiological
        standards. Normal hearing is typically 0-20 dB HL across frequencies.
        
    References:
        - ASHA Guidelines for Manual Pure-Tone Threshold Audiometry (2005)
        - ISO 8253-1:2010 Audiometric test methods
    """
    # Implementation with clear inline comments explaining clinical reasoning
    if not all(col in audiogram_data.columns for col in ['frequency', 'intensity', 'response']):
        raise KeyError(
            f"Required columns missing from audiogram_data.\n"
            f"Expected: ['frequency', 'intensity', 'response']\n"  
            f"Found: {list(audiogram_data.columns)}"
        )
```

### Modern Type Hints

```python
# Python 3.12+ style - minimal typing imports
from pathlib import Path
from typing import Any, Literal
import pandas as pd
import numpy as np
from numpy.typing import NDArray

# Use built-in generics for medical data
def load_multiple_studies(
    study_names: list[str],
    data_type: Literal["audiogram", "cochlear_implant", "tinnitus"] = "audiogram"
) -> dict[str, pd.DataFrame]:
    """Load multiple study datasets into a dictionary."""

# Use union operator for optional medical parameters
def analyze_hearing_loss(
    data: pd.DataFrame,
    severity_threshold: float | tuple[float, float] | None = None,
    age_stratify: bool = True
) -> dict[str, Any]:
    """Analyze hearing loss patterns with optional stratification."""
```

### Error Handling for Research Context

```python
def load_patient_data(study_id: str, patient_id: str) -> pd.DataFrame:
    """
    Load individual patient data with research-appropriate error handling.
    
    Provides clear, actionable error messages for common research scenarios.
    """
    # Check study exists first - most common error
    study_path = PARQUET_DIR / f"{study_id}.parquet"
    if not study_path.exists():
        available_studies = [f.stem for f in PARQUET_DIR.glob("*.parquet")]
        raise FileNotFoundError(
            f"Study '{study_id}' not found.\n"
            f"Available studies: {available_studies}\n"
            f"Please check:\n"
            f"  1. Is the study name correct?\n"
            f"  2. Has the data been processed through the PyPi package?\n"
            f"  3. Do you have access to the data directory?"
        )
    
    # Load and check patient exists
    data = pd.read_parquet(study_path)
    if patient_id not in data['patient_id'].values:
        available_patients = data['patient_id'].unique()[:10]  # Show first 10
        raise ValueError(
            f"Patient '{patient_id}' not found in study '{study_id}'.\n"
            f"Study contains {len(data['patient_id'].unique())} patients.\n"
            f"First 10 patient IDs: {list(available_patients)}\n"
            f"Use data['patient_id'].unique() to see all IDs."
        )
    
    return data[data['patient_id'] == patient_id].copy()
```

## Statistical Analysis Standards

### Reproducibility Requirements

```python
# ALWAYS set seeds for any randomization
import numpy as np
import random
from sklearn.model_selection import train_test_split

# Set seeds for all libraries
def set_random_seeds(seed: int = 42) -> None:
    """Set random seeds for reproducible analysis."""
    np.random.seed(seed)
    random.seed(seed)
    # Add other libraries as needed (torch, tensorflow, etc.)

# Document statistical methods clearly
def perform_audiogram_analysis(
    data: pd.DataFrame,
    alpha: float = 0.05,
    correction_method: str = "bonferroni"
) -> dict[str, Any]:
    """
    Perform standard audiogram statistical analysis.
    
    This implements the statistical pipeline commonly used in audiology
    research, including appropriate multiple comparison corrections.
    
    Statistical Methods:
        - Normality testing: Shapiro-Wilk test (n < 50) or Kolmogorov-Smirnov (n >= 50)
        - Group comparisons: t-test (normal) or Mann-Whitney U (non-normal)
        - Multiple comparisons: Bonferroni or FDR correction
        - Effect size: Cohen's d for t-tests, r for Mann-Whitney U
        
    Args:
        data: DataFrame with columns ['group', 'threshold', 'frequency']
        alpha: Significance level (default 0.05)
        correction_method: Multiple comparison correction ("bonferroni" or "fdr")
        
    Returns:
        Dictionary containing:
            - 'test_results': DataFrame with p-values, effect sizes, CIs
            - 'normality_tests': Results of normality testing
            - 'descriptive_stats': Mean, SD, median, IQR by group
            - 'interpretation': Clinical significance notes
    """
    results = {}
    
    # Document each step clearly
    # Step 1: Check data structure and completeness
    # Step 2: Test normality assumptions  
    # Step 3: Choose appropriate statistical tests
    # Step 4: Apply multiple comparison corrections
    # Step 5: Calculate effect sizes and confidence intervals
    # Step 6: Interpret clinical significance
    
    return results
```

### Visualization Standards

```python
def plot_audiogram_comparison(
    data: pd.DataFrame,
    groups: list[str],
    save_path: Path | None = None
) -> plt.Figure:
    """
    Create publication-ready audiogram comparison plot.
    
    Follows standard audiological plotting conventions:
    - Frequency on log scale (x-axis)
    - Hearing level in dB HL (y-axis, inverted - worse hearing at bottom)
    - Standard frequency range: 250-8000 Hz
    - Color-blind friendly palette
    - Clear confidence intervals or error bars
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use color-blind friendly palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    # Standard audiological plotting conventions
    frequencies = [250, 500, 1000, 2000, 4000, 8000]
    ax.set_xscale('log')
    ax.set_xlim(200, 10000)
    ax.set_ylim(120, -10)  # Inverted y-axis (better hearing at top)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Hearing Level (dB HL)')
    ax.set_title('Audiogram Comparison by Group')
    
    # Add clinical reference lines
    ax.axhline(y=20, color='gray', linestyle='--', alpha=0.5, label='Normal hearing limit')
    ax.axhline(y=40, color='orange', linestyle='--', alpha=0.5, label='Mild hearing loss')
    
    # Plot data with confidence intervals
    for i, group in enumerate(groups):
        group_data = data[data['group'] == group]
        # Implementation with proper error bars and statistical annotations
        
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
    return fig
```

## Development Workflow

### Step-by-Step Research Analysis Process

1. **Research Question Clarification**
    - What specific hypothesis are we testing?
    - What does clinical significance look like?
    - What are the statistical assumptions?
    
2. **Analysis Design Discussion**
    - Present 2-3 statistical approaches
    - Discuss power analysis and sample size
    - Consider potential confounding variables
    - Get approval before implementation
    
3. **Incremental Implementation**
    - Start with descriptive statistics
    - Add visualizations
    - Implement statistical tests
    - Validate results with domain knowledge
    
4. **Review and Interpret**
    - Do results make clinical sense?
    - Are effect sizes meaningful?
    - What are the limitations?
    - How do results compare to literature?

### When to Provide Alternatives

ALWAYS offer choices when:

- Multiple statistical tests could be appropriate
- Different visualization approaches exist
- Performance vs interpretability tradeoffs exist
- Clinical vs statistical significance considerations differ

Example:

```
"For comparing hearing thresholds between groups, we have several options:

1. **Parametric approach** (t-test)
   - Pros: More statistical power, familiar to reviewers
   - Cons: Requires normality assumption (often violated in audiology)
   - Best if: Data is normally distributed after transformation
   
2. **Non-parametric approach** (Mann-Whitney U)
   - Pros: No normality assumption, robust to outliers
   - Cons: Less power, harder to interpret effect sizes
   - Best if: Data is clearly non-normal or small sample sizes
   
3. **Mixed-effects model** (more complex)
   - Pros: Handles repeated measures, accounts for patient variability
   - Cons: More complex to interpret, requires larger sample
   - Best if: Multiple measurements per patient

Given your sample size of 50 and preliminary plots showing right-skewed data, which approach feels right for your research question?"
```

## Collaboration Guidelines

### Working with Shared Resources

- **Templates**: Copy `shared/templates/analysis_template.py` to your project folder, don't modify original
- **Utilities**: Check `shared/utils/` before writing custom functions
- **Documentation**: Update project README.md with research questions, methods, and findings
- **Data Dictionary**: Use but don't modify the automated data dictionary from PyPi package

### Git Workflow for Researchers (Simplified)

```bash
# Daily workflow
git pull                                    # Get latest changes
# Work in projects/your-project-name/
git add projects/your-project-name/
git commit -m "Add hearing threshold analysis for CI patients"
git push

# Proposing shared utilities
git add shared/utils/new_function.py
git commit -m "Add standardized audiogram plotting function"
# Create pull request for review
```

### Code Review Checklist

Before committing ANY research analysis:

- [ ] Have I explained the research question and approach?
- [ ] Did I get approval for the statistical methods?
- [ ] Are all functions documented with clinical context?
- [ ] Do statistical tests match the research design?
- [ ] Have I checked for clinical plausibility of results?
- [ ] Are visualizations publication-ready?
- [ ] Is the analysis reproducible (seeds set)?
- [ ] Have I updated the project README?
- [ ] Are there no data files committed?
- [ ] Are file paths relative or configurable?
- [ ] Is the commit message descriptive (no co-author tags)?

## Learning Resources for Medical Research

When implementing new statistical concepts, provide:

1. Simple explanation with clinical context
2. Minimal working example with medical data
3. Common pitfalls in medical research
4. Links to clinical research resources

Example:

```python
"""
Power Analysis for Audiology Research

Power analysis helps determine if your study has enough participants
to detect clinically meaningful differences in hearing thresholds.

Clinical context:
- Minimal clinically important difference: ~5-10 dB for most applications
- Standard deviation in healthy adults: ~5-15 dB depending on frequency
- Common effect sizes in audiology: small (0.2), medium (0.5), large (0.8)

Simple example:
"""
from scipy import stats
import numpy as np

def calculate_sample_size_audiogram(
    effect_size: float = 0.5,  # Cohen's d
    alpha: float = 0.05,       # Type I error rate  
    power: float = 0.80        # Statistical power (1 - Type II error)
) -> int:
    """Calculate required sample size for audiogram comparison."""
    
    # Two-tailed t-test sample size calculation
    z_alpha = stats.norm.ppf(1 - alpha/2)  # Critical value for alpha
    z_beta = stats.norm.ppf(power)         # Critical value for power
    
    # Sample size per group
    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
    
    return int(np.ceil(n))

# Example: To detect a medium effect (0.5 Cohen's d) with 80% power
n_per_group = calculate_sample_size_audiogram(effect_size=0.5)
print(f"Need {n_per_group} participants per group")

# Clinical interpretation:
# - This would detect ~7.5 dB difference if SD = 15 dB
# - Increase n for smaller clinically important differences
```

## Remember: Research-Focused Development

1. **Clinical relevance first** - statistical significance isn't always clinically meaningful
2. **Reproducibility is critical** - other researchers must be able to replicate
3. **Document everything** - methods, assumptions, limitations
4. **Collaborate and learn** - browse others' approaches in projects/ folder
5. **Security is not optional** - treat all data as PHI

When in doubt about research methods, statistical approaches, or clinical interpretation, stop and ask. The goal is rigorous, reproducible medical research that advances understanding of hearing and related disorders.

## NSQIP-Specific Implementation Details

### Critical Reminders
- **Always use Polars**, never pandas - nsqip_tools is designed for Polars
- **No emojis** in any documentation or code
- **Sandbox mode** is enforced through helper scripts (./nsqip edit)
- **Data is strings** - NSQIP outcomes are text like "No Complication", "Pneumonia", not 0/1
- **Auto-detection** - Helper functions detect adult vs pediatric using age columns

### Repository Structure
```
NSQIP-analysis/
├── nsqip                      # Helper script for sandboxed marimo
├── nsqip.bat                  # Windows version
├── quickstart.py              # Interactive project setup
├── shared/
│   ├── templates/
│   │   └── basic_analysis.py  # Marimo template with optional helpers
│   ├── utils/
│   │   └── nsqip_helpers.py  # Auto-detecting helper functions
│   └── docs/
│       ├── adult_data_dictionary.json
│       └── pediatric_data_dictionary.json
└── projects/                  # Researcher folders
```

### Key Technical Decisions
1. **LazyFrame Support** - All helpers preserve DataFrame/LazyFrame type
2. **Path-based data access** - No environment variables, paths in notebooks
3. **String outcomes** - Handle NSQIP's text-based complication variables
4. **Helper imports optional** - Template has commented imports to avoid IDE errors
5. **Direct to main branch** - Simple Git workflow for beginners

### NSQIP Data Characteristics
- **Adult age**: AGE_AS_INT (integer years)
- **Pediatric age**: AGE_DAYS (integer days)
- **Outcomes**: Text strings ("No Complication" vs specific complication)
- **ASA Class**: Text with description (e.g., "2-Mild Disturb")
- **Sex**: Different capitalization (adult: "male", pediatric: "Male")
- **SSI Variables**: SUPINFEC, WNDINFD, ORGSPCSSI (same names both datasets)

### Collaboration Setup
- Repository at: https://github.com/jabrant/NSQIP-analysis
- Private repo - add collaborators via Settings → Manage access
- Each researcher works in projects/lastname-description/
- Shared utilities require maintainer approval

### When Updating
- Test with both adult and pediatric data
- Ensure all functions handle both DataFrame and LazyFrame
- Keep documentation beginner-friendly
- Always consider PHI protection
