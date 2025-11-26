import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def perform_eda(input_file, output_report):
    try:
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file, low_memory=False)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_report), exist_ok=True)
        
        with open(output_report, 'w') as f:
            f.write("# Exploratory Data Analysis Report\n\n")
            
            # 1. Data Structure
            f.write("## 1. Data Structure\n")
            f.write(f"*   **Rows**: {df.shape[0]}\n")
            f.write(f"*   **Columns**: {df.shape[1]}\n")
            f.write(f"*   **Years**: {df['Year'].unique().tolist()}\n\n")
            
            # 2. Univariate Analysis
            f.write("## 2. Univariate Analysis\n")
            
            # Facility Types
            f.write("### Facility Types\n")
            type_counts = df['TYPE_CNTRL'].value_counts()
            f.write(type_counts.to_string())
            f.write("\n\n")
            
            # Financials
            f.write("### Financial Overview (Averages)\n")
            financial_cols = ['TOT_HC_REV', 'TOT_HC_EXP', 'NET_INCOME']
            f.write(df[financial_cols].describe().to_string())
            f.write("\n\n")
            
            # 3. Bivariate Analysis
            f.write("## 3. Bivariate Analysis\n")
            
            # Profitability by Ownership
            f.write("### Net Income by Ownership Type\n")
            profit_by_owner = df.groupby('TYPE_CNTRL')['NET_INCOME'].mean().sort_values(ascending=False)
            f.write(profit_by_owner.to_string())
            f.write("\n\n")
            
            # 4. Temporal Analysis
            f.write("## 4. Temporal Analysis (2022 vs 2024)\n")
            year_comparison = df.groupby('Year')[['TOT_HC_REV', 'TOT_HC_EXP', 'NET_INCOME', 'OCCUP']].mean()
            f.write(year_comparison.to_string())
            f.write("\n\n")
            
            # 5. Geographic Analysis
            f.write("## 5. Geographic Analysis (Top 10 Counties)\n")
            top_counties = df['COUNTY_x'].value_counts().head(10).index
            geo_stats = df[df['COUNTY_x'].isin(top_counties)].groupby('COUNTY_x')[['NET_INCOME', 'OCCUP']].mean().sort_values('NET_INCOME', ascending=False)
            f.write(geo_stats.to_string())
            f.write("\n\n")

        print(f"EDA report generated at {output_report}")
        
    except Exception as e:
        print(f"Error performing EDA: {e}")

if __name__ == "__main__":
    input_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/data/processed/longterm_care_cleaned.csv'
    output_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/docs/eda_report.md'
    perform_eda(input_path, output_path)
