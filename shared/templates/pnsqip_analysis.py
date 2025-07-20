# ---
# title: P-NSQIP Pediatric Surgery Analysis Template
# description: Template for analyzing pediatric surgical outcomes using P-NSQIP data
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
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Set reproducible random seed
np.random.seed(42)

# Configure plotting defaults for pediatric-friendly visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create marimo app
app = mo.App()

# --------------------------------------------------
# CELL 1: Introduction and Configuration
# --------------------------------------------------
@app.cell
def introduction():
    """
    Introduction and data path configuration
    """
    mo.md("""
    # P-NSQIP Pediatric Surgery Analysis
    
    ## About This Template
    
    This template is specifically designed for analyzing **Pediatric NSQIP (P-NSQIP)** data, 
    focusing on surgical outcomes in children from newborns to adolescents.
    
    ### Key Features:
    - Age-appropriate groupings (neonatal, infant, child, adolescent)
    - Pediatric-specific outcomes and complications
    - Weight-based calculations for medication and fluid management
    - Interactive filtering by age groups and procedures
    - Pediatric-specific risk factors
    
    ## Step 1: Configure Your Data Path
    
    Update the DATA_PATH below to point to your institution's P-NSQIP parquet dataset.
    """)
    
    # UPDATE THIS PATH to your institution's P-NSQIP data location
    DATA_PATH = "/path/to/your/pnsqip_parquet_dataset"
    
    # Verify the path exists
    data_path = Path(DATA_PATH)
    if not data_path.exists():
        mo.md(f"""
        **ERROR**: Data path not found!
        
        Please update DATA_PATH to point to your P-NSQIP parquet dataset.
        Current path: {DATA_PATH}
        """).callout(kind="danger")
        mo.stop()
    
    mo.md(f"""
    ✅ Data path confirmed: {DATA_PATH}
    """).callout(kind="success")
    
    return DATA_PATH, data_path

# --------------------------------------------------
# CELL 2: Define Pediatric Age Groups
# --------------------------------------------------
@app.cell
def age_groups():
    """
    Define standard pediatric age groupings
    """
    mo.md("""
    ## Pediatric Age Groups
    
    Standard age categories used in pediatric surgery research:
    """)
    
    # Define age groups with boundaries in days and years
    PEDIATRIC_AGE_GROUPS = {
        "Neonate": {"min_days": 0, "max_days": 28, "description": "0-28 days"},
        "Infant": {"min_days": 29, "max_days": 365, "description": "29 days - 1 year"},
        "Toddler": {"min_years": 1, "max_years": 3, "description": "1-3 years"},
        "Preschool": {"min_years": 3, "max_years": 5, "description": "3-5 years"},
        "School Age": {"min_years": 5, "max_years": 12, "description": "5-12 years"},
        "Adolescent": {"min_years": 12, "max_years": 18, "description": "12-18 years"}
    }
    
    # Display age groups
    age_group_table = pl.DataFrame([
        {"Age Group": group, "Age Range": info["description"]}
        for group, info in PEDIATRIC_AGE_GROUPS.items()
    ])
    
    mo.md(f"""
    {age_group_table.to_pandas().to_markdown(index=False)}
    """)
    
    return PEDIATRIC_AGE_GROUPS

# --------------------------------------------------
# CELL 3: Research Parameters with Pediatric Focus
# --------------------------------------------------
@app.cell
def parameters(PEDIATRIC_AGE_GROUPS):
    """
    Define research parameters with pediatric-specific options
    """
    mo.md("""
    ## Step 2: Define Your Research Parameters
    
    Select pediatric procedures and age groups for your analysis.
    """)
    
    # Common pediatric CPT codes (examples - modify for your procedures)
    # These are some common pediatric procedures
    PEDIATRIC_CPT_CODES = {
        "44970": "Laparoscopic appendectomy",
        "49500": "Inguinal hernia repair, initial, age 6 months to < 5 years",
        "49505": "Inguinal hernia repair, initial, age 5 years or older",
        "43280": "Laparoscopic fundoplication",
        "44120": "Enterectomy, small intestine",
        "50546": "Laparoscopic nephrectomy",
        "44180": "Laparoscopic enterolysis"
    }
    
    # Select CPT codes for analysis
    CPT_CODES = ["44970", "49500", "49505"]  # Modify as needed
    
    # Years to analyze
    YEARS = [2021, 2022, 2023]
    
    # Age groups to include (modify as needed)
    INCLUDE_AGE_GROUPS = ["Infant", "Toddler", "Preschool", "School Age", "Adolescent"]
    
    # Display selected parameters
    mo.md(f"""
    ### Selected Parameters:
    
    **CPT Codes**: 
    {chr(10).join([f'- {code}: {PEDIATRIC_CPT_CODES.get(code, "Custom procedure")}' for code in CPT_CODES])}
    
    **Years**: {', '.join(map(str, YEARS))}
    
    **Age Groups**: {', '.join(INCLUDE_AGE_GROUPS)}
    """)
    
    return CPT_CODES, YEARS, INCLUDE_AGE_GROUPS, PEDIATRIC_CPT_CODES

