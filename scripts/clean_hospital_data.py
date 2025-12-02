import pandas as pd
import os

def clean_hospital_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'processed', 'hospital_22_24.csv')
    output_file = os.path.join(base_dir, 'data', 'processed', 'hospital_cleaned.csv')

    try:
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file, low_memory=False)
        
        initial_columns = len(df.columns)
        print(f"Initial columns: {initial_columns}")
        
        # Calculate missing percentages
        missing_percentages = df.isnull().mean() * 100
        
        # Identify columns to drop
        columns_to_drop = missing_percentages[missing_percentages > 50].index
        
        # Drop columns
        df_cleaned = df.drop(columns=columns_to_drop)
        
        final_columns = len(df_cleaned.columns)
        print(f"Columns dropped: {len(columns_to_drop)}")
        print(f"Remaining columns: {final_columns}")
        
        # Save cleaned data
        print(f"Saving cleaned data to {output_file}...")
        df_cleaned.to_csv(output_file, index=False)
        print("Done.")
        
    except Exception as e:
        print(f"Error cleaning data: {e}")

if __name__ == "__main__":
    clean_hospital_data()
