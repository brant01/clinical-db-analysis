# ---
# title: NCDB Analysis Template
# description: Starting template for NCDB cancer outcomes analysis
# marimo-version: 0.13.15
# ---

# Import required packages
# When running with ./db edit, these will be automatically installed
import marimo as mo
import polars as pl
import ncdb_tools
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import our helper utilities (optional - uncomment if you want to use them)
# import sys
# sys.path.append(str(Path(__file__).parent.parent.parent / "shared" / "utils"))
# from ncdb_helpers import *

# Set reproducible random seed
np.random.seed(42)

# Configure plotting defaults
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create marimo app
app = mo.App()

# --------------------------------------------------
# CELL 1: Configuration and Data Path
# --------------------------------------------------
@app.cell
def setup():
    """
    Configuration cell - UPDATE THE DATA_PATH for your institution
    """
    mo.md("""
    # NCDB Analysis Template
    
    ## About This Template
    
    This template provides a comprehensive starting point for analyzing **NCDB** cancer registry data.
    It includes interactive controls, survival analysis, and treatment pattern evaluation.
    
    ### Key Features:
    - Interactive cancer site and year selection
    - Demographic and clinical characteristics summary
    - Basic survival analysis with stage stratification
    - Treatment pattern analysis over time
    - Export functions for research datasets
    - Integration with optional helper functions
    
    ## Step 1: Configure Your Data Path
    
    Update the DATA_PATH below to point to your institution's NCDB parquet dataset.
    This path should contain the parquet files created by ncdb_tools.
    """)
    
    # UPDATE THIS PATH to your institution's data location
    # Examples:
    # Mac/Linux: "/Users/username/ncdb_data/ncdb_parquet"
    # Windows: "C:/Users/username/ncdb_data/ncdb_parquet"
    # Network: "//server/share/ncdb_data/ncdb_parquet"
    
    DATA_PATH = "/path/to/your/ncdb/parquet/dataset"
    
    # Verify the path exists
    data_path = Path(DATA_PATH)
    if not data_path.exists():
        mo.md(f"""
        **ERROR**: Data path not found!
        
        Please update DATA_PATH to point to your NCDB parquet dataset.
        Current path: {DATA_PATH}
        """).callout(kind="danger")
        mo.stop()
    
    mo.md(f"""
    Data path confirmed: {DATA_PATH}
    """).callout(kind="success")
    
    return DATA_PATH, data_path

# --------------------------------------------------
# CELL 2: Define Research Parameters
# --------------------------------------------------
@app.cell
def parameters():
    """
    Define your research parameters with interactive controls
    """
    mo.md("""
    ## Step 2: Define Your Research Parameters
    
    Use the controls below to configure your cancer cohort.
    """)
    
    # Common cancer site codes
    cancer_sites = {
        "Breast": ["C50.0", "C50.1", "C50.2", "C50.3", "C50.4", "C50.5", "C50.6", "C50.8", "C50.9"],
        "Lung": ["C34.0", "C34.1", "C34.2", "C34.3", "C34.8", "C34.9"],
        "Colorectal": ["C18.0", "C18.1", "C18.2", "C18.3", "C18.4", "C18.5", "C18.6", "C18.7", "C18.8", "C18.9", "C19.9", "C20.9"],
        "Prostate": ["C61.9"],
        "Pancreas": ["C25.0", "C25.1", "C25.2", "C25.3", "C25.4", "C25.7", "C25.8", "C25.9"]
    }
    
    # Create interactive selectors
    site_selector = mo.ui.dropdown(
        options=list(cancer_sites.keys()),
        value="Breast",
        label="Select Cancer Site"
    )
    
    year_selector = mo.ui.multiselect(
        options=[2016, 2017, 2018, 2019, 2020, 2021, 2022],
        value=[2019, 2020, 2021],
        label="Select Years"
    )
    
    behavior_selector = mo.ui.dropdown(
        options=[("3", "Malignant only"), ("2,3", "In situ and malignant")],
        value="3",
        label="Tumor Behavior"
    )
    
    # Display controls
    mo.md(f"""
    ### Configure Your Cohort:
    
    {site_selector}
    
    {year_selector}
    
    {behavior_selector}
    """)
    
    # Get selected values
    SITE_CODES = cancer_sites[site_selector.value]
    YEARS = year_selector.value
    BEHAVIOR = behavior_selector.value
    
    # Display selected parameters
    if SITE_CODES and YEARS:
        mo.md(f"""
        ### Selected Parameters:
        - **Cancer Site**: {site_selector.value}
        - **ICD-O-3 Codes**: {', '.join(SITE_CODES[:3])}{'...' if len(SITE_CODES) > 3 else ''}
        - **Years**: {', '.join(map(str, YEARS))}
        - **Behavior**: {dict(behavior_selector.options)[BEHAVIOR]}
        """)
    else:
        mo.md("**Please select at least one site and year to continue**").callout(kind="warning")
    
    return SITE_CODES, YEARS, BEHAVIOR, site_selector, year_selector, behavior_selector

