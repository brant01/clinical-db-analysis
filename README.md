# Clinical Database Collaborative Analysis Repository

Welcome! This repository helps clinical researchers collaborate on NSQIP (surgical outcomes) and NCDB (cancer outcomes) data analysis. It's designed for beginners - no advanced technical knowledge required.

## What This Repository Does

- **Organizes** your NSQIP and NCDB analysis projects
- **Provides** templates to get started quickly  
- **Enables** collaboration without data sharing
- **Protects** patient data automatically

## Prerequisites

Before starting, make sure you have:

1. **Clinical Data Access** - Your institution's NSQIP and/or NCDB parquet files (created using nsqip_tools or ncdb-tools)
2. **Python** - Version 3.13 or newer ([Download Python](https://www.python.org/downloads/))
3. **uv** - Fast Python package manager ([Install uv](https://docs.astral.sh/uv/getting-started/installation/))
4. **Git** - For collaboration ([Download Git](https://git-scm.com/downloads))
5. **GitHub Account** - Free account for collaboration ([Sign up](https://github.com/))

## Getting Started

### Step 1: Clone the Repository

After accepting your GitHub invitation, clone this repository:

```bash
git clone https://github.com/jabrant/clinical-db-analysis.git
cd clinical-db-analysis
```

### Step 2: Set Up Your Data Paths

Copy the example environment file and update with your data paths:

```bash
cp .env.example .env
# Edit .env with your actual data paths
```

### Step 3: Create Your Project

Create your own project folder and copy the appropriate template:

```bash
# Create your project folder
mkdir projects/yourname-description
# Example: mkdir projects/smith-mortality

# Copy the template for your data type:
```

**For Adult NSQIP:**
```bash
cp shared/templates/nsqip_analysis.py projects/yourname-description/analysis.py
```

**For Pediatric NSQIP:**
```bash
cp shared/templates/pnsqip_analysis.py projects/yourname-description/analysis.py
```

**For NCDB Cancer Data:**
```bash
cp shared/templates/ncdb_analysis.py projects/yourname-description/analysis.py
```

### Step 4: Start Analyzing

Open your copy of the template:

```bash
uv run marimo edit --sandbox projects/yourname-description/analysis.py
```

### That's it! 🎉

The template will guide you through:
1. Setting your data path
2. Loading and filtering data
3. Creating visualizations
4. Exporting results

## ⚠️ Current Known Issues

### Data Loading Issues (July 2024)

**If you encounter errors when loading NSQIP data**, use this alternative approach:

Instead of using nsqip_tools, load data directly with polars:

```python
import polars as pl
from pathlib import Path

# Load NSQIP data directly
DATA_PATH = Path("/path/to/your/data/adult_nsqip_parquet")
df = (
    pl.scan_parquet(DATA_PATH / "*.parquet")
    .with_columns([
        # Clean problematic columns
        pl.col("MORBPROB").map_elements(
            lambda x: None if str(x).strip() in ["", " "] else x,
            return_dtype=pl.Float64
        ),
        pl.col("MORTPROB").map_elements(
            lambda x: None if str(x).strip() in ["", " "] else x,
            return_dtype=pl.Float64
        ),
    ])
    .filter(
        # Your filters here
        (pl.col("ALL_CPT_CODES").list.len() == 1) &
        (pl.col("ALL_CPT_CODES").list.first().is_in(["42821", "42826"]))
    )
    .collect()
)
```

**Issues being resolved:**
- nsqip_tools filter_by_cpt() method has a bug with column references
- Parquet files have schema inconsistencies across years
- Some numeric columns contain empty strings instead of null values

These issues are being addressed in upcoming updates to nsqip_tools and the parquet creation process.

## Repository Structure

```
clinical-db-analysis/
├── README.md                  # This file
├── .env.example              # Environment configuration template
├── pyproject.toml            # Project dependencies
├── shared/                    # Resources for everyone
│   ├── templates/            # Analysis templates
│   │   ├── nsqip_analysis.py  # Adult NSQIP template
│   │   ├── pnsqip_analysis.py # Pediatric NSQIP template
│   │   └── ncdb_analysis.py   # NCDB cancer data template
│   ├── utils/                # Helper functions
│   └── docs/                 # Documentation
└── projects/                  # Individual researcher folders
    └── [your-name-project]/  # Your analysis goes here
        ├── README.md         # Document your research
        ├── analysis.py       # Your main analysis
        └── results/          # Plots and tables
```

## Daily Workflow

### Starting Your Work Session

```bash
# 1. Get latest updates
git pull

# 2. Open your analysis
uv run marimo edit --sandbox projects/yourname-description/analysis.py
```

### Saving Your Work

```bash
# 1. See what changed
git status

# 2. Add your changes
git add projects/yourname-description/

# 3. Save with a message
git commit -m "Add mortality analysis for emergency cases"

# 4. Share with team
git push
```

## Choosing the Right Template

### Template Selection Guide

- **`nsqip_analysis.py`** - For adult surgical outcomes (ACS NSQIP)
  - Use for: General surgery, vascular, orthopedic procedures
  - Key features: CPT code filtering, surgical complications, mortality

- **`pnsqip_analysis.py`** - For pediatric surgical outcomes (ACS Pediatric NSQIP)
  - Use for: Pediatric surgery cases
  - Key features: Age-specific complications, pediatric risk factors

- **`ncdb_analysis.py`** - For cancer outcomes (NCDB)
  - Use for: Cancer treatment outcomes, survival analysis
  - Key features: Cancer site filtering, stage analysis, treatment patterns

## Using the Analysis Templates

All templates include interactive UI components and show you how to:

1. **Load your data** using nsqip_tools or ncdb-tools
2. **Filter cases** by CPT codes, years, or diagnoses  
3. **Calculate outcomes** like mortality, complications, readmissions
4. **Create visualizations** for publication
5. **Export results** as tables

### Example: Loading Your Data

**For NSQIP (Surgical Outcomes):**
```python
# Example from nsqip_analysis.py template
import marimo as mo
import nsqip_tools
import polars as pl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Interactive data path configuration
data_path = mo.ui.text(
    label="NSQIP Data Path:",
    value=os.getenv("NSQIP_PATH", "/path/to/nsqip_parquet")
)

# Load data with filters
df = (
    nsqip_tools.load_data(data_path.value)
    .filter_by_cpt(["44970"])  # Laparoscopic appendectomy
    .filter_by_year([2021, 2022])
    .collect()
)
```

**For NCDB (Cancer Outcomes):**
```python
# Example from ncdb_analysis.py template
import marimo as mo
import ncdb_tools
import polars as pl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Interactive data path configuration
data_path = mo.ui.text(
    label="NCDB Data Path:",
    value=os.getenv("NCDB_PATH", "/path/to/ncdb_parquet")
)

# Load data with filters
df = (
    ncdb_tools.load_data(data_path.value)
    .filter_by_site(["C50"])  # Breast cancer
    .filter_by_year([2021, 2022])
    .collect()
)
```

## Data Security

**CRITICAL**: This repository automatically protects patient data:

- Code files are shared
- Data files are NEVER uploaded
- Results with patient info are NEVER uploaded
- Each researcher uses their own secure data path

The `.gitignore` file handles this automatically - don't modify it!

## Documentation Tips

Always document your analysis in your project's README:

```markdown
# Project: [Your Analysis Title]

## Research Question
What factors predict 30-day mortality in emergency surgery?

## Methods
- Population: Emergency cases (EMERGENT=1)
- Outcomes: 30-day mortality (DEATH30)
- Analysis: Logistic regression with risk adjustment

## Key Findings
- Finding 1...
- Finding 2...
```

## Getting Help

### Common Issues

**"Cannot find data" error**  
- Check your data path in the notebook
- Ensure you have access to the network drive

**"Package not found" error**
- Run: `uv add [package-name]` to add missing packages to the project

### Resources

- **nsqip_tools documentation**: See `shared/docs/nsqip_tools_README.md`
- **ncdb-tools documentation**: See ncdb-tools package documentation
- **NSQIP User Guide**: See `shared/docs/nsqip_puf_userguide_2022.pdf`
- **NCDB User Guide**: See your institution's NCDB documentation
- **Polars documentation**: [Polars User Guide](https://pola-rs.github.io/polars/user-guide/)
- **Git Help**: [GitHub's Git Handbook](https://guides.github.com/introduction/git-handbook/)

## Collaboration Guidelines

1. **Work in your own folder** - Don't modify others' projects
2. **Update regularly** - Run `git pull` before starting work
3. **Commit often** - Save your progress frequently
4. **Write clear messages** - Help others understand your changes
5. **Ask questions** - We're all learning together!

## Environment Configuration

The repository includes a `.env.example` file showing the required environment variables. During setup (Step 2), you copied this to `.env` and updated it with your actual data paths.

If you need to update your data paths later:

```bash
# Edit your .env file
nano .env  # or use your preferred text editor
```

This keeps your data paths secure and makes notebooks portable across different machines.

## For Repository Maintainers

To add new researchers:
1. Send GitHub invitation to their email
2. Have them clone the repository
3. Guide them to create their project folder
4. Review their first pull request

---

**Remember**: Focus on your research questions, not the technology. This repository handles the technical details so you can concentrate on clinical outcomes research!