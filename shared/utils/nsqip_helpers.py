"""
NSQIP Analysis Helper Functions

Common utilities for NSQIP data analysis using Polars.
These functions complement nsqip_tools for frequent analysis patterns.

Supports both adult and pediatric NSQIP datasets.
Functions automatically detect dataset type and preserve DataFrame/LazyFrame types.
"""

import polars as pl
from typing import Any, Literal, TypeVar, Union, Optional
from pathlib import Path

# Type variable to preserve DataFrame or LazyFrame type
FrameType = TypeVar('FrameType', pl.DataFrame, pl.LazyFrame)


def detect_dataset_type(
    df: Union[pl.DataFrame, pl.LazyFrame],
    dataset_type: Optional[Literal["adult", "pediatric"]] = None
) -> Literal["adult", "pediatric"]:
    """
    Detect whether dataset is adult or pediatric NSQIP.
    
    Args:
        df: Polars DataFrame or LazyFrame
        dataset_type: If provided, uses this instead of auto-detection
        
    Returns:
        "adult" or "pediatric"
        
    Raises:
        ValueError: If dataset type cannot be determined
    """
    if dataset_type is not None:
        return dataset_type
    
    # Get column names - works for both DataFrame and LazyFrame
    columns = df.columns
    
    # Most reliable indicator is the age column
    if "AGE_DAYS" in columns:
        return "pediatric"
    elif "AGE_AS_INT" in columns or "AGE" in columns:
        return "adult"
    else:
        raise ValueError(
            "Cannot determine dataset type (adult vs pediatric). "
            "No age columns found. "
            "Please specify dataset_type='adult' or dataset_type='pediatric'"
        )


def calculate_composite_ssi(
    df: FrameType,
    dataset_type: Optional[Literal["adult", "pediatric"]] = None
) -> FrameType:
    """
    Calculate composite SSI (Surgical Site Infection) outcome.
    
    Creates ANY_SSI binary indicator from SSI complication text fields.
    
    Args:
        df: Polars DataFrame or LazyFrame with SSI variables
        dataset_type: Force "adult" or "pediatric" (auto-detects if None)
        
    Returns:
        Same type as input with added ANY_SSI column (0/1)
        
    Example:
        >>> df = calculate_composite_ssi(df)
        >>> ssi_rate = df.filter(pl.col("ANY_SSI") == 1).count()
    """
    # SSI variables are same in both adult and pediatric
    ssi_vars = ["SUPINFEC", "WNDINFD", "ORGSPCSSI"]
    
    # Check which SSI columns exist
    ssi_cols = [col for col in ssi_vars if col in df.columns]
    
    if not ssi_cols:
        raise ValueError(f"No SSI columns found. Expected: {ssi_vars}")
    
    # Create expressions to check for SSI
    # Variables contain "No Complication" when no SSI, otherwise the SSI type
    ssi_exprs = [
        (pl.col(col) != "No Complication").cast(pl.Int8)
        for col in ssi_cols
    ]
    
    # ANY_SSI = 1 if any SSI occurred
    any_ssi_expr = pl.max_horizontal(ssi_exprs).fill_null(0).alias("ANY_SSI")
    
    return df.with_columns(any_ssi_expr)


def calculate_serious_morbidity(
    df: FrameType,
    dataset_type: Optional[Literal["adult", "pediatric"]] = None
) -> FrameType:
    """
    Calculate serious morbidity composite outcome.
    
    Creates binary indicator for any serious complication.
    
    Args:
        df: Polars DataFrame or LazyFrame
        dataset_type: Force "adult" or "pediatric" (auto-detects if None)
        
    Returns:
        Same type as input with added SERIOUS_MORBIDITY column (0/1)
    """
    # Common complications in both datasets (text format)
    common_complications = {
        "WNDINFD": "Deep Incisional SSI",      # Deep SSI
        "ORGSPCSSI": "Organ/Space SSI",        # Organ space SSI
        "OUPNEUMO": "Pneumonia",               # Pneumonia
        "URNINFEC": "Urinary Tract Infection", # UTI
    }
    
    # Build expressions for complications that exist
    comp_exprs = []
    
    # Check text-based complications
    for col, complication_text in common_complications.items():
        if col in df.columns:
            comp_exprs.append(
                (pl.col(col) == complication_text).cast(pl.Int8)
            )
    
    # Check Yes/No format variables
    yes_no_vars = []
    
    # Detect dataset type for specific variables
    ds_type = detect_dataset_type(df, dataset_type)
    
    if ds_type == "adult":
        # Adult specific
        yes_no_vars.extend(["REOPERATION1", "READMISSION1"])
        # Check for other serious complications (if they exist)
        other_checks = ["CDARREST", "CDMI", "CNSCVA", "RENAINSF", "OPRENAFL"]
    else:
        # Pediatric specific  
        yes_no_vars.extend(["REOPERATION", "READMISSION1"])
        # Check for other serious complications
        other_checks = ["CDARREST", "STROKE", "SEIZURE", "RENALFAIL"]
    
    # Add Yes/No checks
    for var in yes_no_vars:
        if var in df.columns:
            comp_exprs.append(
                (pl.col(var) == "Yes").cast(pl.Int8)
            )
    
    # Add numeric checks (these should be 1 for positive)
    for var in other_checks:
        if var in df.columns:
            comp_exprs.append(
                (pl.col(var) == 1).cast(pl.Int8)
            )
    
    if not comp_exprs:
        raise ValueError(f"No complication columns found in {ds_type} dataset")
    
    # Create composite serious morbidity
    morbidity_expr = pl.max_horizontal(comp_exprs).fill_null(0).alias("SERIOUS_MORBIDITY")
    
    return df.with_columns(morbidity_expr)


