# Project: 30-Day Mortality Risk Factors in Emergency Surgery

**Researcher**: Dr. Example Smith  
**Institution**: Example Medical Center  
**Date Started**: January 2025  
**Status**: In Progress

## Research Question

What patient factors are associated with increased 30-day mortality following emergency general surgery procedures?

### Primary Aim
Identify modifiable and non-modifiable risk factors for 30-day mortality in emergency surgery patients.

### Secondary Aims
1. Compare mortality rates across different emergency procedures
2. Develop a risk prediction model for clinical use
3. Analyze temporal trends in mortality rates

## Methods

### Study Design
Retrospective cohort study using NSQIP data from 2019-2022.

### Inclusion Criteria
- Adult patients (age ≥ 18 years)
- Emergency surgery cases (EMERGENT = "Yes")
- General surgery procedures (CPT codes 44xxx-49xxx)

### Exclusion Criteria
- Elective procedures
- Trauma cases
- Missing outcome data

### Primary Outcome
- 30-day mortality (variable: varies by year, see analysis notebook)

### Key Variables
- **Demographics**: Age, sex, race
- **Comorbidities**: ASA class, diabetes, smoking, COPD
- **Procedure**: CPT code, operative time
- **Complications**: SSI, pneumonia, sepsis

### Statistical Analysis
1. Descriptive statistics by mortality status
2. Univariate comparisons (chi-square, t-tests)
3. Multivariable logistic regression
4. Model validation using split-sample approach

## Files in This Project

- `analysis.py` - Main analysis notebook (Marimo)
- `exploratory/` - Initial data exploration
- `results/` - Tables and figures for publication
- `supplementary/` - Additional analyses

## Key Findings

*To be updated as analysis progresses*

1. Overall 30-day mortality rate: X.X%
2. Highest risk procedures: [TBD]
3. Independent risk factors: [TBD]

## Data Notes

- Using institution's NSQIP data path: [Set in notebook]
- Adult dataset only
- Years included have different variable names for some outcomes

## Next Steps

- [ ] Complete descriptive analysis
- [ ] Run regression models
- [ ] Internal validation
- [ ] Prepare manuscript tables

## References

1. ACS NSQIP User Guide 2022
2. [Relevant surgical literature]