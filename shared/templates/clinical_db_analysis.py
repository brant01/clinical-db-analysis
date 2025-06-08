# ---
# title: Clinical Database Analysis Template
# description: Starting template for NSQIP and NCDB clinical outcomes analysis
# marimo-version: 0.13.15
# ---

# Import required packages
# When running with ./db edit, these will be automatically installed
import marimo as mo
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import database-specific tools based on your needs
# Uncomment the one you need:
# import nsqip_tools  # For NSQIP surgical outcomes data
# import ncdb_tools   # For NCDB cancer outcomes data

# Import our helper utilities (optional)
# import sys
# sys.path.append(str(Path(__file__).parent.parent.parent / "shared" / "utils"))
# from clinical_helpers import *

# Set reproducible random seed
np.random.seed(42)

# Configure plotting defaults
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create marimo app
app = mo.App()

# --------------------------------------------------
# CELL 1: Select Database Type
# --------------------------------------------------
@app.cell
def select_database():
    """
    Select which clinical database to analyze
    """
    mo.md("""
    # Clinical Database Analysis Template
    
    ## Step 1: Select Your Database
    
    Choose which clinical database you are analyzing:
    """)
    
    database_type = mo.ui.radio(
        ["NSQIP (Surgical Outcomes)", "NCDB (Cancer Outcomes)"],
        value="NSQIP (Surgical Outcomes)",
        label="Database Type:"
    )
    
    mo.md(f"""
    {database_type}
    
    You selected: **{database_type.value}**
    """)
    
    # Set database-specific variables
    if "NSQIP" in database_type.value:
        db_name = "NSQIP"
        import nsqip_tools as db_tools
    else:
        db_name = "NCDB"
        import ncdb_tools as db_tools
    
    return database_type, db_name, db_tools

# --------------------------------------------------
# CELL 2: Configuration and Data Path
# --------------------------------------------------
@app.cell
def setup(db_name):
    """
    Configuration cell - UPDATE THE DATA_PATH for your institution
    """
    mo.md(f"""
    ## Step 2: Configure Your Data Path
    
    Update the DATA_PATH below to point to your institution's {db_name} parquet dataset.
    """)
    
    # UPDATE THIS PATH to your institution's data location
    # Examples:
    # NSQIP: "/path/to/nsqip_parquet_dataset"
    # NCDB: "/path/to/ncdb_parquet_dataset"
    
    DATA_PATH = f"/path/to/your/{db_name.lower()}_parquet_dataset"
    
    # Verify the path exists
    data_path = Path(DATA_PATH)
    if not data_path.exists():
        mo.md(f"""
        **ERROR**: Data path not found!
        
        Please update DATA_PATH to point to your {db_name} parquet dataset.
        Current path: {DATA_PATH}
        """).callout(kind="danger")
    else:
        mo.md(f"""
        Data path confirmed: {DATA_PATH}
        """).callout(kind="success")
    
    return DATA_PATH, data_path

# --------------------------------------------------
# CELL 3: Define Research Parameters
# --------------------------------------------------
@app.cell
def parameters(db_name):
    """
    Define your research parameters based on database type
    """
    mo.md(f"""
    ## Step 3: Define Your Research Parameters
    
    Modify the parameters below for your {db_name} analysis.
    """)
    
    if db_name == "NSQIP":
        # NSQIP parameters
        mo.md("""
        ### NSQIP Parameters
        """)
        
        # CPT codes
        CPT_CODES = ["44970", "47562"]  # Example: lap appy, lap chole
        
        # Years
        YEARS = [2021, 2022]
        
        # Optional diagnosis codes
        DIAGNOSIS_CODES = []
        
        mo.md(f"""
        - **CPT Codes**: {', '.join(CPT_CODES)}
        - **Years**: {', '.join(map(str, YEARS))}
        - **Diagnosis Codes**: {', '.join(DIAGNOSIS_CODES) if DIAGNOSIS_CODES else 'None'}
        """)
        
        return {
            "cpt_codes": CPT_CODES,
            "years": YEARS,
            "diagnosis_codes": DIAGNOSIS_CODES
        }
    
    else:  # NCDB
        # NCDB parameters
        mo.md("""
        ### NCDB Parameters
        """)
        
        # Primary site codes (C50 = breast, C18 = colon, etc.)
        PRIMARY_SITES = ["C50", "C18"]
        
        # Years of diagnosis
        YEARS = [2020, 2021]
        
        # Histology codes (optional)
        HISTOLOGY_CODES = []
        
        mo.md(f"""
        - **Primary Sites**: {', '.join(PRIMARY_SITES)}
        - **Years**: {', '.join(map(str, YEARS))}
        - **Histology Codes**: {', '.join(HISTOLOGY_CODES) if HISTOLOGY_CODES else 'None'}
        """)
        
        return {
            "primary_sites": PRIMARY_SITES,
            "years": YEARS,
            "histology_codes": HISTOLOGY_CODES
        }

