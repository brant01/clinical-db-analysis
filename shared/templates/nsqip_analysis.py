# ---
# title: NSQIP Basic Analysis Template
# description: Starting template for NSQIP surgical outcomes analysis
# marimo-version: 0.13.15
# ---

# Import required packages
# When running with "uv run marimo edit --sandbox", these will be automatically installed
import marimo as mo
import polars as pl
import nsqip_tools
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import our helper utilities
# The helper functions are optional - uncomment if you want to use them
# import sys
# sys.path.append(str(Path(__file__).parent.parent.parent / "shared" / "utils"))
# from nsqip_helpers import *

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
    # NSQIP Analysis Template
    
    ## About This Template
    
    This template provides a starting point for analyzing **Adult NSQIP** surgical outcomes data.
    It includes interactive controls, standard quality metrics, and publication-ready visualizations.
    
    ### Key Features:
    - Interactive parameter selection for CPT codes and years
    - Automatic calculation of standard NSQIP quality outcomes
    - Risk stratification by ASA class
    - Export functions for research datasets
    - Integration with optional helper functions
    
    ## Step 1: Configure Your Data Path
    
    Update the DATA_PATH below to point to your institution's NSQIP parquet dataset.
    This path should contain the parquet files created by nsqip_tools.
    """)
    
    # UPDATE THIS PATH to your institution's data location
    # Examples:
    # Mac/Linux: "/Users/username/nsqip_data/adult_nsqip_parquet"
    # Windows: "C:/Users/username/nsqip_data/adult_nsqip_parquet"
    # Network: "//server/share/nsqip_data/adult_nsqip_parquet"
    
    DATA_PATH = "/path/to/your/nsqip_parquet_dataset"
    
    # Verify the path exists
    data_path = Path(DATA_PATH)
    if not data_path.exists():
        mo.md(f"""
        **ERROR**: Data path not found!
        
        Please update DATA_PATH to point to your NSQIP parquet dataset.
        Current path: {DATA_PATH}
        """).callout(kind="danger")
        mo.stop()
    
    mo.md(f"""
    Data path confirmed: {DATA_PATH}
    """).callout(kind="success")
    
    return DATA_PATH, data_path

# --------------------------------------------------
# CELL 2: Define Research Parameters with Interactive Selection
# --------------------------------------------------
@app.cell
def parameters():
    """
    Define your research parameters with interactive controls
    """
    mo.md("""
    ## Step 2: Define Your Research Parameters
    
    Use the controls below to configure your analysis.
    """)
    
    # Common CPT code options
    common_cpt_codes = {
        "44970": "Laparoscopic appendectomy",
        "47562": "Laparoscopic cholecystectomy",
        "44140": "Colectomy",
        "44204": "Laparoscopic colectomy",
        "49505": "Inguinal hernia repair",
        "43280": "Laparoscopic fundoplication"
    }
    
    # Create interactive selectors
    cpt_selector = mo.ui.multiselect(
        options=list(common_cpt_codes.keys()),
        value=["44970", "47562"],
        label="Select CPT Codes"
    )
    
    year_selector = mo.ui.multiselect(
        options=[2019, 2020, 2021, 2022, 2023],
        value=[2021, 2022],
        label="Select Years"
    )
    
    # Display controls
    mo.md(f"""
    ### Configure Your Analysis:
    
    {cpt_selector}
    
    {year_selector}
    """)
    
    # Get selected values
    CPT_CODES = cpt_selector.value
    YEARS = year_selector.value
    DIAGNOSIS_CODES = []  # Can add interactive selector if needed
    
    # Display selected parameters
    if CPT_CODES and YEARS:
        selected_cpts = [f"{code} ({common_cpt_codes.get(code, 'Custom')})" for code in CPT_CODES]
        mo.md(f"""
        ### Selected Parameters:
        - **CPT Codes**: {', '.join(selected_cpts)}
        - **Years**: {', '.join(map(str, YEARS))}
        - **Diagnosis Codes**: {', '.join(DIAGNOSIS_CODES) if DIAGNOSIS_CODES else 'None'}
        """)
    else:
        mo.md("**Please select at least one CPT code and year to continue**").callout(kind="warning")
    
    return CPT_CODES, YEARS, DIAGNOSIS_CODES, cpt_selector, year_selector

# --------------------------------------------------
# CELL 3: Load and Filter Data
# --------------------------------------------------
@app.cell
def load_data(DATA_PATH, CPT_CODES, YEARS, DIAGNOSIS_CODES):
    """
    Load NSQIP data using nsqip_tools
    """
    mo.md("""
    ## Step 3: Load and Filter Data
    
    Using nsqip_tools to efficiently load and filter the data.
    """)
    
    # Check if parameters are selected
    if not CPT_CODES or not YEARS:
        mo.md("**Please select CPT codes and years above to load data**").callout(kind="info")
        mo.stop()
    
    # Initialize variables
    df = None
    query_info = None
    
    try:
        # Build the query
        query = nsqip_tools.load_data(DATA_PATH)
        
        # Apply filters
        if CPT_CODES:
            query = query.filter_by_cpt(CPT_CODES)
        
        if YEARS:
            query = query.filter_by_year(YEARS)
            
        if DIAGNOSIS_CODES:
            query = query.filter_by_diagnosis(DIAGNOSIS_CODES)
        
        # Get information about the query before collecting
        query_info = query.describe()
        
        mo.md(f"""
        ### Query Information:
        - **Total rows matching criteria**: {query_info['total_rows']:,}
        - **Columns available**: {query_info['columns']}
        """)
        
        # Collect the data
        df = query.collect()
        
        mo.md(f"""
        ### Data Loaded Successfully!
        - **Cases loaded**: {len(df):,}
        - **Variables**: {len(df.columns)}
        """).callout(kind="success")
        
    except Exception as e:
        mo.md(f"""
        **ERROR loading data**: {str(e)}
        
        Common issues:
        1. Check that DATA_PATH points to a valid nsqip_tools parquet dataset
        2. Ensure you have access to the data location
        3. Verify CPT codes and years are valid
        """).callout(kind="danger")
        mo.stop()
    
    return df, query_info

# --------------------------------------------------
# CELL 4: Basic Data Overview
# --------------------------------------------------
@app.cell
def data_overview(df):
    """
    Provide basic overview of the loaded data
    """
    if df is None:
        mo.md("**No data loaded** - Please fix the data path above").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 4: Data Overview
    
    Basic information about your dataset.
    """)
    
    # Get basic statistics
    total_cases = len(df)
    
    # Year distribution
    year_counts = df.group_by("OPERYR").agg(pl.count()).sort("OPERYR")
    
    # CPT distribution  
    cpt_counts = df.group_by("CPT").agg(pl.count()).sort("count", descending=True)
    
    # Age statistics (using AGE_AS_INT for numeric operations)
    age_stats = df.select([
        pl.col("AGE_AS_INT").mean().alias("mean_age"),
        pl.col("AGE_AS_INT").median().alias("median_age"),
        pl.col("AGE_AS_INT").std().alias("std_age")
    ]).to_dicts()[0]
    
    # Gender distribution
    gender_counts = df.group_by("SEX").agg(pl.count())
    
    # Create overview display
    mo.md(f"""
    ### Dataset Summary:
    
    **Total Cases**: {total_cases:,}
    
    **Age**: Mean = {age_stats['mean_age']:.1f}, Median = {age_stats['median_age']:.0f}, SD = {age_stats['std_age']:.1f}
    
    **Cases by Year**:
    {year_counts.to_pandas().to_markdown(index=False)}
    
    **Top CPT Codes**:
    {cpt_counts.head(5).to_pandas().to_markdown(index=False)}
    
    **Gender Distribution**:
    {gender_counts.to_pandas().to_markdown(index=False)}
    """)
    
    return year_counts, cpt_counts, age_stats, gender_counts