def filter_by_age(
    df: FrameType,
    min_age: Optional[float] = None,
    max_age: Optional[float] = None,
    dataset_type: Optional[Literal["adult", "pediatric"]] = None
) -> FrameType:
    """
    Filter cases by age range (in years).
    
    Args:
        df: Polars DataFrame or LazyFrame
        min_age: Minimum age in years
        max_age: Maximum age in years
        dataset_type: Force "adult" or "pediatric" (auto-detects if None)
        
    Returns:
        Filtered DataFrame or LazyFrame
        
    Example:
        >>> # Get patients 65 and older
        >>> elderly = filter_by_age(df, min_age=65)
        >>> # Get pediatric patients under 1 year
        >>> infants = filter_by_age(df, max_age=1)
    """
    # Detect dataset type
    ds_type = detect_dataset_type(df, dataset_type)
    
    if ds_type == "adult":
        # Use AGE_AS_INT (already in years)
        age_col = "AGE_AS_INT"
        if min_age is not None:
            df = df.filter(pl.col(age_col) >= min_age)
        if max_age is not None:
            df = df.filter(pl.col(age_col) <= max_age)
            
    else:
        # Pediatric: convert AGE_DAYS to years for filtering
        if min_age is not None:
            df = df.filter(pl.col("AGE_DAYS") >= (min_age * 365.25))
        if max_age is not None:
            df = df.filter(pl.col("AGE_DAYS") <= (max_age * 365.25))
    
    return df


def create_age_groups(
    df: FrameType,
    custom_bins: Optional[list[float]] = None,
    dataset_type: Optional[Literal["adult", "pediatric"]] = None
) -> FrameType:
    """
    Create age group categories for analysis.
    
    Args:
        df: Polars DataFrame or LazyFrame
        custom_bins: Custom age bins in years. If None, uses standard groupings.
        dataset_type: Force "adult" or "pediatric" (auto-detects if None)
        
    Returns:
        Same type as input with added AGE_GROUP column
    """
    # Detect dataset type
    ds_type = detect_dataset_type(df, dataset_type)
    
    if ds_type == "adult":
        if custom_bins is None:
            # Standard adult age groups
            bins = [0, 18, 40, 65, 80, 150]
            labels = ["<18", "18-39", "40-64", "65-79", "80+"]
        else:
            bins = custom_bins
            labels = []
            for i in range(len(bins) - 1):
                if i == len(bins) - 2:
                    labels.append(f"{int(bins[i])}+")
                else:
                    labels.append(f"{int(bins[i])}-{int(bins[i+1]-1)}")
        
        age_expr = pl.col("AGE_AS_INT").cut(bins, labels=labels).alias("AGE_GROUP")
        
    else:
        # Pediatric
        if custom_bins is None:
            # Standard pediatric age groups
            # Convert years to days for cutting
            bins_years = [0, 1/365.25, 30/365.25, 1, 2, 5, 12, 18, 100]
            bins = [b * 365.25 for b in bins_years]
            labels = ["<1d", "1-30d", "1mo-1y", "1-2y", "2-5y", "5-12y", "12-18y", "18+y"]
        else:
            # Convert custom bins from years to days
            bins = [b * 365.25 for b in custom_bins]
            labels = []
            for i in range(len(custom_bins) - 1):
                if custom_bins[i] < 1:
                    # Under 1 year - show in months or days
                    if custom_bins[i+1] <= 30/365.25:
                        labels.append(f"{int(custom_bins[i]*365.25)}-{int(custom_bins[i+1]*365.25)}d")
                    else:
                        labels.append(f"{int(custom_bins[i]*12)}-{int(custom_bins[i+1]*12)}mo")
                else:
                    # 1+ years
                    if i == len(custom_bins) - 2:
                        labels.append(f"{int(custom_bins[i])}+y")
                    else:
                        labels.append(f"{int(custom_bins[i])}-{int(custom_bins[i+1]-1)}y")
        
        age_expr = pl.col("AGE_DAYS").cut(bins, labels=labels).alias("AGE_GROUP")
    
    return df.with_columns(age_expr)