# --------------------------------------------------
# CELL 3: Load and Filter Data
# --------------------------------------------------
@app.cell
def load_data(DATA_PATH, SITE_CODES, YEARS, BEHAVIOR):
    """
    Load NCDB data with selected filters
    """
    mo.md("""
    ## Step 3: Load and Filter Data
    
    Using ncdb_tools to efficiently load and filter the data.
    """)
    
    # Initialize variables
    df = None
    query_info = None
    
    try:
        # Build the query
        query = ncdb_tools.load_data(DATA_PATH)
        
        # Apply filters
        if SITE_CODES:
            query = query.filter_by_site(SITE_CODES)
        
        if YEARS:
            query = query.filter_by_year(YEARS)
        
        if BEHAVIOR:
            query = query.filter_by_behavior(BEHAVIOR)
        
        # Get information about the query before collecting
        query_info = query.describe()
        
        mo.md(f"""
        ### Query Information:
        - **Total rows matching criteria**: {query_info.get('total_rows', 'Unknown'):,}
        - **Available columns**: {query_info.get('columns', 'Unknown')}
        """)
        
        # Collect the data
        df = query.collect()
        
        # Display basic information
        n_patients = len(df)
        years = df["YEAR_OF_DIAGNOSIS"].unique().sort()
        
        mo.md(f"""
        ### Data Loaded Successfully!
        - **Patients loaded**: {n_patients:,}
        - **Variables**: {len(df.columns)}
        - **Years included**: {', '.join(map(str, years))}
        """).callout(kind="success")
        
    except Exception as e:
        mo.md(f"""
        **ERROR loading data**: {str(e)}
        
        Common issues:
        1. Check that DATA_PATH points to a valid ncdb_tools parquet dataset
        2. Ensure you have access to the data location
        3. Verify site codes and years are valid
        """).callout(kind="danger")
        mo.stop()
    
    return df, n_patients, query_info

# --------------------------------------------------
# CELL 4: Basic Demographics
# --------------------------------------------------
@app.cell
def demographics(df):
    """
    Display basic demographic information
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 4: Basic Demographics
    
    Overview of your study population:
    """)
    
    # Age distribution
    age_stats = df["AGE"].describe()
    
    # Sex distribution
    sex_counts = df["SEX"].value_counts().sort("SEX")
    
    # Race distribution
    race_counts = df["RACE"].value_counts().sort("count", descending=True)
    
    # Create demographic tables
    sex_table = sex_counts.with_columns([
        (pl.col("count") / pl.col("count").sum() * 100).round(1).alias("Percentage")
    ])
    
    race_table = race_counts.head(5).with_columns([
        (pl.col("count") / pl.col("count").sum() * 100).round(1).alias("Percentage")
    ])
    
    mo.md(f"""
    ### Patient Characteristics
    
    **Age**
    - Mean: {age_stats["mean"]:.1f} years
    - Median: {age_stats["50%"]:.0f} years
    - Range: {age_stats["min"]:.0f} - {age_stats["max"]:.0f} years
    
    **Sex Distribution**
    {sex_table.to_pandas().to_markdown(index=False)}
    
    **Race Distribution (Top 5)**
    {race_table.to_pandas().to_markdown(index=False)}
    """)
    
    return age_stats, sex_counts, race_counts, sex_table, race_table