# --------------------------------------------------
# CELL 5: Calculate Key Outcomes
# --------------------------------------------------
@app.cell
def calculate_outcomes(df):
    """
    Calculate standard NSQIP quality outcomes
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 5: Key Surgical Outcomes
    
    Calculating standard NSQIP quality measures.
    """)
    
    # Define outcome variables and their descriptions
    outcomes = {
        "DEATH30": "30-day Mortality",
        "READMISSION": "30-day Readmission", 
        "REOPERATION": "30-day Reoperation",
        "SSI": "Surgical Site Infection",
        "PNEUMONIA": "Pneumonia",
        "UTI": "Urinary Tract Infection",
        "DVT": "Deep Vein Thrombosis",
        "PE": "Pulmonary Embolism"
    }
    
    # Calculate rates for each outcome
    outcome_rates = {}
    
    for var, description in outcomes.items():
        if var in df.columns:
            # Calculate rate (assuming 1 = Yes, 0 = No)
            rate = (df.filter(pl.col(var) == 1).shape[0] / df.shape[0]) * 100
            n_events = df.filter(pl.col(var) == 1).shape[0]
            outcome_rates[description] = {
                "rate": rate,
                "n": n_events,
                "total": df.shape[0]
            }
    
    # Create summary table
    summary_data = []
    for outcome, data in outcome_rates.items():
        summary_data.append({
            "Outcome": outcome,
            "Events": data["n"],
            "Total": data["total"],
            "Rate (%)": f"{data['rate']:.2f}"
        })
    
    summary_df = pl.DataFrame(summary_data)
    
    mo.md(f"""
    ### Outcome Rates:
    
    {summary_df.to_pandas().to_markdown(index=False)}
    """)
    
    return outcome_rates, summary_df

