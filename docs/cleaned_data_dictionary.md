# Cleaned Data Dictionary for Long Term Care Facilities

This dictionary describes the 248 columns remaining in `longterm_care_cleaned.csv` after removing those with >50% missing data.

## 1. Facility Identification & Location
*   **FAC_NO**: Facility Number (Unique 9-digit HCAI identifier)
*   **FAC_NAME_x / FAC_NAME_y / FAC_NAME**: Facility Name (Appears multiple times due to merge)
*   **LICENSE_NO_x / LICENSE_NO_y**: State License Number
*   **HCAI_ID**: HCAI Facility ID
*   **FACID**: Facility ID
*   **FACNAME**: Facility Name
*   **LICENSE_NUMBER**: License Number
*   **CITY / FAC_CITY**: City
*   **ZIP_CODE / FAC_ZIP**: Zip Code
*   **COUNTY_x / COUNTY_y**: County
*   **HSA**: Health Service Area
*   **HFPA**: Health Facility Planning Area
*   **ASSEMBLY_DIST**: Assembly District
*   **SENATE_DIST**: Senate District
*   **CONGRESS_DIST**: Congress District
*   **CENSUS_KEY**: Census Key
*   **MED_SVC_STUDY_AREA**: Medical Service Study Area
*   **HEALTH_SVC_AREA**: Health Service Area

## 2. Facility Characteristics & Administration
*   **Year**: Reporting Year (2022 or 2024)
*   **LIC_CAT_x / LIC_CAT_y**: License Category (e.g., Skilled Nursing Facility)
*   **TYPE_CNTRL**: Type of Control (e.g., Investor Owned, Non-Profit)
*   **LEGAL_ORG**: Legal Organization (e.g., Corporation, Partnership)
*   **ADMINIS**: Administrator Name
*   **RELATED**: Related Party Transaction Indicator
*   **FAC_OPERATED_THIS_YR**: Did the facility operate this year?
*   **FAC_OP_PER_BEGIN_DT**: Operating Period Begin Date
*   **FAC_OP_PER_END_DT**: Operating Period End Date
*   **FAC_PAR_CORP_NAME**: Parent Corporation Name
*   **FAC_PAR_CORP_CITY**: Parent Corporation City
*   **FAC_PAR_CORP_STATE**: Parent Corporation State
*   **FAC_PAR_CORP_ZIP**: Parent Corporation Zip
*   **LICENSE_EFF_DATE**: License Effective Date
*   **LICENSE_EXP_DATE**: License Expiration Date
*   **LICENSE_STATUS**: License Status
*   **FACILITY_LEVEL**: Facility Level
*   **LICEE_TOC**: Licensee Type of Control
*   **FAC_CERT_MEDICARE_SN**: Certified for Medicare Skilled Nursing?
*   **FAC_CERT_MEDI_CAL_SN**: Certified for Medi-Cal Skilled Nursing?
*   **FAC_OFFER_HOSPICE_PROG_DURING_REPT_PERIOD**: Offered Hospice Program?
*   **FAC_OFFER_ALZHEIMER_PROG**: Offered Alzheimer's Program?
*   **FAC_ACQUIRE_EQUIPMENT_OVER_500K**: Acquired equipment over $500k?
*   **PROJ_OVER_1M**: Projects over $1M?

## 3. Utilization (Patient Days, Census, Admissions, Discharges)
*   **BED_END**: Licensed Beds at End of Period
*   **BED_AVG**: Average Licensed Beds
*   **DAY_TOTL**: Total Patient Days
*   **OCCUP**: Occupancy Rate (%)
*   **ADMITS**: Total Admissions
*   **DISCHS**: Total Discharges
*   **DAY_SELF**: Patient Days - Self Pay
*   **DAY_OTH**: Patient Days - Other Payers
*   **DAY_SN**: Patient Days - Skilled Nursing
*   **TOT_PATS**: Total Patients
*   **TOT_DISCHARGES**: Total Discharges
*   **SN_DEC_31_PY_CEN**: Skilled Nursing Census - Dec 31 Prior Year
*   **SN_NURSING_PLUS_ADM**: Skilled Nursing + Admissions
*   **SN_MINUS_DISCHARGES**: Skilled Nursing - Discharges
*   **SN_DEC_31_CEN**: Skilled Nursing Census - Dec 31 Current Year
*   **SN_PAT_DAYS_FOR**: Skilled Nursing Patient Days
*   **SN_LIC_BEDS**: Skilled Nursing Licensed Beds
*   **SN_LIC_BED_DAYS**: Skilled Nursing Licensed Bed Days
*   **TOT_DEC_31_PY_CEN**: Total Census - Dec 31 Prior Year
*   **TOT_PLUS_ADM**: Total + Admissions
*   **TOT_MINUS_DISCHARGES**: Total - Discharges
*   **TOT_DEC_31_CEN**: Total Census - Dec 31 Current Year
*   **TOT_PAT_DAYS_FOR**: Total Patient Days
*   **TOT_LIC_BEDS**: Total Licensed Beds
*   **TOT_LIC_BED_DAYS**: Total Licensed Bed Days

