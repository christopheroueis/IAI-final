import pandas as pd

def analyze_missing_data(file_path):
    try:
        df = pd.read_csv(file_path, low_memory=False)
        missing_percentages = df.isnull().mean() * 100
        missing_columns = missing_percentages[missing_percentages > 50].sort_values(ascending=False)
        
        # Save to file
        output_file = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/missing_data_columns.md'
        with open(output_file, 'w') as f:
            f.write("# Columns with > 50% Missing Data\n\n")
            for col, pct in missing_columns.items():
                f.write(f"*   **{col}**: {pct:.2f}%\n")
        
        print(f"Total columns in file: {len(df.columns)}")
        print(f"List of missing columns saved to: {output_file}")
            
    except Exception as e:
        print(f"Error analyzing file: {e}")

if __name__ == "__main__":
    file_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/longterm_care_22_24.csv'
    analyze_missing_data(file_path)
