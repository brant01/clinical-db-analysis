# Clinical Database Specifics

## NSQIP Data Characteristics

### Data Structure
- Outcomes are text strings (e.g., "No Complication", "Pneumonia")
- Adult and pediatric datasets have different variable names
- Years may have different variable availability
- Data is stored in parquet format via nsqip_tools

### Working with NSQIP Outcomes
```python
# Remember outcomes are text, not binary
# Example: checking for SSI
has_ssi = pl.col("SUPINFEC") != "No Complication"

# Multiple complications stored as separate columns
complications = ["SUPINFEC", "WNDINFD", "ORGSPCSSI"]
```

### Dataset Detection
```python
# Helper functions auto-detect dataset type using age columns
from nsqip_helpers import detect_dataset_type
dataset_type = detect_dataset_type(df)  # Returns "adult" or "pediatric"
```

### Common NSQIP Variables
- **Adult**: AGE_DAYS, OPERYR, DEATH30, READMISSION
- **Pediatric**: AGE_DAYS, OPERYR, DEATH30, READMISSION1
- **Outcomes**: Text strings, not 0/1 values

## NCDB Data Characteristics

### Data Structure
- Cancer registry data with staging information
- Treatment modalities tracked separately
- Survival data in different format than NSQIP
- Also stored in parquet format via ncdb_tools

### Working with NCDB Data
```python
# Vital status coding differs from NSQIP
alive = pl.col("VITAL_STATUS") == 1
dead = pl.col("VITAL_STATUS") == 0

# Stage information requires careful handling
stage_iv = pl.col("TNM_CLIN_STAGE_GROUP").str.contains("IV")
```

### Common NCDB Variables
- **Demographics**: AGE_AT_DX, SEX, RACE
- **Clinical**: PRIMARY_SITE, HISTOLOGY, GRADE
- **Treatment**: CHEMOTHERAPY, RADIATION, SURGERY
- **Outcomes**: VITAL_STATUS, DX_LASTCONTACT_DEATH_MONTHS

## Data Loading Best Practices

### Use LazyFrames for Exploration
```python
# Efficient data exploration
import polars as pl

# NSQIP
nsqip_df = pl.scan_parquet("/path/to/nsqip/*.parquet")
print(nsqip_df.columns)
sample = nsqip_df.head(100).collect()

# NCDB
ncdb_df = pl.scan_parquet("/path/to/ncdb/*.parquet")
print(ncdb_df.columns)
sample = ncdb_df.head(100).collect()
```

### Filter Early, Collect Late
```python
# Good: Filter before collecting
result = (nsqip_df
    .filter(pl.col("OPERYR") >= 2020)
    .filter(pl.col("CPT").is_in(["44970", "47562"]))
    .collect()
)

# Bad: Collect then filter
result = nsqip_df.collect()
result = result.filter(pl.col("OPERYR") >= 2020)
```

## Testing Requirements
- Test helper functions with both adult and pediatric NSQIP data
- Test with different years (variable availability changes)
- Verify text outcome handling
- Check for edge cases (missing data, unusual values)
- Ensure NCDB and NSQIP functions don't interfere