# --------------------------------------------------
# CELL 4: Interactive Age Group Selector
# --------------------------------------------------
@app.cell
def age_selector(PEDIATRIC_AGE_GROUPS):
    """
    Create interactive age group selection
    """
    mo.md("""
    ## Interactive Age Group Selection
    
    Use the checkboxes below to filter by specific age groups:
    """)
    
    # Create checkboxes for each age group
    age_checkboxes = {
        group: mo.ui.checkbox(value=True, label=f"{group} ({info['description']})")
        for group, info in PEDIATRIC_AGE_GROUPS.items()
    }
    
    # Display checkboxes
    checkbox_display = mo.vstack([cb for cb in age_checkboxes.values()])
    
    mo.md(f"""
    {checkbox_display}
    """)
    
    return age_checkboxes

# --------------------------------------------------
# CELL 5: Load and Filter P-NSQIP Data
# --------------------------------------------------
@app.cell
def load_data(DATA_PATH, CPT_CODES, YEARS, age_checkboxes):
    """
    Load P-NSQIP data with pediatric-specific handling
    """
    mo.md("""
    ## Step 3: Load and Filter Data
    
    Loading P-NSQIP data with pediatric-specific filters...
    """)
    
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
        
        # Get query information
        query_info = query.describe()
        
        # Collect the data
        df = query.collect()
        
        # Apply age group filtering based on checkboxes
        selected_groups = [group for group, cb in age_checkboxes.items() if cb.value]
        
        mo.md(f"""
        ### Data Loading Results:
        - **Total cases before age filtering**: {len(df):,}
        - **Selected age groups**: {', '.join(selected_groups)}
        """)
        
        # Apply age group filtering based on selected groups
        if "AGE_DAYS" in df.columns and selected_groups:
            # Create age group conditions
            age_conditions = []
            
            for group in selected_groups:
                group_info = PEDIATRIC_AGE_GROUPS[group]
                if "min_days" in group_info:
                    # Handle age in days
                    min_days = group_info["min_days"]
                    max_days = group_info["max_days"]
                    age_conditions.append(
                        (pl.col("AGE_DAYS") >= min_days) & (pl.col("AGE_DAYS") <= max_days)
                    )
                elif "min_years" in group_info:
                    # Convert years to days for consistency
                    min_days = group_info["min_years"] * 365.25
                    max_days = group_info["max_years"] * 365.25
                    age_conditions.append(
                        (pl.col("AGE_DAYS") >= min_days) & (pl.col("AGE_DAYS") < max_days)
                    )
            
            # Apply the combined filter
            if age_conditions:
                combined_condition = age_conditions[0]
                for condition in age_conditions[1:]:
                    combined_condition = combined_condition | condition
                
                df = df.filter(combined_condition)
        
        mo.md(f"""
        ### Data Loaded Successfully!
        - **Cases loaded**: {len(df):,}
        - **Variables**: {len(df.columns)}
        """).callout(kind="success")
        
    except Exception as e:
        mo.md(f"""
        **ERROR loading data**: {str(e)}
        
        Please check:
        1. DATA_PATH points to a valid P-NSQIP parquet dataset
        2. You have access to the data location
        3. CPT codes and years are valid
        """).callout(kind="danger")
        mo.stop()
    
    return df, query_info, selected_groups