# --------------------------------------------------
# CELL 5: Clinical Characteristics
# --------------------------------------------------
@app.cell
def clinical_chars(df):
    """
    Analyze clinical characteristics
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 5: Clinical Characteristics
    
    Key clinical variables for your cohort:
    """)
    
    # Stage distribution
    stage_counts = df["TNM_CLIN_STAGE_GROUP"].value_counts().sort("TNM_CLIN_STAGE_GROUP")
    
    # Grade distribution
    grade_counts = df["GRADE"].value_counts().sort("GRADE")
    
    # Histology
    histology_counts = df["HISTOLOGY"].value_counts().sort("count", descending=True).head(10)
    
    # Treatment summary
    surgery_pct = (df["RX_SUMM_SURG_PRIM_SITE"] != 0).mean() * 100
    chemo_pct = (df["RX_SUMM_CHEMO"] != 0).mean() * 100
    radiation_pct = (df["RX_SUMM_RADIATION"] != 0).mean() * 100
    
    mo.md(f"""
    ### Treatment Summary
    
    - **Surgery**: {surgery_pct:.1f}% of patients
    - **Chemotherapy**: {chemo_pct:.1f}% of patients  
    - **Radiation**: {radiation_pct:.1f}% of patients
    """)
    
    return stage_counts, grade_counts, histology_counts

