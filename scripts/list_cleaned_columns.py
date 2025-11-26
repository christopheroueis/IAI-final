import pandas as pd

def list_columns(file_path):
    try:
        df = pd.read_csv(file_path, nrows=0) # Read only headers
        columns = df.columns.tolist()
        
        print(f"Columns in {file_path} ({len(columns)} total):")
        for col in columns:
            print(col)
            
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    file_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/longterm_care_cleaned.csv'
    list_columns(file_path)
