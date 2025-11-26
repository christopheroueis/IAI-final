import pandas as pd

def check_missing(file_path):
    try:
        print(f"Reading {file_path}...")
        df = pd.read_csv(file_path, low_memory=False)
        
        missing_percentages = df.isnull().mean() * 100
        top_missing = missing_percentages.sort_values(ascending=False).head(20)
        
        print("\nTop 20 columns with highest % of missing data:")
        print("-" * 50)
        for col, pct in top_missing.items():
            print(f"{col}: {pct:.2f}%")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/data/processed/longterm_care_cleaned.csv'
    check_missing(file_path)
