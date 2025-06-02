# NSQIP Collaborative Analysis Repository

Welcome! This repository helps surgical researchers collaborate on NSQIP data analysis. It's designed for beginners - no advanced technical knowledge required.

## What This Repository Does

- **Organizes** your NSQIP analysis projects
- **Provides** templates to get started quickly  
- **Enables** collaboration without data sharing
- **Protects** patient data automatically

## Prerequisites

Before starting, make sure you have:

1. **NSQIP Data Access** - Your institution's NSQIP parquet files (created using nsqip_tools)
2. **Python** - Version 3.10 or newer ([Download Python](https://www.python.org/downloads/))
3. **Git** - For collaboration ([Download Git](https://git-scm.com/downloads))
4. **GitHub Account** - Free account for collaboration ([Sign up](https://github.com/))
5. **Repository Access** - Accept the invitation sent to your email

## Getting Started (First Time Setup)

### Step 1: Accept Repository Invitation

Check your email for a GitHub invitation to collaborate on this repository. Click the link to accept.

### Step 2: Copy This Repository

Open your terminal (Mac) or Command Prompt (Windows) and run:

```bash
git clone https://github.com/jabrant/NSQIP-analysis.git
cd NSQIP-analysis
```

If prompted for credentials, use your GitHub username and a personal access token (not your password).
[Create a token here](https://github.com/settings/tokens) with "repo" permissions.

### Step 3: Install Required Tools

```bash
# Install the package manager
pip install uv

# Install analysis tools
uv pip install marimo nsqip-tools polars matplotlib seaborn
```

### Step 4: Create Your Project Folder

**Quick Start (Recommended for beginners):**
```bash
python3 quickstart.py
```

This will guide you through creating your project folder.

**Manual Setup:**
1. Navigate to the `projects` folder
2. Create a new folder: `lastname-brief-description` (e.g., `smith-mortality-analysis`)
3. Copy the analysis template:

```bash
# From the repository root directory
cp shared/templates/basic_analysis.py projects/smith-mortality-analysis/analysis.py
```

### Step 5: Start Your Analysis

```bash
# Navigate to your project
cd projects/smith-mortality-analysis

# Open the analysis notebook using our helper script
../../nsqip edit analysis.py
```

Or from the repository root:

```bash
./nsqip edit projects/smith-mortality-analysis/analysis.py
```

The helper script automatically uses sandbox mode to keep your environment clean.

## Repository Structure

```
NSQIP-analysis/
├── README.md                  # This file
├── nsqip                      # Helper script (Mac/Linux)
├── nsqip.bat                  # Helper script (Windows)
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

## Using the NSQIP Helper Script

We provide a simple helper script that ensures notebooks always run in sandbox mode:

**Mac/Linux:**
```bash
./nsqip edit analysis.py    # Edit or create a notebook
./nsqip run analysis.py     # Run notebook (read-only)
./nsqip new                 # Create new notebook
./nsqip help               # Show help
```

**Windows:**
```bash
nsqip.bat edit analysis.py    # Edit or create a notebook
nsqip.bat run analysis.py     # Run notebook (read-only)
nsqip.bat new                # Create new notebook
nsqip.bat help              # Show help
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
../../nsqip edit analysis.py
```

**Windows users**: Use `..\..\nsqip.bat edit analysis.py`

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

1. **Load your data** using nsqip_tools
2. **Filter cases** by CPT codes, years, or diagnoses  
3. **Calculate outcomes** like mortality, complications, readmissions
4. **Create visualizations** for publication
5. **Export results** as tables

### Example: Loading Your Data

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
- **NSQIP User Guide**: See `shared/docs/nsqip_puf_userguide_2022.pdf`
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

**Remember**: Focus on your research questions, not the technology. This repository handles the technical details so you can concentrate on surgical outcomes research!