# --------------------------------------------------
# CELL 6: Create Visualizations
# --------------------------------------------------
@app.cell
def create_plots(df, outcome_rates):
    """
    Create basic visualizations
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 6: Visualizations
    
    Basic plots for your analysis.
    """)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('NSQIP Analysis Summary', fontsize=16)
    
    # 1. Age distribution
    ax1 = axes[0, 0]
    age_data = df.select("AGE_AS_INT").to_pandas()
    ax1.hist(age_data["AGE_AS_INT"], bins=20, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Age (years)')
    ax1.set_ylabel('Number of Cases')
    ax1.set_title('Age Distribution')
    ax1.grid(True, alpha=0.3)
    
    # 2. Outcome rates bar chart
    ax2 = axes[0, 1]
    if outcome_rates:
        outcomes_list = list(outcome_rates.keys())
        rates = [outcome_rates[o]["rate"] for o in outcomes_list]
        
        bars = ax2.bar(range(len(outcomes_list)), rates, color='skyblue', edgecolor='navy')
        ax2.set_xticks(range(len(outcomes_list)))
        ax2.set_xticklabels(outcomes_list, rotation=45, ha='right')
        ax2.set_ylabel('Rate (%)')
        ax2.set_title('Outcome Rates')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{rate:.1f}%', ha='center', va='bottom')
    
    # 3. Cases by year
    ax3 = axes[1, 0]
    year_data = df.group_by("OPERYR").agg(pl.count()).sort("OPERYR")
    years = year_data.select("OPERYR").to_pandas()["OPERYR"]
    counts = year_data.select("count").to_pandas()["count"]
    
    ax3.bar(years, counts, color='lightgreen', edgecolor='darkgreen')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Number of Cases')
    ax3.set_title('Cases by Year')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. ASA class distribution (risk stratification)
    ax4 = axes[1, 1]
    if "ASA_CLASS" in df.columns:
        asa_data = df.group_by("ASA_CLASS").agg(pl.count()).sort("ASA_CLASS")
        asa_classes = asa_data.select("ASA_CLASS").to_pandas()["ASA_CLASS"]
        asa_counts = asa_data.select("count").to_pandas()["count"]
        
        ax4.bar(asa_classes, asa_counts, color='salmon', edgecolor='darkred')
        ax4.set_xlabel('ASA Class')
        ax4.set_ylabel('Number of Cases')
        ax4.set_title('ASA Class Distribution')
        ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    return fig

# --------------------------------------------------
# CELL 7: Export Results
# --------------------------------------------------
@app.cell
def export_results(df, summary_df):
    """
    Export results for publication
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 7: Export Results
    
    Save your results for publication or further analysis.
    """)
    
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Export options with better state management
    export_summary_btn = mo.ui.button(label="Export Summary Table to CSV")
    export_dataset_btn = mo.ui.button(label="Export Filtered Dataset")
    
    export_status = mo.md("")
    
    if export_summary_btn.value:
        # Export summary table
        output_file = results_dir / "outcome_summary.csv"
        summary_df.write_csv(output_file)
        export_status = mo.md(f"""
        ✅ **Summary exported successfully!**
        
        File saved to: `{output_file}`
        """).callout(kind="success")
    
    if export_dataset_btn.value:
        # Export filtered dataset (without PHI)
        safe_columns = [
            "OPERYR", "AGE_AS_INT", "SEX", "ASA_CLASS",
            "DEATH30", "READMISSION", "REOPERATION", "SSI",
            "PNEUMONIA", "UTI", "DVT", "PE"
        ]
        # Only include columns that exist in the dataframe
        export_columns = [col for col in safe_columns if col in df.columns]
        
        df_export = df.select(export_columns)
        output_file = results_dir / "analysis_dataset.parquet"
        df_export.write_parquet(output_file)
        export_status = mo.md(f"""
        ✅ **Dataset exported successfully!**
        
        File saved to: `{output_file}`
        Exported {len(df_export):,} rows with {len(export_columns)} columns
        """).callout(kind="success")
    
    mo.md(f"""
    ### Export Options:
    
    {export_summary_btn} {export_dataset_btn}
    
    {export_status}
    
    ### Data Privacy Note:
    
    The export functions above automatically exclude potentially identifying information.
    Always verify your institution's data sharing policies before exporting.
    """)
    
    return export_summary_btn, export_dataset_btn, export_status

