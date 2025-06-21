# Project Architecture - Clinical Database Analysis

## Overview
A collaborative research platform using marimo interactive notebooks for analyzing clinical databases (NSQIP and NCDB). The architecture prioritizes data security, user simplicity, and reproducible research through template-based analysis in sandboxed environments.

## Directory Structure
```
clinical-db-analysis/
├── README.md                    # Main user documentation
├── CLAUDE.md                   # AI assistant quick reference
├── .env                        # Local data path configuration
├── .gitignore                  # PHI protection patterns
│
├── db                          # Unix helper script  
├── db.bat                      # Windows helper script
├── db_helper.py                # Helper implementation
│
├── shared/                     # Shared resources
│   ├── templates/              # Analysis templates
│   │   ├── nsqip_analysis.py   # Adult NSQIP
│   │   ├── pnsqip_analysis.py  # Pediatric NSQIP
│   │   └── ncdb_analysis.py    # NCDB cancer
│   ├── utils/                  # Helper functions
│   └── docs/                   # Documentation
│
├── projects/                   # User projects
│   └── [lastname-topic]/       # Individual analyses
│       ├── README.md
│       ├── analysis.py
│       └── results/
│
└── claude_config/              # AI configuration
    └── claude_config/          # Config system
        ├── experts/            # Domain expertise
        ├── guidelines/         # Standards
        └── project/            # Project info
```

## Core Components

### Helper System (`db`, `db_helper.py`)
- **Purpose:** Simplify notebook execution and environment management
- **Dependencies:** Python 3.8+, uv package manager
- **Interfaces:** 
  - `./db edit [notebook]` - Edit mode
  - `./db run [notebook]` - Read-only mode
  - `./db new [name]` - Create new notebook

### Analysis Templates
- **Purpose:** Provide starting points for each database type
- **Dependencies:** marimo, polars, database-specific tools
- **Interfaces:** Copy template → Modify for specific analysis

### Marimo Notebooks
- **Purpose:** Interactive, reactive data analysis
- **Dependencies:** marimo framework
- **Interfaces:** Python functions as cells with automatic dependency tracking

## Data Flow

```
1. User Data (Local) → 2. Template Loads → 3. Interactive Filters
         ↓                                           ↓
   6. Export Results ← 5. Visualizations ← 4. Analysis Cells
```

### Detailed Flow:
1. **Data Loading:** User sets DATA_PATH, tools load parquet files
2. **Interactive Filtering:** UI components (dropdowns, sliders) filter data
3. **Reactive Analysis:** Changes propagate automatically through dependent cells
4. **Result Generation:** Tables, plots, statistics computed on demand
5. **Export:** Results saved locally, never uploaded

## Design Decisions

### Decision: Marimo over Jupyter
- **Date:** 2025-01
- **Context:** Need for reproducible, interactive notebooks
- **Options Considered:**
  1. Jupyter - Traditional, widely known
  2. Marimo - Reactive, pure Python files
- **Decision:** Marimo
- **Rationale:** Better reproducibility, version control, reactive programming

### Decision: Manual Project Creation
- **Date:** 2025-01
- **Context:** Simplify onboarding process
- **Options Considered:**
  1. Automated setup script
  2. Interactive quickstart
  3. Manual folder creation
- **Decision:** Manual creation with clear instructions
- **Rationale:** Simpler, fewer failure points, educational for users

### Decision: Template-Based Approach
- **Date:** 2025-01
- **Context:** Support different database types
- **Options Considered:**
  1. Single universal template
  2. Database-specific templates
  3. Configuration-based system
- **Decision:** Three specific templates
- **Rationale:** Better user experience, clearer examples, specific features

## Integration Points
- **External Systems:** None (intentionally isolated)
- **APIs:** None (data stays local)
- **Data Sources:** 
  - Institution's NSQIP parquet files
  - Institution's NCDB parquet files
  - User must have local access

## Security Architecture
- **Authentication:** Handled by OS/institution
- **Authorization:** File system permissions
- **Data Protection:** 
  - No data in repository
  - .gitignore prevents accidental commits
  - Each user's data stays on their system
- **Audit Logging:** Git history for code changes only

## Performance Considerations
- **Bottlenecks:** Large dataset loading
- **Optimization:** 
  - Polars for efficient dataframe operations
  - Lazy evaluation where possible
  - Parquet format for fast I/O
- **Caching:** Marimo's reactive model prevents redundant computation
- **Scaling:** Templates handle millions of records efficiently

## Deployment Strategy
- **Distribution:** Git clone only
- **Updates:** Git pull for latest templates
- **Dependencies:** Handled automatically by uv
- **Platform Support:** Windows, Mac, Linux