# Project Details - Clinical Database Analysis

**Project Name:** Clinical Database Collaborative Analysis Repository  
**Last Updated:** 2025-01-21  
**Primary Developer:** Jason Brant  
**Project Type:** Research Analysis Platform

## Project Overview
A collaborative platform enabling clinical researchers to analyze surgical and cancer outcomes data using NSQIP (adult and pediatric) and NCDB databases. The platform provides interactive notebook templates, automated environment management, and secure collaboration without requiring data sharing.

## Core Functionality
- **Three specialized analysis templates:**
  - Adult NSQIP - General surgical outcomes analysis
  - Pediatric NSQIP - Pediatric-specific surgical analysis with age groupings
  - NCDB - Cancer outcomes and survival analysis
- **Interactive marimo notebooks** with reactive UI components for filtering and exploration
- **Automated package management** via uv in sandboxed environments
- **Simple three-step workflow:** clone → create project → analyze
- **Secure collaboration** through Git while keeping data local

## Technology Stack
- **Primary Language:** Python 3.8+
- **Key Libraries:** 
  - marimo - Interactive reactive notebooks
  - polars - High-performance dataframe operations
  - nsqip-tools - NSQIP data loading and filtering
  - ncdb-tools - NCDB data handling
  - matplotlib/seaborn - Visualization
- **Package Manager:** uv (for isolation and dependency management)
- **Version Control:** Git/GitHub

## Domain Context
**Medical Specialties:**
- General Surgery (NSQIP)
- Pediatric Surgery (P-NSQIP) 
- Oncology (NCDB)

**Research Areas:**
- Surgical outcomes and quality improvement
- Post-operative complications and mortality
- Cancer treatment patterns and survival
- Healthcare disparities
- Risk adjustment and modeling

**Data Sources:**
- American College of Surgeons NSQIP
- American College of Surgeons NCDB
- Institution-specific data extracts

## Success Criteria
- [x] Templates for all three databases (NSQIP, P-NSQIP, NCDB)
- [x] Interactive UI components in all templates
- [x] Simplified setup process (<10 minutes to first analysis)
- [x] Marimo best practices implemented
- [ ] Demo notebooks created
- [ ] User documentation complete
- [ ] First external collaborator onboarded

## Constraints
- **Performance:** Must handle datasets with millions of records
- **Security:** No PHI in repository, data stays local
- **Compliance:** HIPAA compliant, supports IRB requirements
- **Usability:** Must be accessible to non-programmers
- **Portability:** Cross-platform (Windows, Mac, Linux)

## Key Design Decisions
1. **Marimo over Jupyter:** Reactive programming model, better reproducibility
2. **Polars over Pandas:** Better performance for large clinical datasets
3. **Manual folder creation:** Simplicity over automation for beginners
4. **Templates not scripts:** Guide users while allowing customization
5. **Local data only:** Security and compliance prioritized

## Related Documentation
- Main README: `/README.md`
- Marimo Expert: `/claude_config/experts/domain_experts/marimo_expert.md`
- Data Handling Guidelines: `/claude_config/guidelines/data_handling.md`
- Templates: `/shared/templates/`