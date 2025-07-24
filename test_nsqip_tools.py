#!/usr/bin/env python3
"""
Test script to check nsqip_tools NSQIPQuery object methods and LazyFrame access
"""

import nsqip_tools
import polars as pl
from pathlib import Path

def main():
    # Data path
    DATA_PATH = Path("/home/brantlab/projects/clinical-db-analysis/data/adult_nsqip_parquet")
    
    print(f"Testing nsqip_tools with data path: {DATA_PATH}")
    print(f"nsqip_tools version: {nsqip_tools.__version__}")
    
    # Also check if version 0.2.2 features are available
    print(f"nsqip_tools location: {nsqip_tools.__file__}")
    
    # Check if filter_by_cpt works
    print("Testing if filter_by_cpt has been fixed...")
    print()
    
    # Load NSQIP data
    print("Loading data...")
    nsqip_query = nsqip_tools.load_data(str(DATA_PATH))
    print(f"Loaded object type: {type(nsqip_query)}")
    print()
    
    # Check available methods
    methods = [m for m in dir(nsqip_query) if not m.startswith('_')]
    print("Available methods:")
    for method in sorted(methods):
        print(f"  - {method}")
    print()
    
    # Test the problematic filtering step by step
    print("=== DEBUGGING FILTERING ISSUE ===")
    
    # CPT codes for tonsillectomy procedures (age 12+)
    target_cpts = ["42821", "42826"]
    
    # Step 1: Test basic CPT filtering
    print("Step 1: Filter by CPT codes only")
    try:
        filtered_query = nsqip_query.filter_by_cpt(target_cpts)
        print(f"  ✓ CPT filtering successful, type: {type(filtered_query)}")
        
        # Get the LazyFrame
        lazy_df = filtered_query.lazy_frame
        print(f"  ✓ Got LazyFrame, type: {type(lazy_df)}")
        
        # Collect to see the result
        df_step1 = lazy_df.collect()
        print(f"  ✓ After CPT filter: {df_step1.shape}")
        
    except Exception as e:
        print(f"  ✗ Step 1 failed: {e}")
        return
    
    # Step 2: Check ALL_CPT_CODES column
    print("\nStep 2: Check ALL_CPT_CODES column")
    try:
        if "ALL_CPT_CODES" in df_step1.columns:
            print("  ✓ ALL_CPT_CODES column exists")
            
            sample_cpts = df_step1["ALL_CPT_CODES"].head(10)
            print("  Sample ALL_CPT_CODES values:")
            for i, cpt_list in enumerate(sample_cpts):
                print(f"    Row {i}: {cpt_list} (type: {type(cpt_list)}, length: {len(cpt_list) if cpt_list else 'None'})")
                
            # Check for any null values
            null_count = df_step1["ALL_CPT_CODES"].null_count()
            print(f"  NULL values in ALL_CPT_CODES: {null_count}")
            
        else:
            print("  ✗ ALL_CPT_CODES column not found!")
            print(f"  Available columns: {df_step1.columns[:10]}...")
            return
            
    except Exception as e:
        print(f"  ✗ Step 2 failed: {e}")
        return
    
    # Step 3: Test the list length filter
    print("\nStep 3: Test list length filter")
    try:
        # First try without the list operations
        df_step3a = (
            lazy_df
            .filter(pl.col("ALL_CPT_CODES").is_not_null())
            .collect()
        )
        print(f"  ✓ Non-null filter works: {df_step3a.shape}")
        
        # Now try the list length filter
        df_step3b = (
            lazy_df
            .filter(pl.col("ALL_CPT_CODES").list.len() == 1)
            .collect()
        )
        print(f"  ✓ List length filter works: {df_step3b.shape}")
        
    except Exception as e:
        print(f"  ✗ Step 3 failed: {e}")
        print(f"  Error details: {str(e)}")
        
        # Try to understand the column structure better
        print("\n  Debugging column structure:")
        try:
            schema = lazy_df.schema
            cpt_col_type = schema.get("ALL_CPT_CODES")
            print(f"    ALL_CPT_CODES column type: {cpt_col_type}")
            
            # Try a simpler approach
            print("    Testing simpler filters...")
            test_df = lazy_df.select("ALL_CPT_CODES").head(5).collect()
            print(f"    Simple select works: {test_df}")
            
        except Exception as debug_e:
            print(f"    Debug failed: {debug_e}")
        
        return
    
    print(f"\n✅ All steps successful! Final result: {df_step3b.shape} rows")
    
    if len(df_step3b) > 0:
        print("Sample results:")
        sample_data = df_step3b.select(["CPT", "ALL_CPT_CODES", "DEATH30"]).head(5)
        print(sample_data)

if __name__ == "__main__":
    main()