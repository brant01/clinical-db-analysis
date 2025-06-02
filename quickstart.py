#!/usr/bin/env python3
"""
NSQIP Repository Quick Start

Helps new users get started with their first project.
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess

def main():
    print("\nNSQIP Repository Quick Start")
    print("="*40)
    
    # Get researcher name
    print("\nFirst, let's set up your project folder.")
    last_name = input("Enter your last name: ").strip().lower()
    if not last_name:
        print("Error: Last name is required")
        sys.exit(1)
    
    # Get project description
    print("\nWhat are you analyzing?")
    print("Examples: mortality, ssi-risk, readmissions")
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
    
    # Copy template
    template_src = Path("shared/templates/basic_analysis.py")
    template_dst = project_path / "analysis.py"
    shutil.copy2(template_src, template_dst)
    print("✓ Copied analysis template")
    
    # Create README
    readme_content = f"""# Project: {description.replace('-', ' ').title()}

**Researcher**: Dr. {last_name.title()}  
**Date Started**: {Path.ctime(project_path)}  
**Status**: In Progress

## Research Question

[Enter your research question here]

## Methods

[Describe your methods]

## Key Findings

[Update as you progress]
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
    print(f"2. Start your analysis: ./nsqip edit projects/{project_name}/analysis.py")
    print("\nHappy researching!")
    
    # Ask if they want to open the notebook now
    response = input("\nWould you like to open your analysis notebook now? (y/n): ")
    if response.lower() == 'y':
        cmd = ["python3", "nsqip", "edit", f"projects/{project_name}/analysis.py"]
        subprocess.run(cmd)

if __name__ == "__main__":
    main()