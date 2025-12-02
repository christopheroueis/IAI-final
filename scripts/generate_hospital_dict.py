import pandas as pd
import os

def generate_dictionary():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'processed', 'hospital_cleaned.csv')
    output_file = os.path.join(base_dir, 'docs-hospitals', 'hospital_data_dictionary.md')

    try:
        df = pd.read_csv(input_file, nrows=1) # Only read header
        columns = df.columns.tolist()
        
        with open(output_file, 'w') as f:
            f.write("# Hospital Data Dictionary\n\n")
            f.write(f"Total Columns: {len(columns)}\n\n")
            f.write("| Column Name | Description | Type |\n")
            f.write("|---|---|---|\n")
            
            for col in columns:
                # Infer description based on common patterns
                desc = "TBD"
                if "FAC" in col: desc = "Facility Information"
                if "LIC" in col: desc = "Licensing Information"
                if "BED" in col: desc = "Bed Count"
                if "REV" in col: desc = "Revenue"
                if "EXP" in col: desc = "Expense"
                if "Penalized" in col: desc = "**Target Variable**: Penalized Status"
                
                f.write(f"| `{col}` | {desc} | |\n")
                
        print(f"Generated dictionary at {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_dictionary()