# --------------------------------------------------
# CELL 6: Pediatric-Specific Data Overview
# --------------------------------------------------
@app.cell
def pediatric_overview(df):
    """
    Provide pediatric-specific overview of the data
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 4: Pediatric Data Overview
    
    Key demographics and characteristics for pediatric surgical patients.
    """)
    
    total_cases = len(df)
    
    # Age distribution - handle both AGE_AS_INT and AGE_DAYS if available
    if "AGE_DAYS" in df.columns:
        # For neonates and infants, days are more meaningful
        age_stats = df.select([
            pl.col("AGE_DAYS").mean().alias("mean_age_days"),
            pl.col("AGE_DAYS").median().alias("median_age_days"),
            (pl.col("AGE_DAYS") / 365.25).mean().alias("mean_age_years")
        ]).to_dicts()[0]
        
        mo.md(f"""
        **Age Statistics**:
        - Mean age: {age_stats['mean_age_days']:.0f} days ({age_stats['mean_age_years']:.1f} years)
        - Median age: {age_stats['median_age_days']:.0f} days
        """)
    
    # Weight statistics (important for pediatrics)
    if "WEIGHT" in df.columns:
        weight_stats = df.select([
            pl.col("WEIGHT").mean().alias("mean_weight"),
            pl.col("WEIGHT").median().alias("median_weight"),
            pl.col("WEIGHT").min().alias("min_weight"),
            pl.col("WEIGHT").max().alias("max_weight")
        ]).to_dicts()[0]
        
        mo.md(f"""
        **Weight Statistics** (kg):
        - Mean: {weight_stats['mean_weight']:.1f} kg
        - Median: {weight_stats['median_weight']:.1f} kg
        - Range: {weight_stats['min_weight']:.1f} - {weight_stats['max_weight']:.1f} kg
        """)
    
    # Prematurity (if available)
    if "PREM_BIRTH" in df.columns:
        prem_count = df.filter(pl.col("PREM_BIRTH") == 1).shape[0]
        prem_rate = (prem_count / total_cases) * 100
        mo.md(f"""
        **Prematurity**: {prem_count} cases ({prem_rate:.1f}%)
        """)
    
    # ASA class distribution
    if "ASA_CLASS" in df.columns:
        asa_dist = df.group_by("ASA_CLASS").agg(
            pl.count().alias("count")
        ).sort("ASA_CLASS")
        
        mo.md(f"""
        **ASA Class Distribution**:
        {asa_dist.to_pandas().to_markdown(index=False)}
        """)
    
    return age_stats if 'age_stats' in locals() else None, weight_stats if 'weight_stats' in locals() else None

