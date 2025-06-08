#!/usr/bin/env python3
"""
Clinical Database Analysis Helper

This script ensures marimo notebooks always run in sandbox mode and 
automatically installs required packages. Designed for beginners.
"""

import sys
import subprocess
import os
from pathlib import Path

def print_usage():
    """Print usage information."""
    print("""
Clinical Database Analysis Helper

Usage:
    ./db edit [notebook]     # Edit a notebook (creates if doesn't exist)
    ./db run [notebook]      # Run a notebook in read-only mode
    ./db new [name]          # Create a new notebook
    ./db help               # Show this message

Examples:
    ./db edit analysis.py
    ./db edit projects/smith-mortality/analysis.py
    ./db run shared/templates/clinical_db_analysis.py
    ./db new exploratory_analysis.py

This script works with both NSQIP and NCDB analyses!

Environment:
    The script automatically creates an isolated environment with:
    - marimo (interactive notebooks)
    - nsqip-tools (for NSQIP data)
    - ncdb-tools (for NCDB data)
    - polars, matplotlib, seaborn (data analysis)
""")

def check_uv_installed():
    """Check if uv is installed, provide helpful error if not."""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: 'uv' is not installed.")
        print("Please install it with: pip install uv")
        print("\nIf you don't have pip, install Python from python.org first.")
        return False

def run_marimo_command(args):
    """Run marimo with uv in sandbox mode."""
    # Build the command
    # Using --with ensures these packages are available in sandbox
    cmd = [
        "uv", "run", 
        "--with", "marimo",
        "--with", "nsqip-tools",
        "--with", "ncdb-tools",
        "--with", "polars",
        "--with", "matplotlib", 
        "--with", "seaborn",
        "marimo"
    ] + args
    
    # Run the command
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def main():
    """Main entry point."""
    # Check if any arguments provided
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Handle help command
    if command in ["help", "-h", "--help"]:
        print_usage()
        sys.exit(0)
    
    # Check uv is installed for all other commands
    if not check_uv_installed():
        sys.exit(1)
    
    # Handle different commands
    if command == "edit":
        if len(sys.argv) < 3:
            print("Error: Please specify a notebook file to edit")
            print("Example: ./db edit analysis.py")
            sys.exit(1)
        notebook = sys.argv[2]
        print(f"Opening {notebook} for editing...")
        run_marimo_command(["edit", notebook])
    
    elif command == "run":
        if len(sys.argv) < 3:
            print("Error: Please specify a notebook file to run")
            print("Example: ./db run analysis.py")
            sys.exit(1)
        notebook = sys.argv[2]
        print(f"Running {notebook} in read-only mode...")
        run_marimo_command(["run", notebook, "--sandbox"])
    
    elif command == "new":
        if len(sys.argv) < 3:
            print("Creating new notebook...")
            run_marimo_command(["new"])
        else:
            notebook = sys.argv[2]
            print(f"Creating new notebook: {notebook}")
            run_marimo_command(["new", notebook])
    
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()