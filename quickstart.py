#!/usr/bin/env python3
"""
Clinical Database Repository Quick Start

Helps new users get started with their first project.
Supports both NSQIP and NCDB databases.
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess
from datetime import datetime

def main():
    print("\nClinical Database Repository Quick Start")
    print("="*40)
    
    # Select database type
    print("\nWhich database are you working with?")
    print("1. NSQIP (Surgical Outcomes)")
    print("2. NCDB (Cancer Outcomes)")
    db_choice = input("Enter 1 or 2: ").strip()
    
    if db_choice == "1":
        db_type = "NSQIP"
        template_file = "basic_analysis.py"
    elif db_choice == "2":
        db_type = "NCDB"
        template_file = "clinical_db_analysis.py"
    else:
        print("Error: Please enter 1 or 2")
        sys.exit(1)
    
    # Get researcher name
    print("\nFirst, let's set up your project folder.")
    last_name = input("Enter your last name: ").strip().lower()
    if not last_name:
        print("Error: Last name is required")
        sys.exit(1)
    
    # Get project description
    print("\nWhat are you analyzing?")
    if db_type == "NSQIP":
        print("Examples: mortality, ssi-risk, readmissions, complications")
    else:
        print("Examples: survival, treatment-patterns, disparities, staging")
    description = input("Brief description: ").strip().lower().replace(" ", "-")
    if not description:
        print("Error: Description is required")
        sys.exit(1)
    
    # Create project folder
    project_name = f"{last_name}-{description}"
    project_path = Path("projects") / project_name
    
    if project_path.exists():
        print(f"\nError: Project '{project_name}' already exists!")
        sys.exit(1)
    
    print(f"\nCreating project: {project_name}")
    project_path.mkdir(parents=True)
    
    # Copy appropriate template
    template_src = Path("shared/templates") / template_file
    template_dst = project_path / "analysis.py"
    
    # If the new template doesn't exist, fall back to basic
    if not template_src.exists():
        template_src = Path("shared/templates/basic_analysis.py")
    
    shutil.copy2(template_src, template_dst)
    print(f"✓ Copied {db_type} analysis template")
    
    # Create README
    readme_content = f"""# Project: {description.replace('-', ' ').title()}

**Researcher**: Dr. {last_name.title()}  
**Database**: {db_type}  
**Date Started**: {datetime.now().strftime('%Y-%m-%d')}  
**Status**: In Progress

## Research Question

[Enter your research question here]

## Methods

### Data Source
- Database: {db_type}
- Years: [Specify years]
- Population: [Describe inclusion/exclusion criteria]

### Analysis Plan
[Describe your analytical approach]

## Key Findings

[Update as you progress]

## Notes

[Any additional notes or considerations]
"""
    
    readme_path = project_path / "README.md"
    readme_path.write_text(readme_content)
    print("✓ Created project README")
    
    # Create results directory
    (project_path / "results").mkdir()
    print("✓ Created results directory")
    
    print(f"\n✅ Project '{project_name}' created successfully!")
    print("\nNext steps:")
    print(f"1. Edit your research question: projects/{project_name}/README.md")
    print(f"2. Start your analysis: ./db edit projects/{project_name}/analysis.py")
    print("\nHappy researching!")
    
    # Ask if they want to open the notebook now
    response = input("\nWould you like to open your analysis notebook now? (y/n): ")
    if response.lower() == 'y':
        cmd = ["python3", "db", "edit", f"projects/{project_name}/analysis.py"]
        subprocess.run(cmd)

if __name__ == "__main__":
    main()