### Admissions by Source
*   **PATS_ADMITTED_FROM_HOME**: From Home
*   **PATS_ADMITTED_FROM_HSP**: From Hospital
*   **PATS_ADMITTED_FROM_OTHER_LTC**: From Other Long Term Care
*   **PATS_ADMITTED_FROM_RESIDENTIAL_BOARD_AND_CARE**: From Residential Board & Care
*   **PATS_ADMITTED_FROM_OTHER**: From Other

### Discharges by Destination
*   **PATS_DISCHARGED_TO_HOME**: To Home
*   **PATS_DISCHARGED_TO_HSP**: To Hospital
*   **PATS_DISCHARGED_TO_OTHER_LTC**: To Other Long Term Care
*   **PATS_DISCHARGED_TO_RESIDENTIAL_BOARD_AND_CARE**: To Residential Board & Care
*   **PATS_DISCHARGED_TO_OTHER**: To Other
*   **PATS_DISCHARGED_TO_AWOL_AMA**: AWOL / Against Medical Advice
*   **PATS_DISCHARGED_TO_DEATH**: Deceased

### Patient Demographics & Types
*   **MEDICARE_PATS**: Medicare Patients
*   **MEDI_CAL_PATS**: Medi-Cal Patients
*   **MANAGED_CARE_PATS**: Managed Care Patients
*   **PRIVATE_INSURANCE_PATS**: Private Insurance Patients
*   **SELF_PAY_PATS**: Self Pay Patients
*   **ALL_OTHER_PATS**: All Other Patients
*   **PATS_DIAG_AIDS**: Patients Diagnosed with AIDS
*   **PATS_PRIMARY_OR_SECONDARY_ALZHEIMERS_DISEASE**: Patients with Alzheimer's

### Length of Stay (Discharges)
*   **DISCHARGES_LT_2_WKS**: < 2 Weeks
*   **DISCHARGES_2_WKS_AND_LT_1_MONTH**: 2 Weeks - 1 Month
*   **DISCHARGES_1_MONTH_AND_LT_3_MONTHS**: 1 - 3 Months
*   **DISCHARGES_3_MONTHS_AND_LT_7_MONTHS**: 3 - 7 Months
*   **DISCHARGES_7_MONTHS_AND_LT_1_YR**: 7 Months - 1 Year
*   **DISCHARGES_1_YR_AND_LT_2_YRS**: 1 - 2 Years
*   **DISCHARGES_2_YRS_AND_LT_3_YRS**: 2 - 3 Years
*   **DISCHARGES_3_YRS_AND_LT_5_YRS**: 3 - 5 Years
*   **DISCHARGES_5_YRS_AND_LT_7_YRS**: 5 - 7 Years
*   **DISCHARGES_7_YRS_AND_LT_10_YRS**: 7 - 10 Years
*   **DISCHARGES_10_YRS_AND_GREATER**: > 10 Years

## 4. Financial Data - Revenue
*   **GR_RT_TOTL**: Gross Routine Services Revenue Total
*   **GR_AN_TOTL**: Gross Ancillary Services Revenue Total
*   **DFR_TOTL**: Deductions from Revenue Total
*   **OTH_OP_REV**: Other Operating Revenue
*   **TOT_HC_REV**: Total Health Care Revenue
*   **NET_FRM_HC**: Net Income from Health Care Operations
*   **NONHC_NET**: Net Income from Non-Health Care Operations
*   **NET_INCOME**: Net Income
*   **GR_RT_SELF**: Gross Routine Rev - Self Pay
*   **GR_RT_OTH**: Gross Routine Rev - Other
*   **GR_SN**: Gross Rev - Skilled Nursing
*   **GR_AN_SELF_IP**: Gross Ancillary Rev - Self Pay Inpatient
*   **GR_PSUPPLY**: Gross Rev - Patient Supplies
*   **GR_SPSURF**: Gross Rev - Supplies Sold
*   **GR_PT**: Gross Rev - Physical Therapy
*   **GR_RT**: Gross Rev - Respiratory Therapy
*   **GR_OT**: Gross Rev - Occupational Therapy
*   **GR_SP**: Gross Rev - Speech Pathology
*   **GR_PHARM**: Gross Rev - Pharmacy
*   **GR_LAB**: Gross Rev - Laboratory
*   **GR_OTH_AN**: Gross Rev - Other Ancillary

