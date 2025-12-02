import pandas as pd
import os

def enhance_dictionary():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'processed', 'hospital_cleaned.csv')
    output_file = os.path.join(base_dir, 'docs-hospitals', 'hospital_data_dictionary.md')

    try:
        df = pd.read_csv(input_file, nrows=1)
        columns = df.columns.tolist()
        
        # Define Themes and Logic
        themes = {
            "Target Variable": [],
            "Facility Profile": [],
            "Licensing & Capacity": [],
            "Utilization & Patient Activity": [],
            "Financials - Revenue": [],
            "Financials - Expenses": [],
            "Financials - Balance Sheet": [],
            "Staffing & Hours": [],
            "Services & Operations": [],
            "Other/Uncategorized": []
        }

        for col in columns:
            desc = "Detailed description not available"
            theme = "Other/Uncategorized"
            
            # Logic for categorization and description
            if col == 'Penalized?':
                theme = "Target Variable"
                desc = "Binary indicator of whether the facility has received enforcement actions or penalties."
            
            elif any(x in col for x in ['FAC_', 'ADDRESS', 'CITY', 'ZIP', 'COUNTY', 'HSA', 'HFPA', 'ORG_NAME', 'OWNER', 'TEACH', 'DIST', 'AREA', 'CENSUS']):
                theme = "Facility Profile"
                if 'FAC_NAME' in col: desc = "Name of the healthcare facility."
                if 'FAC_NO' in col: desc = "Unique facility identification number."
                if 'ZIP' in col: desc = "Zip code of the facility location."
                if 'COUNTY' in col: desc = "County where the facility is located."
                if 'HSA' in col: desc = "Health Service Area code."
                if 'OWNER' in col: desc = "Ownership type of the facility."
                if 'TEACH' in col: desc = "Teaching hospital status."
                if 'CENSUS' in col: desc = "Census tract key."
            
            elif any(x in col for x in ['LIC', 'BED', 'LEVEL', 'STATUS', 'BASSINETS']):
                theme = "Licensing & Capacity"
                if 'LIC_NO' in col or 'LICENSE' in col: desc = "License number or status details."
                if 'BED_LIC' in col: desc = "Number of licensed beds."
                if 'BED_AVL' in col: desc = "Number of available beds."
                if 'BED_STF' in col: desc = "Number of staffed beds."
                if 'BED_ACUTE' in col: desc = "Number of acute care beds."
                if 'BED_PSYCH' in col: desc = "Number of psychiatric beds."
                if 'BED_LTC' in col: desc = "Number of long-term care beds."
                if 'BASSINETS' in col: desc = "Number of newborn bassinets."
            
            elif any(x in col for x in ['DAY_', 'DIS_', 'VIS_', 'OCC_', 'ALOS', 'CEN_', 'ADMITTED', 'TRANSFERS']):
                theme = "Utilization & Patient Activity"
                if 'DAY_TOT' in col: desc = "Total patient days."
                if 'DIS_TOT' in col: desc = "Total patient discharges."
                if 'VIS_TOT' in col: desc = "Total outpatient visits."
                if 'ALOS' in col: desc = "Average Length of Stay (days)."
                if 'OCC_LIC' in col: desc = "Occupancy rate based on licensed beds."
                if 'VIS_ER' in col: desc = "Emergency room visits."
                if 'MCAR' in col: desc = "Medicare patient activity."
                if 'MCAL' in col: desc = "Medi-Cal patient activity."
                if 'CNTY' in col: desc = "County Indigent patient activity."
                if 'THRD' in col: desc = "Third Party/Private Insurance patient activity."
            
            elif any(x in col for x in ['REV', 'INCOME', 'NET_', 'GR_', 'CAP_', 'CHAR_', 'BAD_DEBT', 'DED_', 'CONTRIBTNS', 'INV_', 'APPRO']):
                theme = "Financials - Revenue"
                if 'GR_PT_REV' in col: desc = "Gross patient revenue."
                if 'NET_PT_REV' in col: desc = "Net patient revenue."
                if 'NET_INCOME' in col: desc = "Net income (Profit/Loss)."
                if 'CAP_REV' in col: desc = "Capitation revenue."
                if 'MCAR' in col: desc = "Revenue from Medicare."
                if 'MCAL' in col: desc = "Revenue from Medi-Cal."
                if 'GR_IP' in col: desc = "Gross Inpatient Revenue."
                if 'GR_OP' in col: desc = "Gross Outpatient Revenue."
                if 'BAD_DEBT' in col: desc = "Provision for bad debts."
                if 'CHAR_' in col: desc = "Charity care charges."
            
            elif any(x in col for x in ['EXP', 'SAL', 'BEN', 'COST', 'PURCH', 'DEPRE', 'LEASES', 'INSUR', 'INTRST']):
                theme = "Financials - Expenses"
                if 'TOT_OP_EXP' in col: desc = "Total operating expenses."
                if 'EXP_SAL' in col: desc = "Salary expenses."
                if 'EXP_BEN' in col: desc = "Benefits expenses."
                if 'EXP_SUPP' in col: desc = "Supply expenses."
                if 'EXP_ANC' in col: desc = "Ancillary service expenses."
                if 'EXP_GEN' in col: desc = "General services expenses."
            
            elif any(x in col for x in ['ASST', 'LIAB', 'EQUITY', 'CASH', 'DEBT', 'PPE', 'BLDGS', 'EQUIPMENT', 'MORT_', 'BOND_', 'CRED']):
                theme = "Financials - Balance Sheet"
                if 'TOT_ASST' in col: desc = "Total assets."
                if 'CUR_ASST' in col: desc = "Current assets."
                if 'TOT_LTDEBT' in col: desc = "Total long-term debt."
                if 'EQUITY' in col: desc = "Total equity."
                if 'PPE' in col: desc = "Property, Plant, and Equipment."
            
            elif any(x in col for x in ['FTE', 'HRS', 'STAFF']):
                theme = "Staffing & Hours"
                if 'HOSP_FTE' in col: desc = "Total hospital Full-Time Equivalents."
                if 'NURS_FTE' in col: desc = "Nursing Full-Time Equivalents."
                if 'PROD_HRS' in col: desc = "Productive hours worked."
                if 'PAID_HRS' in col: desc = "Total paid hours."
                if 'CNT_HR' in col: desc = "Contracted labor hours."
                if '_RN' in col: desc += " (Registered Nurses)."
                if '_LVN' in col: desc += " (Licensed Vocational Nurses)."
                if '_AID' in col: desc += " (Aides/Orderlies)."
                if '_MGT' in col: desc += " (Management/Supervision)."
            
            elif any(x in col for x in ['SURG', 'OPER', 'EMS', 'ER_', 'OFFER', 'TRAFFIC', 'SECTIONS']):
                theme = "Services & Operations"
                if 'SURG_IP' in col: desc = "Inpatient surgeries performed."
                if 'SURG_OP' in col: desc = "Outpatient surgeries performed."
                if 'EMS_VISITS' in col: desc = "Emergency Medical Services visits."
                if 'OP_ROOM' in col: desc = "Number of operating rooms."
                if 'OFFER' in col: desc = "Service offered indicator."

            themes[theme].append((col, desc))

        # Write to Markdown
        with open(output_file, 'w') as f:
            f.write("# Hospital Data Dictionary\n\n")
            f.write(f"**Total Columns**: {len(columns)}\n\n")
            f.write("This document provides a comprehensive dictionary of the features available in the hospital dataset, categorized by operational theme.\n\n")
            
            for theme, items in themes.items():
                if not items: continue
                f.write(f"## {theme}\n")
                f.write(f"| Column Name | Comprehensive Description | Type |\n")
                f.write("|---|---|---|\n")
                for col, desc in items:
                    # Attempt to infer type
                    dtype = str(df[col].dtype)
                    f.write(f"| `{col}` | {desc} | {dtype} |\n")
                f.write("\n")
                
        print(f"Enhanced dictionary generated at {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    enhance_dictionary()