def clean_asa_class(df: FrameType) -> FrameType:
    """
    Clean ASA class to simple 1-5 categories.
    
    Handles different text formats in adult vs pediatric datasets.
    
    Args:
        df: Polars DataFrame or LazyFrame
        
    Returns:
        Same type as input with added ASA_SIMPLE column
    """
    if "ASACLAS" not in df.columns:
        raise ValueError("ASACLAS column not found")
    
    # Extract numeric ASA class from text
    # Handles formats like "2-Mild Disturb", "ASA 2 - Mild Disturb", etc.
    asa_expr = (
        pl.col("ASACLAS")
        .str.extract(r"(\d)", 1)  # Extract first digit
        .alias("ASA_SIMPLE")
    )
    
    return df.with_columns(asa_expr)


def calculate_bmi(df: FrameType) -> FrameType:
    """
    Calculate BMI from height and weight if not already present.
    
    Args:
        df: Polars DataFrame or LazyFrame
        
    Returns:
        Same type as input with BMI column added (if HEIGHT and WEIGHT exist)
    """
    if "BMI" in df.columns:
        return df
    
    if "HEIGHT" in df.columns and "WEIGHT" in df.columns:
        # BMI = weight(kg) / height(m)^2
        # NSQIP stores height in inches and weight in pounds
        bmi_expr = (
            (pl.col("WEIGHT") * 0.453592) / 
            ((pl.col("HEIGHT") * 0.0254) ** 2)
        ).alias("BMI")
        
        return df.with_columns(bmi_expr)
    else:
        return df


def standardize_sex(df: FrameType) -> FrameType:
    """
    Standardize sex/gender coding to M/F.
    
    Handles different capitalizations between adult and pediatric.
    
    Args:
        df: Polars DataFrame or LazyFrame
        
    Returns:
        Same type as input with SEX_STANDARD column
    """
    if "SEX" not in df.columns:
        return df
    
    sex_expr = (
        pl.col("SEX")
        .str.to_uppercase()
        .str.slice(0, 1)  # Just take first letter
        .alias("SEX_STANDARD")
    )
    
    return df.with_columns(sex_expr)


def get_surgery_year(df: FrameType) -> FrameType:
    """
    Extract surgery year as integer.
    
    Args:
        df: Polars DataFrame or LazyFrame
        
    Returns:
        Same type as input with SURGERY_YEAR column
    """
    year_col = "OPERYR" if "OPERYR" in df.columns else "ADMYR"
    
    if year_col in df.columns:
        year_expr = pl.col(year_col).cast(pl.Int32).alias("SURGERY_YEAR")
        return df.with_columns(year_expr)
    else:
        return df


def filter_elective_cases(df: FrameType) -> FrameType:
    """
    Filter to only elective (non-emergency) cases.
    
    Args:
        df: Polars DataFrame or LazyFrame
        
    Returns:
        Filtered DataFrame or LazyFrame
    """
    if "EMERGENT" in df.columns:
        # Standard variable name
        return df.filter(pl.col("EMERGENT") == "No")
    else:
        raise ValueError("EMERGENT column not found")