## 5. Financial Data - Expenses
*   **TOT_HC_EXP**: Total Health Care Expenses
*   **EXP_SAL**: Salaries
*   **EXP_BEN**: Benefits
*   **EXP_OTHER**: Other Expenses
*   **WORK_COMP**: Workers Compensation
*   **EXP_SN**: Expenses - Skilled Nursing
*   **EXP_PSUPPL**: Expenses - Patient Supplies
*   **EXP_PT**: Expenses - Physical Therapy
*   **EXP_OT**: Expenses - Occupational Therapy
*   **EXP_SP**: Expenses - Speech Pathology
*   **EXP_PHARM**: Expenses - Pharmacy
*   **EXP_LAB**: Expenses - Laboratory
*   **EXP_OTH_AN**: Expenses - Other Ancillary
*   **EXP_POM**: Expenses - Plant Operations & Maintenance
*   **EXP_HKP**: Expenses - Housekeeping
*   **EXP_LL**: Expenses - Laundry & Linen
*   **EXP_DIET**: Expenses - Dietary
*   **EXP_SS**: Expenses - Social Services
*   **EXP_ACTV**: Expenses - Activities
*   **EXP_INSV**: Expenses - In-Service Education
*   **EXP_ADMN**: Expenses - Administration
*   **EXP_DPREC**: Expenses - Depreciation
*   **EXP_LEASE**: Expenses - Leases
*   **EXP_PRPTAX**: Expenses - Property Taxes
*   **EXP_PRPINS**: Expenses - Property Insurance
*   **EXP_BDEBT**: Expenses - Bad Debt

## 6. Balance Sheet & Financial Ratios
*   **CUR_ASST**: Current Assets
*   **NET_PPE**: Net Property, Plant, Equipment
*   **INV_OTH**: Investments/Other Assets
*   **TOT_ASST**: Total Assets
*   **CUR_LIAB**: Current Liabilities
*   **EQUITY**: Equity
*   **LIAB_EQ**: Total Liabilities & Equity
*   **LAND&IMP**: Land & Improvements
*   **LEASE_IMP**: Leasehold Improvements
*   **EQUIPMENT**: Equipment
*   **TOT_PPE**: Total Property, Plant, Equipment
*   **ACC_DEPREC**: Accumulated Depreciation
*   **CUR_RATIO**: Current Ratio
*   **ACID_RATIO**: Acid Test Ratio
*   **DAYS_AR**: Days in Accounts Receivable
*   **LTD_ASST**: Long Term Debt to Assets
*   **DEBT_COV**: Debt Coverage Ratio
*   **OP_MARGIN**: Operating Margin
*   **NET_RTN_EQ**: Net Return on Equity
*   **TRNOVR_OPR**: Operating Turnover
*   **ASST_EQUTY**: Assets to Equity Ratio
*   **PPE_BED**: PPE per Bed

## 7. Staffing (Hours & Wages)
*   **PRDHR_...**: Productive Hours (by role: MGT, GNP, RN, LVN, NA, TSP, PSY, OTH, POM, HKP, LL, DIET, SS, ACTV, INSV, ADMN, TOTL)
*   **S&W_...**: Salaries & Wages (by role: same as above)
*   **TMP_HR_...**: Temporary Staff Hours (by role)
*   **TMP_PD_...**: Temporary Staff Pay (by role)
*   **EMP_AVG**: Average Employees
*   **EMP_TRNOVR**: Employee Turnover
*   **EMP_CONT**: Employee Contracts

## 8. Other
*   **Utilization Reported?**: Data availability flag
*   **Financials Reported?**: Data availability flag
*   **Penalized?**: Enforcement action flag
*   **Total Records Found**: Metadata
*   **Total Amount Due Final**: Metadata
*   **BEG_DATE**: Report Period Begin
*   **END_DATE**: Report Period End
*   **DAY_PER**: Days in Period
*   **DATA_IND**: Data Indicator
*   **COMPARABLE**: Comparable Flag
*   **SUBMITTED_DT**: Submission Date
