# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.3",
#     "nsqip-tools==0.2.2",
#     "numpy==2.3.1",
#     "polars==1.31.0",
#     "scikit-learn==1.7.1",
#     "seaborn==0.13.2",
# ]
# ///

import marimo

__generated_with = "0.14.12"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import nsqip_tools
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegressionCV
    from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
    import warnings
    warnings.filterwarnings('ignore')

    return Path, mo, np, pl, plt, sns


@app.cell
def _(np):
    np.random.seed(2)
    return


@app.cell
def _(plt, sns):
    # Configure plotting style
    plt.style.use('seaborn-v0_8')
    sns.set_palette('husl')
    return


@app.cell
def _(mo):
    mo.md(
        """
    # Tonsillectomy Mortality Analysis

    ## Analysis Overview
    This notebook analyzes 30-day mortality outcomes for tonsillectomy procedures:
    - **CPT 42821**: Tonsillectomy and adenoidectomy; age 12 or over
    - **CPT 42826**: Tonsillectomy, primary or secondary; age 12 or over

    We'll filter for cases with ONLY these CPT codes (no concurrent procedures), analyze descriptive 
    statistics, and build a regularized logistic regression model to identify mortality risk factors.
    """
    )
    return


@app.cell
def _(Path, pl):
    # Load NSQIP data directly with polars

    DATA_PATH = Path("/home/brantlab/projects/clinical-db-analysis/data/adult_nsqip_parquet")

    # CPT codes for tonsillectomy procedures (age 12+)
    target_cpts = ["42821", "42826"]

    # Load all parquet files with proper null handling
    df = (
      pl.scan_parquet(
          DATA_PATH / "*.parquet",
          # Tell polars to treat these as null values
          null_values=[" ", "", "NULL", "null", "NA", "N/A", "#N/A"],
          # Try to infer the schema more aggressively
          try_parse_dates=True
      )
      .filter(
          # Filter for cases with exactly one CPT code
          (pl.col("ALL_CPT_CODES").list.len() == 1) &
          # And that CPT code is one of our targets
          (pl.col("ALL_CPT_CODES").list.first().is_in(target_cpts))
      )
      .collect()
    )
    return


app._unparsable_cell(
    r"""
    # Display summary statistics
      n_total = len(df)
      n_42821 = len(df.filter(pl.col(\"CPT\") == \"42821\"))
      n_42826 = len(df.filter(pl.col(\"CPT\") == \"42826\"))
      mortality_rate = df[\"DEATH30\"].mean()

      mo.md(f\"\"\"
      ### Data Summary
      - Total cases with only tonsillectomy: **{n_total:,}**
      - CPT 42821 (Tonsillectomy & adenoidectomy): **{n_42821:,}**
      - CPT 42826 (Tonsillectomy only): **{n_42826:,}**
      - 30-day mortality rate: **{mortality_rate:.2%}**
      \"\"\")
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
