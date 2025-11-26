# Data Dictionary for Long Term Care Facilities (HCAI)

This list provides definitions for the column headers found in `longterm_care_22_24.csv`. The data originates from the California Department of Health Care Access and Information (HCAI), formerly OSHPD.

## Facility Information
*   **FAC_NO**: Facility Number (Unique 9-digit identifier assigned by HCAI)
*   **FAC_NAME**: Facility Name
*   **LICENSE_NO**: License Number
*   **Year**: Reporting Year
*   **HCAI_ID**: HCAI Facility ID
*   **HFPA**: Health Facility Planning Area (Geographic planning region)
*   **HSA**: Health Service Area
*   **LIC_CAT**: License Category (e.g., SNF for Skilled Nursing Facility)
*   **TYPE_CNTRL**: Type of Control (Ownership type, e.g., Investor Owned, Non-Profit)
*   **LEGAL_ORG**: Legal Organization (e.g., Corporation, Partnership)
*   **MCAL_PRO#**: Medi-Cal Provider Number
*   **ADMINIS**: Administrator Name
*   **RELATED**: Related Party Transaction Indicator
*   **PARENT**: Parent Organization Name

## Utilization Data (Patient Days & Beds)
*   **BED_END**: Licensed Beds at End of Period
*   **BED_AVG**: Average Licensed Beds
*   **DAY_TOTL**: Total Patient Days
*   **OCCUP**: Occupancy Rate (%)
*   **ADMITS**: Total Admissions
*   **DISCHS**: Total Discharges
*   **DAY_MCAR**: Patient Days - Medicare
*   **DAY_MCAL**: Patient Days - Medi-Cal
*   **DAY_SELF**: Patient Days - Self Pay (Private Pay)
*   **DAY_MGD**: Patient Days - Managed Care
*   **DAY_OTH**: Patient Days - Other Payers
*   **DAY_SN**: Patient Days - Skilled Nursing
*   **DAY_IC**: Patient Days - Intermediate Care
*   **DAY_MD**: Patient Days - Mentally Disordered
*   **DAY_DD**: Patient Days - Developmentally Disabled

## Financial Data - Revenue
*   **GR_RT_TOTL**: Gross Routine Services Revenue Total
*   **GR_AN_TOTL**: Gross Ancillary Services Revenue Total
*   **DFR_TOTL**: Deductions from Revenue Total (Contractual adjustments, charity care, etc.)
*   **OTH_OP_REV**: Other Operating Revenue
*   **TOT_HC_REV**: Total Health Care Revenue (Net Patient Revenue + Other Operating Revenue)
*   **NET_FRM_HC**: Net Income from Health Care Operations
*   **NONHC_NET**: Net Income from Non-Health Care Operations
*   **NET_INCOME**: Net Income (Bottom line)

### Gross Revenue by Payer (Prefixes)
*   **GR_RT_...**: Gross Revenue Routine Services (Daily care)
*   **GR_AN_...**: Gross Revenue Ancillary Services (Therapy, pharmacy, etc.)
    *   **_MCAR**: Medicare
    *   **_MCAL**: Medi-Cal
    *   **_SELF**: Self Pay
    *   **_MGD**: Managed Care
    *   **_OTH**: Other
    *   **_IP**: Inpatient
    *   **_OP**: Outpatient

## Financial Data - Expenses
*   **TOT_HC_EXP**: Total Health Care Expenses
*   **EXP_SAL**: Salaries and Wages
*   **EXP_BEN**: Employee Benefits
*   **EXP_OTHER**: Other Expenses
*   **EXP_...**: Specific Expense Categories
    *   **_NURS**: Nursing Services
    *   **_ANCL**: Ancillary Services
    *   **_GEN**: General Services
    *   **_FIS**: Fiscal Services
    *   **_ADMN**: Administrative Services

## Balance Sheet
*   **CUR_ASST**: Current Assets
*   **TOT_ASST**: Total Assets
*   **CUR_LIAB**: Current Liabilities
*   **EQUITY**: Total Equity (Net Worth)
*   **NET_PPE**: Net Property, Plant, and Equipment

## Labor & Staffing
*   **PRDHR_...**: Productive Hours (Hours worked)
*   **S&W_...**: Salaries and Wages (Dollar amount)
    *   **_MGT**: Management
    *   **_RN**: Registered Nurses
    *   **_LVN**: Licensed Vocational Nurses
    *   **_NA**: Nurse Assistants
    *   **_OTH**: Other Staff
*   **EMP_AVG**: Average Number of Employees
*   **EMP_TRNOVR**: Employee Turnover Rate

## Other
*   **Utilization Reported?**: Indicator if utilization data was reported
*   **Financials Reported?**: Indicator if financial data was reported
*   **Penalized?**: Indicator if the facility received an enforcement action/penalty