# --------------------------------------------------
# CELL 6: Survival Analysis
# --------------------------------------------------
@app.cell
def survival_analysis(df):
    """
    Basic survival analysis
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 6: Survival Analysis
    
    Overall survival analysis for your cohort:
    """)
    
    # Calculate survival metrics
    # Filter to patients with known vital status and follow-up
    survival_df = df.filter(
        (pl.col("PUF_VITAL_STATUS") != 9) &  # Known vital status
        (pl.col("DX_LASTCONTACT_DEATH_MONTHS").is_not_null())
    )
    
    # Basic survival statistics
    died = (survival_df["PUF_VITAL_STATUS"] == 0).sum()
    alive = (survival_df["PUF_VITAL_STATUS"] == 1).sum()
    median_followup = survival_df.filter(pl.col("PUF_VITAL_STATUS") == 1)["DX_LASTCONTACT_DEATH_MONTHS"].median()
    
    mo.md(f"""
    ### Survival Summary
    
    - **Patients with follow-up**: {len(survival_df):,}
    - **Deaths**: {died:,} ({died/len(survival_df)*100:.1f}%)
    - **Alive**: {alive:,} ({alive/len(survival_df)*100:.1f}%)
    - **Median follow-up** (alive patients): {median_followup:.1f} months
    
    Note: For more detailed survival analysis, consider using survival analysis packages.
    """)
    
    # Simple survival plot by stage
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Group by stage and calculate survival rates
    stage_survival = (survival_df
                     .filter(pl.col("TNM_CLIN_STAGE_GROUP").is_in(["1", "2", "3", "4"]))
                     .group_by("TNM_CLIN_STAGE_GROUP")
                     .agg([
                         pl.count().alias("N"),
                         (pl.col("PUF_VITAL_STATUS") == 1).sum().alias("Alive"),
                     ])
                     .with_columns((pl.col("Alive") / pl.col("N") * 100).alias("Survival_Rate"))
                     .sort("TNM_CLIN_STAGE_GROUP"))
    
    if len(stage_survival) > 0:
        # Create bar plot
        stages = stage_survival["TNM_CLIN_STAGE_GROUP"].to_list()
        survival_rates = stage_survival["Survival_Rate"].to_list()
        
        bars = ax.bar(stages, survival_rates, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax.set_xlabel("Clinical Stage")
        ax.set_ylabel("Survival Rate (%)")
        ax.set_title("Survival Rate by Clinical Stage")
        ax.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, rate in zip(bars, survival_rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate:.1f}%', ha='center', va='bottom')
    else:
        ax.text(0.5, 0.5, 'Insufficient stage data for visualization', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Survival Rate by Clinical Stage")
    
    plt.tight_layout()
    
    return survival_df, died, alive, median_followup, fig

# --------------------------------------------------
# CELL 7: Interactive Analysis Options
# --------------------------------------------------
@app.cell
def interactive_analysis(df):
    """
    Interactive analysis options
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 7: Interactive Analysis Options
    
    Select additional analyses to perform:
    """)
    
    # Create analysis options
    analysis_options = mo.ui.multiselect(
        options=[
            "Stage-stratified survival",
            "Treatment patterns over time",
            "Facility volume analysis",
            "Insurance disparities",
            "Geographic variations"
        ],
        value=[],
        label="Select Additional Analyses"
    )
    
    mo.md(f"{analysis_options}")
    
    # Show relevant analysis based on selection
    if "Stage-stratified survival" in analysis_options.value:
        mo.md("""
        ### Stage-Stratified Survival Analysis
        
        Analyzing survival outcomes by clinical and pathologic stage...
        """)
        
        # Add stage-specific analysis here
    
    if "Treatment patterns over time" in analysis_options.value:
        # Analyze treatment trends
        treatment_trends = (
            df.group_by("YEAR_OF_DIAGNOSIS")
            .agg([
                pl.count().alias("n_patients"),
                (pl.col("RX_SUMM_SURG_PRIM_SITE") != 0).sum().alias("n_surgery"),
                (pl.col("RX_SUMM_CHEMO") != 0).sum().alias("n_chemo"),
                (pl.col("RX_SUMM_RADIATION") != 0).sum().alias("n_radiation")
            ])
            .with_columns([
                (pl.col("n_surgery") / pl.col("n_patients") * 100).alias("surgery_pct"),
                (pl.col("n_chemo") / pl.col("n_patients") * 100).alias("chemo_pct"),
                (pl.col("n_radiation") / pl.col("n_patients") * 100).alias("radiation_pct")
            ])
            .sort("YEAR_OF_DIAGNOSIS")
        )
        
        mo.md(f"""
        ### Treatment Patterns Over Time
        
        {treatment_trends.select(["YEAR_OF_DIAGNOSIS", "surgery_pct", "chemo_pct", "radiation_pct"]).to_pandas().to_markdown(index=False)}
        """)
    
    return analysis_options

# --------------------------------------------------
# CELL 8: Custom Analysis Space
# --------------------------------------------------
@app.cell
def custom_analysis():
    """
    Space for your custom analysis
    """
    mo.md("""
    ## Your Custom Analysis
    
    Add your specific analyses here. Some suggestions:
    
    - Multivariate regression models
    - Propensity score matching
    - Machine learning predictions
    - Competing risk analysis
    - Quality metric calculations
    
    ### Example: Simple Logistic Regression
    
    ```python
    # Example code structure
    from sklearn.linear_model import LogisticRegression
    
    # Prepare features and outcome
    features = ['AGE', 'SEX', 'GRADE', 'TNM_CLIN_STAGE_GROUP']
    outcome = 'DEATH_STATUS'
    
    # Create model and fit
    model = LogisticRegression()
    # model.fit(X, y)
    ```
    """)
    
    return

# --------------------------------------------------
# CELL 9: Export Results
# --------------------------------------------------
@app.cell
def export_results(df, age_stats, sex_table, race_table):
    """
    Export results and create summary report
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 8: Export Results
    
    Save your analysis results for publication or further analysis.
    """)
    
    # Create results directory
    results_dir = Path("results/ncdb")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Export buttons
    export_demographics = mo.ui.button(label="Export Demographics Summary")
    export_dataset = mo.ui.button(label="Export Research Dataset")
    export_survival = mo.ui.button(label="Export Survival Data")
    
    export_status = mo.md("")
    
    if export_demographics.value:
        # Create demographics summary
        demo_summary = pl.DataFrame({
            "Characteristic": ["N", "Age (mean)", "Age (median)", "Female (%)"],
            "Value": [
                f"{len(df):,}",
                f"{age_stats['mean']:.1f}",
                f"{age_stats['50%']:.0f}",
                f"{sex_table.filter(pl.col('SEX') == 2)['Percentage'][0]:.1f}" if len(sex_table.filter(pl.col('SEX') == 2)) > 0 else "N/A"
            ]
        })
        
        output_file = results_dir / "demographics_summary.csv"
        demo_summary.write_csv(output_file)
        export_status = mo.md(f"""
        ✅ Demographics exported to: `{output_file}`
        """).callout(kind="success")
    
    if export_dataset.value:
        # Export research dataset without PHI
        safe_columns = [
            "YEAR_OF_DIAGNOSIS", "AGE", "SEX", "RACE",
            "PRIMARY_SITE", "HISTOLOGY", "BEHAVIOR", "GRADE",
            "TNM_CLIN_STAGE_GROUP", "TNM_PATH_STAGE_GROUP",
            "RX_SUMM_SURG_PRIM_SITE", "RX_SUMM_RADIATION", "RX_SUMM_CHEMO",
            "PUF_VITAL_STATUS", "DX_LASTCONTACT_DEATH_MONTHS"
        ]
        export_columns = [col for col in safe_columns if col in df.columns]
        
        ncdb_export = df.select(export_columns)
        output_file = results_dir / "ncdb_research_dataset.parquet"
        ncdb_export.write_parquet(output_file)
        export_status = mo.md(f"""
        ✅ Research dataset exported to: `{output_file}`
        Exported {len(ncdb_export):,} rows with {len(export_columns)} columns
        """).callout(kind="success")
    
    if export_survival.value:
        # Export survival data
        survival_columns = [
            "PUF_VITAL_STATUS", "DX_LASTCONTACT_DEATH_MONTHS",
            "AGE", "SEX", "TNM_CLIN_STAGE_GROUP"
        ]
        survival_export_cols = [col for col in survival_columns if col in df.columns]
        
        survival_data = df.select(survival_export_cols)
        output_file = results_dir / "survival_data.csv"
        survival_data.write_csv(output_file)
        export_status = mo.md(f"""
        ✅ Survival data exported to: `{output_file}`
        """).callout(kind="success")
    
    mo.md(f"""
    ### Export Options:
    
    {export_demographics} {export_dataset} {export_survival}
    
    {export_status}
    
    ### Data Privacy Note:
    
    All exports automatically exclude potentially identifying information.
    Always verify compliance with your institution's data use agreements.
    """)
    
    return results_dir, export_demographics, export_dataset, export_survival, export_status

