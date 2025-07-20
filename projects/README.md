# NSQIP Research Projects

This folder contains individual researcher projects. Each researcher should create their own folder here for their analyses.

## Creating Your Project Folder

1. Create a new folder with the naming convention: `lastname-brief-description`
   - Example: `smith-mortality-analysis`
   - Example: `jones-ssi-prevention`

2. Copy the analysis template to start:
   ```bash
   # For Adult NSQIP
   cp ../shared/templates/nsqip_analysis.py smith-mortality-analysis/analysis.py
   
   # For Pediatric NSQIP
   cp ../shared/templates/pnsqip_analysis.py smith-mortality-analysis/analysis.py
   
   # For NCDB
   cp ../shared/templates/ncdb_analysis.py smith-mortality-analysis/analysis.py
   ```

3. Create a README.md in your folder documenting:
   - Research question
   - Methods
   - Key findings
   - See `example-mortality-analysis/README.md` for a template

## Project Organization

Each project folder should contain:
- `README.md` - Project documentation
- `analysis.py` - Main analysis notebook (Marimo)
- `results/` - Output tables and figures (created automatically)
- `exploratory/` - Optional: preliminary analyses

## Important Reminders

- **Never commit data files** - The .gitignore protects against this
- **Update your README** as you progress through your analysis
- **Don't modify other researchers' folders** - Only work in your own project
- **Share utilities** - If you create something useful for everyone, propose adding it to `shared/utils/`

## Current Projects

- `example-mortality-analysis/` - Example project structure (template)