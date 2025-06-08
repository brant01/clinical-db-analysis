# Project Architecture - EDITABLE

## Overview
The clinical-db-analysis repository uses a distributed architecture where each researcher maintains their own local clinical data (NSQIP or NCDB) while sharing only analysis code. This ensures HIPAA compliance while enabling collaboration. The system leverages marimo notebooks for interactive analysis and git for version control.

## Directory Structure
```
clinical-db-analysis/
├── projects/              # Individual researcher folders
│   ├── example-mortality-analysis/
│   └── [researcher-name-project]/
│       ├── README.md     # Project documentation
│       ├── analysis.py   # Main marimo notebook
│       └── results/      # Generated outputs
├── shared/               # Shared resources
│   ├── templates/       # Analysis templates
│   │   └── basic_analysis.py
│   ├── utils/           # Helper functions
│   │   └── nsqip_helpers.py
│   └── docs/            # Documentation
├── claude_config/       # AI assistant configuration
├── db                  # Helper script (Mac/Linux)
├── db.bat              # Helper script (Windows)
├── quickstart.py       # New project wizard
└── pyproject.toml      # Project dependencies
```

## Core Components

### Database Helper Script (db/db.bat)
- **Purpose:** Simplifies marimo notebook management with sandbox mode
- **Dependencies:** marimo, uv (auto-installed)
- **Interfaces:** Command-line: `./db edit|run|new|help`

### Analysis Templates
- **Purpose:** Provide starting points for common NSQIP analyses
- **Dependencies:** nsqip-tools, polars, marimo
- **Interfaces:** Copy template to new project, customize as needed

### Quickstart Wizard
- **Purpose:** Guide new users through project setup
- **Dependencies:** Python standard library only
- **Interfaces:** Interactive CLI prompts

### Shared Utilities
- **Purpose:** Common functions for NSQIP data analysis
- **Dependencies:** nsqip-tools, polars
- **Interfaces:** Import into analysis notebooks

## Data Flow
```
1. Institution's Clinical Data (NSQIP/NCDB Parquet files)
   ↓
2. Researcher's Local Machine
   ↓
3. nsqip-tools or ncdb-tools loads data into Polars DataFrames
   ↓
4. Marimo notebook performs analysis
   ↓
5. Results saved locally (never uploaded)
   ↓
6. Only code committed to Git repository
```

Key principle: Data never leaves the researcher's local environment

## Design Decisions

### Decision: Marimo over Jupyter
- **Date:** 2025-06-03
- **Context:** Need reproducible, interactive notebooks
- **Options Considered:**
  1. Jupyter - Traditional but state management issues
  2. Marimo - Reactive, reproducible, Git-friendly
- **Decision:** Marimo notebooks
- **Rationale:** Better reproducibility, cleaner diffs, reactive updates

### Decision: Polars over Pandas
- **Date:** 2025-06-03
- **Context:** Large NSQIP datasets (1M+ records)
- **Options Considered:**
  1. Pandas - Familiar but slower
  2. Polars - Fast, modern API
- **Decision:** Polars with lazy evaluation
- **Rationale:** 10-100x performance improvement, better memory usage

## Integration Points
- **External Systems:** None (all local)
- **APIs:** None (security requirement)
- **Data Sources:** 
  - Institution's NSQIP Parquet files (via nsqip-tools)
  - NSQIP: Must be pre-processed from ACS NSQIP PUFs
  - NCDB: Must be pre-processed from CoC NCDB PUFs

## Security Architecture
- **Authentication:** Git/GitHub for code access only
- **Authorization:** Repository access controls
- **Data Protection:** 
  - .gitignore prevents data upload
  - All analysis runs locally
  - No patient identifiers in code
- **Audit Logging:** Git commit history

## Performance Considerations
- **Bottlenecks:** Initial data loading from Parquet
- **Optimization:** 
  - Polars lazy evaluation
  - Column selection at load time
  - Predicate pushdown for filtering
- **Caching:** Parquet format provides built-in compression
- **Scaling:** Horizontal - each researcher works independently