# --------------------------------------------------
# CELL 4: Load and Filter Data
# --------------------------------------------------
@app.cell
def load_data(DATA_PATH, db_name, db_tools, parameters):
    """
    Load clinical data using appropriate tools
    """
    mo.md(f"""
    ## Step 4: Load and Filter Data
    
    Using {db_name.lower()}_tools to efficiently load and filter the data.
    """)
    
    df = None
    
    try:
        # Build the query
        query = db_tools.load_data(DATA_PATH)
        
        if db_name == "NSQIP":
            # NSQIP filters
            if parameters.get("cpt_codes"):
                query = query.filter_by_cpt(parameters["cpt_codes"])
            if parameters.get("years"):
                query = query.filter_by_year(parameters["years"])
            if parameters.get("diagnosis_codes"):
                query = query.filter_by_diagnosis(parameters["diagnosis_codes"])
        
        else:  # NCDB
            # NCDB filters
            if parameters.get("primary_sites"):
                query = query.filter_by_primary_site(parameters["primary_sites"])
            if parameters.get("years"):
                query = query.filter_by_year(parameters["years"])
            if parameters.get("histology_codes"):
                query = query.filter_by_histology(parameters["histology_codes"])
        
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
        
        Please check:
        1. DATA_PATH points to valid {db_name.lower()}_tools parquet dataset
        2. You have access to the data location
        3. Your filter parameters are valid
        """).callout(kind="danger")
    
    return df

# --------------------------------------------------
# CELL 5: Database-Specific Outcomes
# --------------------------------------------------
@app.cell
def calculate_outcomes(df, db_name):
    """
    Calculate database-specific outcomes
    """
    if df is None:
        return mo.md("**No data loaded**")
    
    mo.md(f"""
    ## Step 5: Key {db_name} Outcomes
    """)
    
    if db_name == "NSQIP":
        # NSQIP surgical outcomes
        outcomes = {
            "DEATH30": "30-day Mortality",
            "READMISSION": "30-day Readmission",
            "REOPERATION": "30-day Reoperation",
            "SSI": "Surgical Site Infection",
            "PNEUMONIA": "Pneumonia",
            "UTI": "Urinary Tract Infection"
        }
    else:  # NCDB
        # NCDB cancer outcomes
        outcomes = {
            "VITAL_STATUS": "Vital Status (Dead)",
            "SURGICAL_MARGINS": "Positive Margins",
            "READM_HOSP_30": "30-day Readmission",
            "CHEMOTHERAPY": "Received Chemotherapy",
            "RADIATION": "Received Radiation",
            "IMMUNOTHERAPY": "Received Immunotherapy"
        }
    
    # Calculate rates
    outcome_rates = {}
    
    for var, description in outcomes.items():
        if var in df.columns:
            if db_name == "NSQIP":
                # NSQIP uses 1/0 coding
                rate = (df.filter(pl.col(var) == 1).shape[0] / df.shape[0]) * 100
                n_events = df.filter(pl.col(var) == 1).shape[0]
            else:  # NCDB
                # NCDB may use different coding - adjust as needed
                if var == "VITAL_STATUS":
                    rate = (df.filter(pl.col(var) == 0).shape[0] / df.shape[0]) * 100
                    n_events = df.filter(pl.col(var) == 0).shape[0]
                else:
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
    ### {db_name} Outcome Rates:
    
    {summary_df.to_pandas().to_markdown(index=False)}
    """)
    
    return outcome_rates, summary_df