# --------------------------------------------------
# CELL 7: Calculate Pediatric-Specific Outcomes
# --------------------------------------------------
@app.cell
def pediatric_outcomes(df):
    """
    Calculate outcomes specific to pediatric surgery
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 5: Pediatric Surgical Outcomes
    
    Key quality measures for pediatric surgery:
    """)
    
    # Define pediatric-specific outcomes
    pediatric_outcomes = {
        # Standard outcomes
        "DEATH30": "30-day Mortality",
        "READMISSION": "30-day Readmission",
        "REOPERATION": "30-day Reoperation",
        
        # Infections
        "SSI": "Surgical Site Infection",
        "PNEUMONIA": "Pneumonia",
        "UTI": "Urinary Tract Infection",
        
        # Pediatric-specific
        "NEURODEF": "Neurologic Deficit",
        "SEIZURE": "Postoperative Seizure",
        "UNPLANNED_INTUB": "Unplanned Intubation",
        "CARDIAC_ARREST": "Cardiac Arrest",
        
        # Respiratory (important in pediatrics)
        "VENTILATOR_DAYS": "Prolonged Ventilation (>48h)",
        "REINTUBATION": "Reintubation"
    }
    
    # Calculate rates
    outcome_rates = {}
    
    for var, description in pediatric_outcomes.items():
        if var in df.columns:
            if var == "VENTILATOR_DAYS":
                # Special handling for ventilator days
                rate = (df.filter(pl.col(var) > 2).shape[0] / df.shape[0]) * 100
                n_events = df.filter(pl.col(var) > 2).shape[0]
            else:
                # Standard binary outcomes
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
    
    **Note**: Rates are unadjusted. Consider age and weight when interpreting outcomes in pediatric patients.
    """)
    
    return outcome_rates, summary_df

# --------------------------------------------------
# CELL 8: Create Pediatric-Focused Visualizations
# --------------------------------------------------
@app.cell
def pediatric_visualizations(df, outcome_rates, selected_groups):
    """
    Create visualizations specific to pediatric data
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 6: Pediatric Surgery Visualizations
    
    Interactive plots designed for pediatric surgical data.
    """)
    
    # Create figure with pediatric-specific plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('P-NSQIP Pediatric Surgery Analysis', fontsize=16)
    
    # 1. Age distribution (in appropriate units)
    ax1 = axes[0, 0]
    if "AGE_DAYS" in df.columns and df.select(pl.col("AGE_DAYS").max())[0, 0] < 365:
        # If mostly infants, show in days
        age_data = df.select("AGE_DAYS").to_pandas()
        ax1.hist(age_data["AGE_DAYS"], bins=30, edgecolor='black', alpha=0.7, color='lightblue')
        ax1.set_xlabel('Age (days)')
        ax1.set_title('Age Distribution (Days)')
    elif "AGE_AS_INT" in df.columns:
        # Show in years for older children
        age_data = df.select("AGE_AS_INT").to_pandas()
        ax1.hist(age_data["AGE_AS_INT"], bins=18, range=(0, 18), edgecolor='black', alpha=0.7, color='lightblue')
        ax1.set_xlabel('Age (years)')
        ax1.set_title('Age Distribution (Years)')
    ax1.set_ylabel('Number of Cases')
    ax1.grid(True, alpha=0.3)
    
    # 2. Weight distribution (important for pediatrics)
    ax2 = axes[0, 1]
    if "WEIGHT" in df.columns:
        weight_data = df.select("WEIGHT").to_pandas()
        ax2.hist(weight_data["WEIGHT"], bins=30, edgecolor='black', alpha=0.7, color='lightgreen')
        ax2.set_xlabel('Weight (kg)')
        ax2.set_ylabel('Number of Cases')
        ax2.set_title('Weight Distribution')
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'Weight data not available', ha='center', va='center')
        ax2.set_title('Weight Distribution')
    
    # 3. Key pediatric outcomes
    ax3 = axes[1, 0]
    if outcome_rates:
        # Select key pediatric outcomes to display
        key_outcomes = ["30-day Mortality", "30-day Readmission", "Unplanned Intubation", 
                       "Surgical Site Infection", "Pneumonia"]
        
        display_outcomes = {k: v for k, v in outcome_rates.items() if k in key_outcomes}
        
        if display_outcomes:
            outcomes_list = list(display_outcomes.keys())
            rates = [display_outcomes[o]["rate"] for o in outcomes_list]
            
            bars = ax3.bar(range(len(outcomes_list)), rates, color='coral', edgecolor='darkred')
            ax3.set_xticks(range(len(outcomes_list)))
            ax3.set_xticklabels(outcomes_list, rotation=45, ha='right')
            ax3.set_ylabel('Rate (%)')
            ax3.set_title('Key Pediatric Outcomes')
            ax3.grid(True, alpha=0.3, axis='y')
            
            # Add value labels
            for bar, rate in zip(bars, rates):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{rate:.1f}%', ha='center', va='bottom')
    
    # 4. Operation time by age group (if available)
    ax4 = axes[1, 1]
    if "OP_TIME" in df.columns:
        # Create age categories for visualization
        age_categories = []
        if "AGE_AS_INT" in df.columns:
            age_data = df.select("AGE_AS_INT", "OP_TIME").to_pandas()
            age_data['Age_Group'] = pd.cut(age_data['AGE_AS_INT'], 
                                          bins=[0, 1, 5, 12, 18],
                                          labels=['<1 yr', '1-5 yr', '5-12 yr', '12-18 yr'])
            
            age_data.boxplot(column='OP_TIME', by='Age_Group', ax=ax4)
            ax4.set_xlabel('Age Group')
            ax4.set_ylabel('Operation Time (minutes)')
            ax4.set_title('Operation Time by Age Group')
            ax4.grid(True, alpha=0.3)
    else:
        ax4.text(0.5, 0.5, 'Operation time data not available', ha='center', va='center')
        ax4.set_title('Operation Time by Age Group')
    
    plt.tight_layout()
    
    return fig

# --------------------------------------------------
# CELL 9: Interactive Outcome Analysis
# --------------------------------------------------
@app.cell
def interactive_analysis(df, outcome_rates, PEDIATRIC_AGE_GROUPS):
    """
    Interactive outcome analysis tools
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Interactive Outcome Analysis
    
    Select specific outcomes to analyze in detail:
    """)
    
    # Create outcome selector
    available_outcomes = list(outcome_rates.keys()) if outcome_rates else []
    
    if not available_outcomes:
        mo.md("**No outcomes available for analysis**").callout(kind="info")
        mo.stop()
    
    outcome_selector = mo.ui.dropdown(
        options=available_outcomes,
        value=available_outcomes[0],
        label="Select Outcome to Analyze"
    )
    
    # Display selector
    mo.md(f"{outcome_selector}")
    
    # Analyze selected outcome
    selected_outcome = outcome_selector.value
    outcome_data = outcome_rates.get(selected_outcome, {})
    
    if outcome_data:
        mo.md(f"""
        ### {selected_outcome} Analysis
        
        - **Total Events**: {outcome_data['n']:,}
        - **Rate**: {outcome_data['rate']:.2f}%
        - **Total Cases**: {outcome_data['total']:,}
        """)
        
        # Age-stratified analysis if age data available
        if "AGE_DAYS" in df.columns:
            mo.md("""
            #### Age-Stratified Analysis
            
            Breaking down outcomes by age group helps identify high-risk populations.
            """)
    
    return outcome_selector

# --------------------------------------------------
# CELL 10: Export Pediatric Results
# --------------------------------------------------
@app.cell
def export_pediatric_results(df, summary_df):
    """
    Export results with pediatric-specific formatting
    """
    if df is None:
        mo.md("**No data loaded**").callout(kind="warning")
        mo.stop()
    
    mo.md("""
    ## Step 7: Export Results
    
    Save your pediatric surgery analysis results.
    """)
    
    # Create results directory
    results_dir = Path("results/pediatric")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Export buttons with better state management
    export_summary = mo.ui.button(label="Export Outcome Summary")
    export_age_stratified = mo.ui.button(label="Export Age-Stratified Results")
    export_dataset = mo.ui.button(label="Export Research Dataset")
    
    export_status = mo.md("")
    
    if export_summary.value:
        output_file = results_dir / "pediatric_outcome_summary.csv"
        summary_df.write_csv(output_file)
        export_status = mo.md(f"""
        ✅ Summary exported to: `{output_file}`
        """).callout(kind="success")
    
    if export_age_stratified.value:
        # Create age-stratified summary
        if "AGE_DAYS" in df.columns:
            age_outcome_summary = (
                df.with_columns(
                    pl.when(pl.col("AGE_DAYS") <= 28).then(pl.lit("Neonate"))
                    .when(pl.col("AGE_DAYS") <= 365).then(pl.lit("Infant"))
                    .when(pl.col("AGE_DAYS") <= 365*5).then(pl.lit("Young Child"))
                    .when(pl.col("AGE_DAYS") <= 365*12).then(pl.lit("Child"))
                    .otherwise(pl.lit("Adolescent"))
                    .alias("Age_Group")
                )
                .group_by("Age_Group")
                .agg([
                    pl.count().alias("N"),
                    (pl.col("DEATH30") == 1).sum().alias("Deaths") if "DEATH30" in df.columns else pl.lit(0).alias("Deaths"),
                    (pl.col("READMISSION") == 1).sum().alias("Readmissions") if "READMISSION" in df.columns else pl.lit(0).alias("Readmissions")
                ])
            )
            output_file = results_dir / "age_stratified_outcomes.csv"
            age_outcome_summary.write_csv(output_file)
            export_status = mo.md(f"""
            ✅ Age-stratified results exported to: `{output_file}`
            """).callout(kind="success")
        else:
            export_status = mo.md("""
            ⚠️ Age data not available for stratified analysis
            """).callout(kind="warning")
    
    if export_dataset.value:
        # Export research dataset without PHI
        safe_columns = [
            "OPERYR", "AGE_DAYS", "AGE_AS_INT", "SEX", "WEIGHT",
            "ASA_CLASS", "PREM_BIRTH", "DEATH30", "READMISSION", 
            "REOPERATION", "SSI", "UNPLANNED_INTUB", "NEURODEF",
            "SEIZURE", "CARDIAC_ARREST", "PNEUMONIA", "UTI"
        ]
        export_columns = [col for col in safe_columns if col in df.columns]
        
        pediatric_export = df.select(export_columns)
        output_file = results_dir / "pediatric_research_dataset.parquet"
        pediatric_export.write_parquet(output_file)
        export_status = mo.md(f"""
        ✅ Research dataset exported to: `{output_file}`
        Exported {len(pediatric_export):,} rows with {len(export_columns)} columns
        """).callout(kind="success")
    
    mo.md(f"""
    ### Export Options:
    
    {export_summary} {export_age_stratified} {export_dataset}
    
    {export_status}
    
    ### Data Privacy Note:
    
    All exports automatically exclude potentially identifying information.
    Always verify compliance with your institution's data sharing policies.
    """)
    
    return export_summary, export_age_stratified, export_dataset, export_status

# --------------------------------------------------
# CELL 11: Pediatric-Specific Guidance
# --------------------------------------------------
@app.cell
def pediatric_guidance():
    """
    Provide guidance specific to pediatric surgical analysis
    """
    mo.md("""
    ## Pediatric Surgery Analysis Guidelines
    
    ### Important Considerations for P-NSQIP Analysis:
    
    #### 1. Age-Appropriate Analysis
    - **Neonates** (0-28 days): Focus on congenital anomalies, birth weight
    - **Infants** (29 days-1 year): Consider feeding issues, failure to thrive
    - **Children** (1-12 years): Normal growth patterns, school attendance
    - **Adolescents** (12-18 years): Adult-like physiology, psychosocial factors
    
    #### 2. Weight-Based Calculations
    - Medication dosing per kg
    - Fluid requirements
    - Blood loss as percentage of estimated blood volume
    
    #### 3. Developmental Considerations
    - Premature birth history
    - Developmental delays
    - Congenital anomalies
    - Syndromic conditions
    
    #### 4. Family-Centered Outcomes
    - Parental satisfaction
    - Time away from school
    - Impact on siblings
    - Long-term developmental outcomes
    
    ### Common Pediatric Risk Factors to Consider:
    
    ```python
    # Example: Creating a prematurity-adjusted analysis
    if "PREM_BIRTH" in df.columns and "GEST_AGE" in df.columns:
        df = df.with_columns([
            (pl.col("GEST_AGE") < 37).alias("premature"),
            (pl.col("GEST_AGE") < 32).alias("very_premature"),
            (pl.col("GEST_AGE") < 28).alias("extremely_premature")
        ])
    ```
    
    ### Next Steps for Your Analysis:
    
    1. **Risk Stratification**
       - Consider age-weight percentiles
       - Account for congenital conditions
       - Include nutritional status
    
    2. **Outcome Benchmarking**
       - Compare to pediatric-specific benchmarks
       - Consider case-mix adjustment
       - Account for hospital volume
    
    3. **Quality Improvement**
       - Focus on preventable complications
       - Consider enhanced recovery protocols
       - Implement age-appropriate pain management
    """)

# --------------------------------------------------
# CELL 12: Resources and References
# --------------------------------------------------
@app.cell
def resources():
    """
    Provide pediatric surgery resources
    """
    mo.md("""
    ## Resources and References
    
    ### P-NSQIP Resources:
    - [ACS P-NSQIP Website](https://www.facs.org/quality-programs/childrens-surgery/childrens-surgery-quality/pediatric/)
    - P-NSQIP Operations Manual
    - Pediatric Risk Calculator
    
    ### Key References:
    1. Raval MV, et al. "Pediatric American College of Surgeons National Surgical Quality Improvement Program: feasibility of a novel, prospective assessment of surgical outcomes." J Pediatr Surg. 2011.
    
    2. Bruny JL, et al. "American College of Surgeons National Surgical Quality Improvement Program Pediatric: a beta phase report." J Pediatr Surg. 2013.
    
    ### Statistical Considerations:
    - Small sample sizes in rare procedures
    - Age-stratified analysis requirements
    - Center effects in pediatric surgery
    
    ### Getting Help:
    - Check `shared/utils/` for pediatric-specific helper functions
    - Review other pediatric projects in the repository
    - Consult with pediatric surgery quality improvement team
    """)

# Run the app
if __name__ == "__main__":
    app.run()