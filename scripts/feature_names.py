"""
Feature name mapping for readable visualization labels.
Maps abbreviated column names to full, human-readable names.
"""

FEATURE_NAME_MAP = {
    # Financial Metrics
    'NET_INCOME': 'Net Income',
    'TOT_HC_REV': 'Total Healthcare Revenue',
    'TOT_HC_EXP': 'Total Healthcare Expenses',
    'Net_Income_Margin': 'Net Income Margin (%)',
    'GR_RT_TOTL': 'Gross Routine Services Revenue',
    'GR_AN_TOTL': 'Gross Ancillary Services Revenue',
    'DFR_TOTL': 'Deductions from Revenue',
    'NET_FRM_HC': 'Net Income from Healthcare Operations',
    'OTH_OP_REV': 'Other Operating Revenue',
    
    # Expenses
    'EXP_SAL': 'Salaries and Wages',
    'EXP_BEN': 'Employee Benefits',
    'EXP_NURS': 'Nursing Services Expenses',
    'EXP_ANCL': 'Ancillary Services Expenses',
    'EXP_ADMN': 'Administrative Expenses',
    'EXP_GEN': 'General Services Expenses',
    'EXP_FIS': 'Fiscal Services Expenses',
    'EXP_OTHER': 'Other Expenses',
    
    # Patient Days & Utilization
    'DAY_TOTL': 'Total Patient Days',
    'DAY_MCAR': 'Medicare Patient Days',
    'DAY_MCAL': 'Medi-Cal Patient Days',
    'DAY_SELF': 'Self-Pay Patient Days',
    'DAY_MGD': 'Managed Care Patient Days',
    'DAY_OTH': 'Other Payer Patient Days',
    'DAY_SN': 'Skilled Nursing Patient Days',
    'DAY_IC': 'Intermediate Care Patient Days',
    'OCCUP': 'Occupancy Rate (%)',
    'ADMITS': 'Total Admissions',
    'DISCHS': 'Total Discharges',
    
    # Beds
    'BED_END': 'Licensed Beds (End of Period)',
    'BED_AVG': 'Average Licensed Beds',
    'TOT_LIC_BEDS': 'Total Licensed Beds',
    
    # Staffing Hours
    'PRDHR_RN': 'RN Productive Hours',
    'PRDHR_LVN': 'LVN Productive Hours',
    'PRDHR_NA': 'Nurse Assistant Productive Hours',
    'PRDHR_RN_Per_Day': 'RN Hours per Patient Day',
    'PRDHR_LVN_Per_Day': 'LVN Hours per Patient Day',
    'PRDHR_NA_Per_Day': 'Nurse Assistant Hours per Patient Day',
    'PRDHR_MGT': 'Management Productive Hours',
    'PRDHR_OTH': 'Other Staff Productive Hours',
    
    # Staffing Wages
    'S&W_RN': 'RN Salaries and Wages',
    'S&W_LVN': 'LVN Salaries and Wages',
    'S&W_NA': 'Nurse Assistant Salaries and Wages',
    'S&W_MGT': 'Management Salaries and Wages',
    'S&W_OTH': 'Other Staff Salaries and Wages',
    
    # Employee Metrics
    'EMP_AVG': 'Average Number of Employees',
    'EMP_TRNOVR': 'Employee Turnover Rate (%)',
    
    # Balance Sheet
    'CUR_ASST': 'Current Assets',
    'TOT_ASST': 'Total Assets',
    'CUR_LIAB': 'Current Liabilities',
    'EQUITY': 'Total Equity (Net Worth)',
    'NET_PPE': 'Net Property, Plant & Equipment',
    
    # Revenue by Payer
    'GR_RT_MCAR': 'Routine Revenue - Medicare',
    'GR_RT_MCAL': 'Routine Revenue - Medi-Cal',
    'GR_RT_SELF': 'Routine Revenue - Self-Pay',
    'GR_RT_MGD': 'Routine Revenue - Managed Care',
    'GR_AN_MCAR': 'Ancillary Revenue - Medicare',
    'GR_AN_MCAL': 'Ancillary Revenue - Medi-Cal',
    'GR_AN_SELF': 'Ancillary Revenue - Self-Pay',
    'GR_AN_MGD': 'Ancillary Revenue - Managed Care',
    
    # Facility Type (One-Hot Encoded)
    'LIC_CAT_SNF': 'License Category: Skilled Nursing Facility',
    'TYPE_CNTRL_Investor Owned': 'Ownership: Investor Owned',
    'TYPE_CNTRL_Non-Profit Corporation': 'Ownership: Non-Profit Corporation',
    'TYPE_CNTRL_County': 'Ownership: County',
    'TYPE_CNTRL_City': 'Ownership: City',
    'TYPE_CNTRL_State': 'Ownership: State',
    'LEGAL_ORG_Corporation': 'Legal Organization: Corporation',
    'LEGAL_ORG_Partnership': 'Legal Organization: Partnership',
    'LEGAL_ORG_Individual': 'Legal Organization: Individual',
    
    # Other
    'RELATED': 'Related Party Transactions',
    'year': 'Reporting Year',
}


def get_readable_name(feature_name):
    """
    Convert abbreviated feature name to readable name.
    
    Args:
        feature_name: Abbreviated column name (e.g., 'DAY_TOTL')
    
    Returns:
        Human-readable name (e.g., 'Total Patient Days')
    """
    # Direct mapping
    if feature_name in FEATURE_NAME_MAP:
        return FEATURE_NAME_MAP[feature_name]
    
    # Handle one-hot encoded categorical features
    # Format: "ColumnName_Value"
    for prefix in ['LIC_CAT_', 'TYPE_CNTRL_', 'LEGAL_ORG_', 'COUNTY_', 'HSA_']:
        if feature_name.startswith(prefix):
            value = feature_name[len(prefix):]
            category = prefix.rstrip('_')
            
            category_names = {
                'LIC_CAT': 'License Category',
                'TYPE_CNTRL': 'Ownership Type',
                'LEGAL_ORG': 'Legal Organization',
                'COUNTY': 'County',
                'HSA': 'Health Service Area'
            }
            
            return f"{category_names.get(category, category)}: {value}"
    
    # Default: Return as-is with underscores replaced
    return feature_name.replace('_', ' ').title()


def map_feature_names(feature_list):
    """
    Map a list of feature names to readable names.
    
    Args:
        feature_list: List of abbreviated feature names
    
    Returns:
        List of readable feature names
    """
    return [get_readable_name(f) for f in feature_list]