def create_outcome_summary(
    df: pl.DataFrame,  # Note: Requires DataFrame, not LazyFrame
    group_var: Optional[str] = None,
    dataset_type: Optional[Literal["adult", "pediatric"]] = None
) -> pl.DataFrame:
    """
    Create a summary table of common outcomes.
    
    Note: This function requires a collected DataFrame (not LazyFrame)
    because it needs to calculate percentages.
    
    Args:
        df: Polars DataFrame with outcome variables
        group_var: Optional grouping variable (e.g., "SURGERY_YEAR", "ASA_SIMPLE")
        dataset_type: Force "adult" or "pediatric" (auto-detects if None)
        
    Returns:
        Summary DataFrame with counts and rates
        
    Example:
        >>> # Overall summary
        >>> summary = create_outcome_summary(df.collect())
        >>> # By year
        >>> yearly = create_outcome_summary(df.collect(), group_var="SURGERY_YEAR")
    """
    if isinstance(df, pl.LazyFrame):
        raise TypeError(
            "create_outcome_summary requires a DataFrame. "
            "Call .collect() first."
        )
    
    # Detect dataset type
    ds_type = detect_dataset_type(df, dataset_type)
    
    # Define outcomes to summarize
    # Format: (column_name, positive_value, display_name)
    outcomes = [
        # SSI complications
        ("SUPINFEC", "Superficial Incisional SSI", "Superficial SSI"),
        ("WNDINFD", "Deep Incisional SSI", "Deep SSI"),
        ("ORGSPCSSI", "Organ/Space SSI", "Organ Space SSI"),
        # Other complications
        ("OUPNEUMO", "Pneumonia", "Pneumonia"),
        ("URNINFEC", "Urinary Tract Infection", "UTI"),
    ]
    
    # Add dataset-specific outcomes
    if ds_type == "adult":
        outcomes.extend([
            ("READMISSION1", "Yes", "Readmission"),
            ("REOPERATION1", "Yes", "Reoperation"),
        ])
    else:
        outcomes.extend([
            ("READMISSION1", "Yes", "Readmission"),
            ("REOPERATION", "Yes", "Reoperation"),
        ])
    
    # Build the summary
    results = []
    
    # Get groups if specified
    if group_var and group_var in df.columns:
        groups = df.select(pl.col(group_var).unique().sort()).to_series().to_list()
        
        for group in groups:
            group_df = df.filter(pl.col(group_var) == group)
            n_total = len(group_df)
            
            for col, positive_val, display_name in outcomes:
                if col in df.columns:
                    n_positive = len(group_df.filter(pl.col(col) == positive_val))
                    rate = (n_positive / n_total * 100) if n_total > 0 else 0
                    
                    results.append({
                        group_var: group,
                        "Outcome": display_name,
                        "N": n_positive,
                        "Total": n_total,
                        "Rate (%)": round(rate, 2)
                    })
    else:
        # Overall summary
        n_total = len(df)
        
        for col, positive_val, display_name in outcomes:
            if col in df.columns:
                n_positive = len(df.filter(pl.col(col) == positive_val))
                rate = (n_positive / n_total * 100) if n_total > 0 else 0
                
                results.append({
                    "Outcome": display_name,
                    "N": n_positive,
                    "Total": n_total,
                    "Rate (%)": round(rate, 2)
                })
    
    return pl.DataFrame(results)


def export_for_stats(
    df: pl.DataFrame,
    output_path: str | Path,
    format: Literal["csv", "parquet", "stata"] = "csv",
    include_vars: Optional[list[str]] = None
) -> None:
    """
    Export data for statistical analysis in other software.
    
    Converts string outcomes to binary numeric for easier analysis.
    
    Args:
        df: Polars DataFrame to export
        output_path: Path to save file
        format: Export format
        include_vars: List of variables to include (None = all)
        
    Example:
        >>> # Export key variables for regression
        >>> export_for_stats(
        ...     df,
        ...     "analysis_data.csv",
        ...     include_vars=["AGE_AS_INT", "SEX", "ASA_SIMPLE", "ANY_SSI", "SERIOUS_MORBIDITY"]
        ... )
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Select variables if specified
    if include_vars:
        df = df.select([col for col in include_vars if col in df.columns])
    
    # Convert string outcomes to binary
    # This is helpful for statistical software
    binary_conversions = {
        "SUPINFEC": ("Superficial Incisional SSI", "SUPINFEC_BINARY"),
        "WNDINFD": ("Deep Incisional SSI", "WNDINFD_BINARY"),
        "ORGSPCSSI": ("Organ/Space SSI", "ORGSPCSSI_BINARY"),
        "OUPNEUMO": ("Pneumonia", "PNEUMO_BINARY"),
        "URNINFEC": ("Urinary Tract Infection", "UTI_BINARY"),
    }
    
    for col, (positive_val, new_col) in binary_conversions.items():
        if col in df.columns:
            df = df.with_columns(
                (pl.col(col) == positive_val).cast(pl.Int8).alias(new_col)
            )
    
    # Export based on format
    if format == "csv":
        df.write_csv(output_path)
    elif format == "parquet":
        df.write_parquet(output_path)
    elif format == "stata":
        # Requires pandas/pyreadstat
        try:
            df.to_pandas().to_stata(output_path)
        except ImportError:
            raise ImportError(
                "Stata export requires pandas. "
                "Install with: uv add pandas pyreadstat"
            )
    
    print(f"Data exported to: {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Variables: {', '.join(df.columns)}")