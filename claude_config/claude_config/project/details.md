# Project Details - EDITABLE

**Project Name:** Clinical Database Collaborative Analysis Repository  
**Last Updated:** 2025-06-07  
**Primary Developer:** jabrant  
**Project Type:** Clinical Data Analysis Platform/Research Collaboration Tool

## Project Overview
This repository helps clinical researchers collaborate on analysis of major healthcare databases including NSQIP (National Surgical Quality Improvement Program) for surgical outcomes and NCDB (National Cancer Database) for cancer outcomes. It provides an organized framework for multiple researchers to work on clinical outcomes research while maintaining strict data security and HIPAA compliance. The platform is designed for researchers with limited programming experience, offering templates and tools to make data analysis accessible.

## Core Functionality
- **Project Organization**: Structured folders for individual researcher projects
- **Analysis Templates**: Pre-built marimo notebooks for common NSQIP and NCDB analyses
- **Data Security**: Automatic protection against uploading patient data
- **Collaboration Tools**: Git-based workflow for code sharing without data sharing
- **Helper Scripts**: Simplified command-line tools for notebook management

## Technology Stack
- **Primary Language:** Python 3.10+
- **Key Libraries:** 
  - nsqip-tools - NSQIP data loading and processing
  - ncdb-tools - NCDB data loading and processing
  - polars - High-performance dataframe operations
  - marimo - Interactive reactive notebooks
  - matplotlib/seaborn - Scientific visualization
  - uv - Fast Python package manager
- **Database:** Parquet files (via nsqip-tools)
- **External APIs:** None (all data is local)

## Domain Context
This project operates in the surgical quality improvement space:
- **Data Sources**: 
  - NSQIP - American College of Surgeons' surgical outcomes database
  - NCDB - Commission on Cancer's cancer outcomes database
- **Research Focus**: 
  - NSQIP: 30-day surgical outcomes, complications, mortality
  - NCDB: Cancer treatment patterns, survival, quality metrics
- **Users**: Surgical researchers, oncology researchers, residents, quality improvement teams
- **Typical Analyses**: 
  - NSQIP: Risk-adjusted surgical outcomes, complications, readmissions
  - NCDB: Cancer stage at diagnosis, treatment patterns, survival analysis

## Success Criteria
- [ ] Researchers can start new analyses within 10 minutes
- [ ] Zero patient data exposure incidents
- [ ] Support for 5+ concurrent researcher projects
- [ ] Templates cover 80% of common NSQIP and NCDB analyses
- [ ] Non-programmers can successfully complete analyses

## Constraints
- **Performance:** Must handle datasets with 1M+ surgical cases
- **Security:** No patient identifiers in repository, all data local
- **Compliance:** HIPAA compliant, IRB approved for multi-institutional use
- **Timeline:** Ongoing collaborative project, no fixed deadline

## Related Documentation
- NSQIP User Guide: `shared/docs/nsqip_puf_userguide_2022.pdf`
- Pediatric NSQIP Guide: `shared/docs/peds_nsqip_userguide_2023.pdf`
- nsqip-tools Documentation: `shared/docs/nsqip_tools_README.md`
- Git Basics Guide: `shared/docs/git-basics-guide.md`
- ACS NSQIP Website: https://www.facs.org/quality-programs/data-and-registries/acs-nsqip/