# --------------------------------------------------
# CELL 6: Database-Specific Visualizations
# --------------------------------------------------
@app.cell
def create_plots(df, db_name, outcome_rates):
    """
    Create database-specific visualizations
    """
    if df is None:
        return mo.md("**No data loaded**")
    
    mo.md(f"""
    ## Step 6: {db_name} Visualizations
    """)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'{db_name} Analysis Summary', fontsize=16)
    
    # Plot 1: Age distribution
    ax1 = axes[0, 0]
    if db_name == "NSQIP":
        age_col = "AGE_AS_INT"
    else:  # NCDB
        age_col = "AGE_AT_DX"
    
    if age_col in df.columns:
        age_data = df.select(age_col).to_pandas()
        ax1.hist(age_data[age_col], bins=20, edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Age (years)')
        ax1.set_ylabel('Number of Cases')
        ax1.set_title('Age Distribution')
        ax1.grid(True, alpha=0.3)
    
    # Plot 2: Outcome rates
    ax2 = axes[0, 1]
    if outcome_rates:
        outcomes_list = list(outcome_rates.keys())[:6]  # Top 6
        rates = [outcome_rates[o]["rate"] for o in outcomes_list]
        
        bars = ax2.bar(range(len(outcomes_list)), rates, color='skyblue', edgecolor='navy')
        ax2.set_xticks(range(len(outcomes_list)))
        ax2.set_xticklabels(outcomes_list, rotation=45, ha='right')
        ax2.set_ylabel('Rate (%)')
        ax2.set_title(f'{db_name} Outcome Rates')
        ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Cases by year
    ax3 = axes[1, 0]
    if db_name == "NSQIP":
        year_col = "OPERYR"
    else:  # NCDB
        year_col = "YEAR_OF_DX"
    
    if year_col in df.columns:
        year_data = df.group_by(year_col).agg(pl.count()).sort(year_col)
        years = year_data.select(year_col).to_pandas()[year_col]
        counts = year_data.select("count").to_pandas()["count"]
        
        ax3.bar(years, counts, color='lightgreen', edgecolor='darkgreen')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Number of Cases')
        ax3.set_title('Cases by Year')
        ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Database-specific plot
    ax4 = axes[1, 1]
    if db_name == "NSQIP":
        # ASA class distribution
        if "ASA_CLASS" in df.columns:
            asa_data = df.group_by("ASA_CLASS").agg(pl.count()).sort("ASA_CLASS")
            ax4.bar(asa_data["ASA_CLASS"], asa_data["count"], color='salmon')
            ax4.set_xlabel('ASA Class')
            ax4.set_ylabel('Number of Cases')
            ax4.set_title('ASA Class Distribution')
    else:  # NCDB
        # Stage distribution
        if "TNM_CLIN_STAGE_GROUP" in df.columns:
            stage_data = df.group_by("TNM_CLIN_STAGE_GROUP").agg(pl.count())
            stage_data = stage_data.filter(pl.col("TNM_CLIN_STAGE_GROUP").is_not_null())
            ax4.bar(range(len(stage_data)), stage_data["count"], color='salmon')
            ax4.set_xticks(range(len(stage_data)))
            ax4.set_xticklabels(stage_data["TNM_CLIN_STAGE_GROUP"], rotation=45)
            ax4.set_xlabel('Clinical Stage')
            ax4.set_ylabel('Number of Cases')
            ax4.set_title('Stage Distribution')
    
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

# --------------------------------------------------
# CELL 7: Next Steps
# --------------------------------------------------
@app.cell
def next_steps(db_name):
    """
    Database-specific guidance
    """
    mo.md(f"""
    ## Next Steps for {db_name} Analysis
    
    ### General Enhancements:
    - Add risk adjustment models
    - Perform subgroup analyses
    - Create publication-ready tables
    - Export de-identified datasets
    
    ### {db_name}-Specific Analyses:
    """)
    
    if db_name == "NSQIP":
        mo.md("""
        - **Risk Models**: Use ACS Risk Calculator variables
        - **Quality Metrics**: Calculate O/E ratios
        - **Complications**: Analyze Clavien-Dindo grades
        - **LOS Analysis**: Compare to expected LOS
        - **Cost Analysis**: If cost data available
        
        Example code:
        ```python
        # Calculate composite complications
        df = df.with_columns(
            ((pl.col("SSI") == 1) | 
             (pl.col("PNEUMONIA") == 1) | 
             (pl.col("UTI") == 1)).alias("ANY_COMPLICATION")
        )
        ```
        """)
    else:  # NCDB
        mo.md("""
        - **Survival Analysis**: Kaplan-Meier curves
        - **Treatment Patterns**: Analyze by facility type
        - **Guideline Concordance**: Compare to NCCN
        - **Disparities**: Analyze by insurance, race
        - **Time to Treatment**: Calculate intervals
        
        Example code:
        ```python
        # Calculate survival time
        df = df.with_columns(
            (pl.col("LAST_CONTACT_DATE") - pl.col("DATE_OF_DX"))
            .dt.days()
            .alias("SURVIVAL_DAYS")
        )
        ```
        """)

# Run the app
if __name__ == "__main__":
    app.run()