# --------------------------------------------------
# CELL 8: Advanced Analysis Options
# --------------------------------------------------
@app.cell
def advanced_analysis(df):
    """
    Interactive advanced analysis options
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Advanced Analysis Options
    
    Select additional analyses to perform:
    """)
    
    # Create analysis options
    analysis_options = mo.ui.multiselect(
        options=[
            "Risk-adjusted outcomes",
            "Subgroup analysis",
            "Temporal trends",
            "Composite outcomes",
            "Length of stay analysis"
        ],
        value=[],
        label="Select Advanced Analyses"
    )
    
    mo.md(f"{analysis_options}")
    
    # Show relevant analysis based on selection
    if "Risk-adjusted outcomes" in analysis_options.value:
        mo.md("""
        ### Risk-Adjusted Analysis
        
        Consider adjusting for:
        - Age and sex
        - ASA class
        - Emergency status
        - Comorbidities (DIABETES, SMOKE, etc.)
        """)
    
    if "Temporal trends" in analysis_options.value:
        # Create temporal analysis
        yearly_outcomes = (
            df.group_by("OPERYR")
            .agg([
                pl.count().alias("n_cases"),
                (pl.col("DEATH30") == 1).sum().alias("deaths"),
                (pl.col("READMISSION") == 1).sum().alias("readmissions")
            ])
            .with_columns([
                (pl.col("deaths") / pl.col("n_cases") * 100).alias("mortality_rate"),
                (pl.col("readmissions") / pl.col("n_cases") * 100).alias("readmission_rate")
            ])
            .sort("OPERYR")
        )
        
        mo.md(f"""
        ### Temporal Trends
        
        {yearly_outcomes.to_pandas().to_markdown(index=False)}
        """)
    
    return analysis_options

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
    
    The repository includes helper functions for common NSQIP tasks.
    To use them, uncomment the import at the top of this notebook.
    
    ### Example: Calculate Composite SSI
    
    ```python
    # First, uncomment the helper imports at the top
    # Then you can use functions like:
    
    # Add composite SSI indicator
    df = calculate_composite_ssi(df)
    
    # Add serious morbidity indicator
    df = calculate_serious_morbidity(df)
    
    # Create age groups
    df = create_age_groups(df)
    
    # Filter to elective cases only
    elective_df = filter_elective_cases(df)
    ```
    
    ### Available Helper Functions:
    
    - `calculate_composite_ssi()` - Creates ANY_SSI indicator
    - `calculate_serious_morbidity()` - Creates composite morbidity
    - `filter_by_age()` - Filter by age range (handles days/years)
    - `create_age_groups()` - Standard age categories
    - `clean_asa_class()` - Simplify ASA to 1-5
    - `standardize_sex()` - Convert to M/F
    - `create_outcome_summary()` - Summary table of outcomes
    
    All functions auto-detect adult vs pediatric data!
    """)

# --------------------------------------------------
# CELL 11: Next Steps
# --------------------------------------------------
@app.cell
def next_steps():
    """
    Guidance for extending the analysis
    """
    mo.md("""
    ## Next Steps
    
    This template provides a starting point. Consider adding:
    
    ### 1. Risk Adjustment
    - Add comorbidity variables (DIABETES, SMOKE, etc.)
    - Calculate risk scores
    - Perform adjusted analyses
    
    ### 2. Subgroup Analysis
    - Compare outcomes by procedure type
    - Analyze by patient characteristics
    - Look at temporal trends
    
    ### 3. Statistical Testing
    - Compare groups using appropriate tests
    - Calculate confidence intervals
    - Perform regression analyses
    
    ### 4. Advanced Visualizations
    - Risk-adjusted funnel plots
    - Forest plots for subgroups
    - Time series analyses
    
    ### Example: Simple Group Comparison
    
    ```python
    # Compare mortality by emergency status
    emergency_mortality = (df
        .group_by("EMERGENT")
        .agg([
            pl.count().alias("n"),
            (pl.col("DEATH30") == 1).sum().alias("deaths")
        ])
        .with_columns(
            (pl.col("deaths") / pl.col("n") * 100).alias("mortality_rate")
        )
    )
    ```
    
    ### Getting Help
    
    - Check `shared/utils/` for helper functions
    - See `shared/docs/` for documentation
    - Review other projects for examples
    """)

# Run the app
if __name__ == "__main__":
    app.run()