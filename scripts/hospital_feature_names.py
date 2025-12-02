"""
Hospital Feature Name Mapping Utility
Converts abbreviated feature names to full, human-readable descriptions.
"""

def get_feature_name_mapping():
    """Returns a dictionary of common abbreviation mappings."""
    return {
        'MCAR': 'Medicare',
        'MCAL': 'Medi-Cal',
        'CNTY': 'County',
        'THRD': 'Third Party',
        'GR_': 'Gross ',
        'NET_': 'Net ',
        'EXP_': 'Expense - ',
        'REV_': 'Revenue - ',
        'DAY_': 'Days - ',
        'DIS_': 'Discharges - ',
        'VIS_': 'Visits - ',
        'BED_': 'Beds - ',
        'LIC_': 'Licensed ',
        'FAC_': 'Facility ',
        'TOT_': 'Total ',
        'OP_': 'Outpatient ',
        'IP_': 'Inpatient ',
        'FTE': 'Full-Time Equivalents',
        'HRS': 'Hours',
        'SURG': 'Surgery',
        'OPER': 'Operating',
        'AMB': 'Ambulatory',
        'ANC': 'Ancillary',
        'DLY': 'Daily',
        'SAL': 'Salary',
        'BEN': 'Benefits',
        'SUPP': 'Supplies',
        'ASST': 'Assets',
        'LIAB': 'Liabilities',
        'DEPRE': 'Depreciation',
        'EQUIP': 'Equipment',
        'HOSP': 'Hospital',
        'NURS': 'Nursing',
        'PROD': 'Productive',
        'PAID': 'Paid',
        'ALOS': 'Average Length of Stay',
        'OCC': 'Occupancy',
        'ACUTE': 'Acute Care',
        'PSYCH': 'Psychiatric',
        'REHAB': 'Rehabilitation',
        'LTC': 'Long-Term Care',
        'IC_': 'Intensive Care ',
        'ER_': 'Emergency Room ',
        'EMS': 'Emergency Medical Services',
        'num__': '',  # Remove preprocessing prefix
        'cat__': '',  # Remove preprocessing prefix
    }

def convert_feature_name(abbreviated_name):
    """
    Convert an abbreviated feature name to a full descriptive name.
    
    Args:
        abbreviated_name (str): The abbreviated feature name
        
    Returns:
        str: Full descriptive feature name
    """
    mapping = get_feature_name_mapping()
    full_name = abbreviated_name
    
    # Apply mappings
    for abbr, full in mapping.items():
        full_name = full_name.replace(abbr, full)
    
    # Clean up underscores and extra spaces
    full_name = full_name.replace('_', ' ').strip()
    full_name = ' '.join(full_name.split())  # Remove multiple spaces
    
    # Capitalize first letter
    if full_name:
        full_name = full_name[0].upper() + full_name[1:]
    
    return full_name

def convert_feature_names(feature_list):
    """
    Convert a list of abbreviated feature names to full descriptive names.
    
    Args:
        feature_list (list): List of abbreviated feature names
        
    Returns:
        list: List of full descriptive feature names
    """
    return [convert_feature_name(name) for name in feature_list]
