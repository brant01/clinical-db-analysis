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
2. **Python** - Version 3.10 or newer ([Download Python](https://www.python.org/downloads/))
3. **Git** - For collaboration ([Download Git](https://git-scm.com/downloads))
4. **GitHub Account** - Free account for collaboration ([Sign up](https://github.com/))
5. **Repository Access** - Accept the invitation sent to your email

## Getting Started

### Step 1: Clone the Repository

After accepting your GitHub invitation, clone this repository:

```bash
git clone https://github.com/jabrant/clinical-db-analysis.git
cd clinical-db-analysis
```

### Step 2: Install Required Tools

Make sure you have Python 3.8+ and install uv (our package manager):

```bash
pip install uv
```

### Step 3: Create Your Project Folder

1. Create a folder for your analysis in the `projects` directory:
   ```bash
   mkdir projects/yourname-description
   ```
   Example: `mkdir projects/smith-mortality`

2. Copy the appropriate template for your database:
   - **Adult NSQIP**: `cp shared/templates/nsqip_analysis.py projects/yourname-description/analysis.py`
   - **Pediatric NSQIP**: `cp shared/templates/pnsqip_analysis.py projects/yourname-description/analysis.py`
   - **NCDB**: `cp shared/templates/ncdb_analysis.py projects/yourname-description/analysis.py`

3. Create a README for your project:
   ```bash
   echo "# My Analysis Project" > projects/yourname-description/README.md
   ```

### Step 4: Start Analyzing

Open your analysis notebook:

```bash
./db edit projects/yourname-description/analysis.py
```

On Windows, use: `db.bat edit projects/yourname-description/analysis.py`

The `db` helper script will:
- Install all required packages automatically
- Open an interactive marimo notebook
- Run in a clean, isolated environment

### That's it! 🎉

You're ready to start analyzing data. The template will guide you through:
1. Setting your data path
2. Loading and filtering data
3. Creating visualizations
4. Exporting results

## Repository Structure

```
clinical-db-analysis/
├── README.md                  # This file
├── db                         # Helper script (Mac/Linux)
├── db.bat                     # Helper script (Windows)
├── shared/                    # Resources for everyone
│   ├── templates/            # Analysis templates
│   │   └── basic_analysis.py # Start here!
│   ├── utils/                # Helper functions
│   └── docs/                 # Documentation
└── projects/                  # Individual researcher folders
    └── [your-name-project]/  # Your analysis goes here
        ├── README.md         # Document your research
        ├── analysis.py       # Your main analysis
        └── results/          # Plots and tables
```

## Using the Clinical Database Helper Script

We provide a simple helper script that ensures notebooks always run in sandbox mode:

**Mac/Linux:**
```bash
./db edit analysis.py    # Edit or create a notebook
./db run analysis.py     # Run notebook (read-only)
./db new                 # Create new notebook
./db help               # Show help
```

**Windows:**
```bash
db.bat edit analysis.py    # Edit or create a notebook
db.bat run analysis.py     # Run notebook (read-only)
db.bat new                # Create new notebook
db.bat help              # Show help
```

This automatically installs required packages in an isolated environment.

## Daily Workflow

### Starting Your Work Session

```bash
# 1. Get latest updates
git pull

# 2. Navigate to your project
cd projects/your-project-name

# 3. Open your analysis
../../db edit analysis.py
```

**Windows users**: Use `..\..\db.bat edit analysis.py`

### Saving Your Work

```bash
# 1. See what changed
git status

# 2. Add your changes
git add projects/your-project-name/

# 3. Save with a message
git commit -m "Add mortality analysis for emergency cases"

# 4. Share with team
git push
```

## Using the Analysis Template

The template in `shared/templates/basic_analysis.py` shows you how to:

1. **Load your data** using nsqip_tools or ncdb-tools
2. **Filter cases** by CPT codes, years, or diagnoses  
3. **Calculate outcomes** like mortality, complications, readmissions
4. **Create visualizations** for publication
5. **Export results** as tables

### Example: Loading Your Data

**For NSQIP (Surgical Outcomes):**
```python
import nsqip_tools
import polars as pl

# Set your data path (update this to your institution's path)
DATA_PATH = "/path/to/your/nsqip_parquet_dataset"

# Load and filter data
df = (nsqip_tools.load_data(DATA_PATH)
      .filter_by_cpt(["44970"])     # Laparoscopic appendectomy
      .filter_by_year([2021, 2022])  # Recent years
      .collect())

print(f"Loaded {len(df)} cases")
```

**For NCDB (Cancer Outcomes):**
```python
import ncdb_tools
import polars as pl

# Set your data path (update this to your institution's path)
DATA_PATH = "/path/to/your/ncdb_parquet_dataset"

# Load and filter data
df = (ncdb_tools.load_data(DATA_PATH)
      .filter_by_site(["C50"])       # Breast cancer
      .filter_by_year([2021, 2022])  # Recent years
      .collect())

print(f"Loaded {len(df)} cases")
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

**"Permission denied" error**
- Make sure you've accepted the GitHub invitation
- Check that you're using a personal access token, not your password

**"Cannot find data" error**  
- Check your DATA_PATH in the notebook
- Ensure you have access to the network drive

**"Package not found" error**
- Run: `uv pip install [package-name]`

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

## For Repository Maintainers

See `shared/docs/maintainer-guide.md` for:
- Adding new researchers
- Creating shared utilities
- Managing the repository

---

**Remember**: Focus on your research questions, not the technology. This repository handles the technical details so you can concentrate on clinical outcomes research!