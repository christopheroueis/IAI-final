import pandas as pd
import os

def convert_and_merge():
    # File paths
    file_2022 = 'longterm_care_v2_2022.xlsx'
    file_2024 = 'longterm_care_v2_2024.xlsx'
    
    # Check if files exist
    if not os.path.exists(file_2022):
        print(f"Error: {file_2022} not found.")
        return
    if not os.path.exists(file_2024):
        print(f"Error: {file_2024} not found.")
        return

    print("Reading 2022 data...")
    df_2022 = pd.read_excel(file_2022)
    df_2022['year'] = 2022
    csv_2022 = 'longterm_care_v2_2022.csv'
    df_2022.to_csv(csv_2022, index=False)
    print(f"Saved {csv_2022}")

    print("Reading 2024 data...")
    df_2024 = pd.read_excel(file_2024)
    df_2024['year'] = 2024
    csv_2024 = 'longterm_care_v2_2024.csv'
    df_2024.to_csv(csv_2024, index=False)
    print(f"Saved {csv_2024}")

    print("Merging data...")
    merged_df = pd.concat([df_2022, df_2024], ignore_index=True)
    
    output_file = 'longterm_care_22_24.csv'
    merged_df.to_csv(output_file, index=False)
    print(f"Saved merged file to {output_file}")
    
    # Verification
    print("\nVerification:")
    print(f"2022 shape: {df_2022.shape}")
    print(f"2024 shape: {df_2024.shape}")
    print(f"Merged shape: {merged_df.shape}")
    
    if len(merged_df) == len(df_2022) + len(df_2024):
        print("Row count verification passed.")
    else:
        print("Row count verification FAILED.")

if __name__ == "__main__":
    convert_and_merge()