# --------------------------------------------------
# CELL 10: Using Helper Functions (Optional)
# --------------------------------------------------
@app.cell
def helper_examples():
    """
    Optional: Using the shared helper functions
    """
    mo.md("""
    ## Using Shared Helper Functions
    
    The repository includes helper functions for common NCDB tasks.
    To use them, uncomment the import at the top of this notebook.
    
    ### Example Helper Functions:
    
    ```python
    # First, uncomment the helper imports at the top
    # Then you can use functions like:
    
    # Calculate Charlson-Deyo comorbidity score
    df = calculate_charlson_deyo(df)
    
    # Create standard age groups
    df = create_age_groups(df, breaks=[40, 50, 60, 70, 80])
    
    # Calculate facility volume quartiles
    df = calculate_facility_volume(df)
    
    # Standardize stage groupings
    df = standardize_stage(df)
    ```
    
    ### Available Helper Functions:
    
    - `calculate_charlson_deyo()` - Comorbidity score
    - `create_age_groups()` - Standard age categories
    - `calculate_facility_volume()` - Hospital volume metrics
    - `standardize_stage()` - Clean stage variables
    - `calculate_time_to_treatment()` - Treatment delays
    - `identify_receipt_of_treatment()` - Treatment indicators
    
    Check the documentation in `shared/utils/ncdb_helpers.py` for details.
    """)

# --------------------------------------------------
# CELL 11: Next Steps and Resources
# --------------------------------------------------
@app.cell
def next_steps():
    """
    Guidance for extending the analysis
    """
    mo.md("""
    ## Next Steps
    
    This template provides a foundation for NCDB analysis. Consider adding:
    
    ### 1. Advanced Survival Analysis
    - Kaplan-Meier curves with log-rank tests
    - Cox proportional hazards models
    - Competing risk analysis
    - Landmark analysis for immortal time bias
    
    ### 2. Treatment Effectiveness
    - Propensity score matching
    - Instrumental variable analysis
    - Difference-in-differences for policy changes
    
    ### 3. Quality Metrics
    - Guideline concordance rates
    - Time to treatment initiation
    - Commission on Cancer quality measures
    
    ### 4. Disparities Research
    - Insurance status effects
    - Geographic access to care
    - Facility type comparisons
    - Social determinants of health
    
    ### Example: Simple Survival Curve
    
    ```python
    from lifelines import KaplanMeierFitter
    
    # Prepare survival data
    kmf = KaplanMeierFitter()
    kmf.fit(
        durations=df['DX_LASTCONTACT_DEATH_MONTHS'],
        event_observed=(df['PUF_VITAL_STATUS'] == 0)
    )
    
    # Plot survival curve
    kmf.plot_survival_function()
    plt.title('Overall Survival')
    plt.xlabel('Months from Diagnosis')
    plt.ylabel('Survival Probability')
    ```
    
    ### Resources:
    
    - [NCDB PUF Data Dictionary](https://www.facs.org/quality-programs/cancer/ncdb/puf)
    - [CoC Quality Measures](https://www.facs.org/quality-programs/cancer/ncdb/quality-measures)
    - Check `shared/docs/` for analysis guides
    - Review published NCDB studies for methodology
    """)

# Run the app
if __name__ == "__main__":
    app.run()