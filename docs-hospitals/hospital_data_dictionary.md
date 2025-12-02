# Hospital Data Dictionary

**Total Columns**: 383

This document provides a comprehensive dictionary of the features available in the hospital dataset, categorized by operational theme.

## Target Variable
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `Penalized?` | Binary indicator of whether the facility has received enforcement actions or penalties. | int64 |

## Facility Profile
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `FAC_NAME_x` | Name of the healthcare facility. | object |
| `FAC_NO` | Unique facility identification number. | int64 |
| `FAC_NAME_y` | Name of the healthcare facility. | object |
| `COUNTY_x` | County where the facility is located. | object |
| `HSA` | Health Service Area code. | float64 |
| `HFPA` | Detailed description not available | float64 |
| `CITY` | Detailed description not available | object |
| `ZIP_CODE` | Zip code of the facility location. | int64 |
| `OWNER` | Ownership type of the facility. | object |
| `ORG_NAME` | Detailed description not available | object |
| `DIST_REV` | Detailed description not available | float64 |
| `FAC_NAME` | Name of the healthcare facility. | object |
| `FAC_CITY` | Detailed description not available | object |
| `FAC_ZIP` | Zip code of the facility location. | int64 |
| `FAC_OPERATED_THIS_YR` | Detailed description not available | object |
| `FAC_OP_PER_BEGIN_DT` | Detailed description not available | object |
| `FAC_OP_PER_END_DT` | Detailed description not available | object |
| `FAC_PAR_CORP_NAME` | Detailed description not available | object |
| `FAC_PAR_CORP_CITY` | Detailed description not available | object |
| `FAC_PAR_CORP_STATE` | Detailed description not available | object |
| `FAC_PAR_CORP_ZIP` | Zip code of the facility location. | int64 |
| `TEACH_HOSP` | Teaching hospital status. | object |
| `TEACH_RURAL` | Teaching hospital status. | object |
| `ASSEMBLY_DIST` | Detailed description not available | object |
| `SENATE_DIST` | Detailed description not available | object |
| `CONGRESS_DIST` | Detailed description not available | object |
| `CENSUS_KEY` | Census tract key. | float64 |
| `MED_SVC_STUDY_AREA` | Detailed description not available | object |
| `HEALTH_SVC_AREA` | Detailed description not available | object |
| `COUNTY_y` | County where the facility is located. | object |
| `FAC_ACQUIRE_EQUIP_OVER_500K` | Detailed description not available | object |

## Licensing & Capacity
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `LICENSE_NO_x` | License number or status details. | int64 |
| `LICENSE_NUMBER` | License number or status details. | float64 |
| `BED_LIC` | Number of licensed beds. | float64 |
| `BED_AVL` | Number of available beds. | float64 |
| `BED_STF` | Number of staffed beds. | float64 |
| `BED_ACUTE` | Number of acute care beds. | float64 |
| `BED_PSYCH` | Number of psychiatric beds. | float64 |
| `BED_CHEM` | Detailed description not available | float64 |
| `BED_REHAB` | Detailed description not available | float64 |
| `BED_LTC` | Number of long-term care beds. | float64 |
| `BED_RESDNT` | Detailed description not available | float64 |
| `OCC_LIC` | Detailed description not available | float64 |
| `LICENSE_NO_y` | License number or status details. | int64 |
| `LICENSE_EFF_DATE` | License number or status details. | object |
| `LICENSE_EXP_DATE` | License number or status details. | object |
| `LICENSE_STATUS` | License number or status details. | object |
| `FACILITY_LEVEL` | Detailed description not available | object |
| `LIC_CAT` | Detailed description not available | object |
| `LICEE_TOC` | Detailed description not available | object |
| `MED_SURG_LIC_BEDS` | Detailed description not available | float64 |
| `PERINATAL_LIC_BEDS` | Detailed description not available | float64 |
| `PEDIATRIC_LIC_BEDS` | Detailed description not available | float64 |
| `IC_LIC_BEDS` | Detailed description not available | float64 |
| `CORONARY_CARE_LIC_BEDS` | Detailed description not available | float64 |
| `ACUTE_RESPIRATORY_CARE_LIC_BEDS` | Detailed description not available | float64 |
| `BURN_LIC_BEDS` | Detailed description not available | float64 |
| `IC_NEWBORN_LIC_BEDS` | Detailed description not available | float64 |
| `REHAB_CTR_LIC_BEDS` | Detailed description not available | float64 |
| `GAC_SUBTOT_LIC_BEDS` | Detailed description not available | float64 |
| `CHEM_DEPEND_RECOVERY_LIC_BEDS` | Detailed description not available | float64 |
| `ACUTE_PSYCHIATRIC_LIC_BEDS` | Detailed description not available | float64 |
| `SN_LIC_BEDS` | Detailed description not available | float64 |
| `INTERMEDIATE_CARE_LIC_BEDS` | Detailed description not available | float64 |
| `INTERMEDIATE_CARE_DEV_DIS_LIC_BEDS` | Detailed description not available | float64 |
| `TOT_LIC_BEDS` | Detailed description not available | float64 |
| `GAC_CDRS_LIC_BEDS` | Detailed description not available | float64 |
| `ACUTE_PSYCH_LIC_BEDS` | Detailed description not available | float64 |
| `NEWBORN_NURSERY_BASSINETS` | Number of newborn bassinets. | float64 |
| `GEN_ACUTE_CARE_SN_SWING_BEDS` | Detailed description not available | float64 |
| `MED_SURG_LIC_BED_DAYS` | Detailed description not available | float64 |
| `PERINATAL_LIC_BED_DAYS` | Detailed description not available | float64 |
| `PEDIATRIC_LIC_BED_DAYS` | Detailed description not available | float64 |
| `IC_LIC_BED_DAYS` | Detailed description not available | float64 |
| `CORONARY_CARE_LIC_BED_DAYS` | Detailed description not available | float64 |
| `ACUTE_RESPIRATORY_CARE_LIC_BED_DAYS` | Detailed description not available | float64 |
| `BURN_LIC_BED_DAYS` | Detailed description not available | float64 |
| `IC_NEWBORN_LIC_BED_DAYS` | Detailed description not available | float64 |
| `REHAB_CTR_LIC_BED_DAYS` | Detailed description not available | float64 |
| `GAC_SUBTOT_LIC_BED_DAYS` | Detailed description not available | float64 |
| `CHEM_DEPEND_RECOVERY_LIC_BED_DAYS` | Detailed description not available | float64 |
| `ACUTE_PSYCHIATRIC_LIC_BED_DAYS` | Detailed description not available | float64 |
| `SN_LIC_BED_DAYS` | Detailed description not available | float64 |
| `INTERMEDIATE_CARE_LIC_BED_DAYS` | Detailed description not available | float64 |
| `INTERMEDIATE_CARE_DEV_DIS_LIC_BED_DAYS` | Detailed description not available | float64 |
| `TOT_LIC_BED_DAYS` | Detailed description not available | float64 |
| `LIC_ED_LEV_BEGIN` | Detailed description not available | object |
| `LIC_ED_LEV_END` | Detailed description not available | object |

## Utilization & Patient Activity
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `DAY_PER` | Detailed description not available | float64 |
| `DAY_MCAR_TR` | Medicare patient activity. | float64 |
| `DAY_MCAR_MC` | Medicare patient activity. | float64 |
| `DAY_MCAL_TR` | Medi-Cal patient activity. | float64 |
| `DAY_MCAL_MC` | Medi-Cal patient activity. | float64 |
| `DAY_CNTY` | County Indigent patient activity. | float64 |
| `DAY_THRD_TR` | Third Party/Private Insurance patient activity. | float64 |
| `DAY_THRD_MC` | Third Party/Private Insurance patient activity. | float64 |
| `DAY_OTH_IND` | Detailed description not available | float64 |
| `DAY_OTH` | Detailed description not available | float64 |
| `DAY_TOT` | Total patient days. | float64 |
| `DIS_MCAR_TR` | Medicare patient activity. | float64 |
| `DIS_MCAR_MC` | Medicare patient activity. | float64 |
| `DIS_MCAL_TR` | Medi-Cal patient activity. | float64 |
| `DIS_MCAL_MC` | Medi-Cal patient activity. | float64 |
| `DIS_CNTY` | County Indigent patient activity. | float64 |
| `DIS_THRD_TR` | Third Party/Private Insurance patient activity. | float64 |
| `DIS_THRD_MC` | Third Party/Private Insurance patient activity. | float64 |
| `DIS_OTH_IND` | Detailed description not available | float64 |
| `DIS_OTH` | Detailed description not available | float64 |
| `DIS_TOT` | Total patient discharges. | float64 |
| `DAY_ACUTE` | Detailed description not available | float64 |
| `DAY_PSYCH` | Detailed description not available | float64 |
| `DAY_CHEM` | Detailed description not available | float64 |
| `DAY_REHAB` | Detailed description not available | float64 |
| `DAY_LTC` | Detailed description not available | float64 |
| `DAY_RESDNT` | Detailed description not available | float64 |
| `DIS_ACUTE` | Detailed description not available | float64 |
| `DIS_PSYCH` | Detailed description not available | float64 |
| `DIS_CHEM` | Detailed description not available | float64 |
| `DIS_REHAB` | Detailed description not available | float64 |
| `DIS_LTC` | Detailed description not available | float64 |
| `DIS_RESDNT` | Detailed description not available | float64 |
| `OCC_AVL` | Detailed description not available | float64 |
| `ALOS_ALL` | Average Length of Stay (days). | float64 |
| `ALOS_EXLTC` | Average Length of Stay (days). | float64 |
| `DAY_NURSRY` | Detailed description not available | float64 |
| `DIS_NURSRY` | Detailed description not available | float64 |
| `VIS_MCAR_TR` | Medicare patient activity. | float64 |
| `VIS_MCAR_MC` | Medicare patient activity. | float64 |
| `VIS_MCAL_TR` | Medi-Cal patient activity. | float64 |
| `VIS_MCAL_MC` | Medi-Cal patient activity. | float64 |
| `VIS_CNTY` | County Indigent patient activity. | float64 |
| `VIS_THRD_TR` | Third Party/Private Insurance patient activity. | float64 |
| `VIS_THRD_MC` | Third Party/Private Insurance patient activity. | float64 |
| `VIS_OTH_IND` | Detailed description not available | float64 |
| `VIS_OTH` | Detailed description not available | float64 |
| `VIS_TOT` | Total outpatient visits. | float64 |
| `VIS_ER` | Emergency room visits. | float64 |
| `VIS_CLIN` | Detailed description not available | float64 |
| `VIS_HOME` | Detailed description not available | float64 |
| `VIS_REF_OP` | Detailed description not available | float64 |
| `IC_INTRA_TRANSFERS` | Detailed description not available | float64 |
| `MED_SURG_CEN_DAYS` | Detailed description not available | float64 |
| `PERINATAL_CEN_DAYS` | Detailed description not available | float64 |
| `IC_CEN_DAYS` | Detailed description not available | float64 |
| `GAC_SUBTOT_CEN_DAYS` | Detailed description not available | float64 |
| `TOT_CEN_DAYS` | Detailed description not available | float64 |
| `NEWBORN_NURSERY_CEN_DAYS` | Detailed description not available | float64 |
| `MED_SURG_ALOS_CY` | Average Length of Stay (days). | float64 |
| `IC_ALOS_CY` | Average Length of Stay (days). | float64 |
| `GAC_SUBTOT_ALOS_CY` | Average Length of Stay (days). | float64 |
| `TOT_ALOS_CY` | Average Length of Stay (days). | float64 |
| `MED_SURG_ALOS_PY` | Average Length of Stay (days). | float64 |
| `PERINATAL_ALOS_PY` | Average Length of Stay (days). | float64 |
| `PEDIATRIC_ALOS_PY` | Average Length of Stay (days). | float64 |
| `IC_ALOS_PY` | Average Length of Stay (days). | float64 |
| `CORONARY_CARE_ALOS_PY` | Average Length of Stay (days). | float64 |
| `ACUTE_RESPIRATORY_CARE_ALOS_PY` | Average Length of Stay (days). | float64 |
| `BURN_ALOS_PY` | Average Length of Stay (days). | float64 |
| `IC_NEWBORN_ALOS_PY` | Average Length of Stay (days). | float64 |
| `REHAB_CTR_ALOS_PY` | Average Length of Stay (days). | float64 |
| `GAC_SUBTOT_ALOS_PY` | Average Length of Stay (days). | float64 |
| `CHEM_DEPEND_RECOV_ALOS_PY` | Average Length of Stay (days). | float64 |
| `ACUTE_PSYCHIATRIC_ALOS_PY` | Average Length of Stay (days). | float64 |
| `SN_ALOS_PY` | Average Length of Stay (days). | float64 |
| `INTERMEDIATE_CARE_ALOS_PY` | Average Length of Stay (days). | float64 |
| `INTERMEDIATE_CARE_DEV_DIS_ALOS_PY` | Average Length of Stay (days). | float64 |
| `TOT_ALOS_PY` | Average Length of Stay (days). | float64 |
| `GAC_CDRS_ALOS_PY` | Average Length of Stay (days). | float64 |
| `ACUTE_PSYCH_CDRS_ALOS_PY` | Average Length of Stay (days). | float64 |
| `EMS_VISITS_NON_URGENT_ADMITTED` | Detailed description not available | float64 |
| `EMS_VISITS_URGENT_ADMITTED` | Detailed description not available | float64 |
| `EMS_VISITS_MODERATE_ADMITTED` | Detailed description not available | float64 |
| `EMS_VISITS_SEVERE_ADMITTED` | Detailed description not available | float64 |
| `EMS_VISITS_CRITICAL_ADMITTED` | Detailed description not available | float64 |
| `ADMITTED_FROM_EMER_DEPT_TOT` | Detailed description not available | float64 |

## Financials - Revenue
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `GR_PT_REV` | Gross patient revenue. | float64 |
| `DED_FR_REV` | Detailed description not available | float64 |
| `TOT_CAP_REV` | Capitation revenue. | float64 |
| `NET_PT_REV` | Net patient revenue. | float64 |
| `OTH_OP_REV` | Detailed description not available | float64 |
| `NET_FRM_OP` | Detailed description not available | float64 |
| `NONOP_REV` | Detailed description not available | float64 |
| `NET_INCOME` | Net income (Profit/Loss). | float64 |
| `GR_REV_DLY` | Detailed description not available | float64 |
| `GR_REV_AMB` | Detailed description not available | float64 |
| `GR_REV_ANC` | Detailed description not available | float64 |
| `GR_IP_MCAR_TR` | Gross Inpatient Revenue. | float64 |
| `GR_IP_MCAR_MC` | Gross Inpatient Revenue. | float64 |
| `GR_IP_MCAL_TR` | Gross Inpatient Revenue. | float64 |
| `GR_IP_MCAL_MC` | Gross Inpatient Revenue. | float64 |
| `GR_IP_CNTY` | Gross Inpatient Revenue. | float64 |
| `GR_IP_THRD_TR` | Gross Inpatient Revenue. | float64 |
| `GR_IP_THRD_MC` | Gross Inpatient Revenue. | float64 |
| `GR_IP_OTH_IND` | Gross Inpatient Revenue. | float64 |
| `GR_IP_OTH` | Gross Inpatient Revenue. | float64 |
| `GR_IP_TOT` | Gross Inpatient Revenue. | float64 |
| `GR_OP_MCAR_TR` | Gross Outpatient Revenue. | float64 |
| `GR_OP_MCAR_MC` | Gross Outpatient Revenue. | float64 |
| `GR_OP_MCAL_TR` | Gross Outpatient Revenue. | float64 |
| `GR_OP_MCAL_MC` | Gross Outpatient Revenue. | float64 |
| `GR_OP_CNTY` | Gross Outpatient Revenue. | float64 |
| `GR_OP_THRD_TR` | Gross Outpatient Revenue. | float64 |
| `GR_OP_THRD_MC` | Gross Outpatient Revenue. | float64 |
| `GR_OP_OTH_IND` | Gross Outpatient Revenue. | float64 |
| `GR_OP_OTH` | Gross Outpatient Revenue. | float64 |
| `GR_OP_TOT` | Gross Outpatient Revenue. | float64 |
| `BAD_DEBT` | Provision for bad debts. | float64 |
| `CHAR_HB` | Charity care charges. | float64 |
| `CHAR_OTH` | Charity care charges. | float64 |
| `DED_OTH` | Detailed description not available | float64 |
| `CAP_REV_MCAR` | Revenue from Medicare. | float64 |
| `CAP_REV_MCAL` | Revenue from Medi-Cal. | float64 |
| `CAP_REV_CNTY` | Capitation revenue. | float64 |
| `CAP_REV_THRD` | Capitation revenue. | float64 |
| `CONTRIBTNS` | Detailed description not available | float64 |
| `CNTY_APPRO` | Detailed description not available | float64 |
| `NET_PPE` | Detailed description not available | float64 |
| `INV_OTH` | Detailed description not available | float64 |
| `NET_LTDEBT` | Detailed description not available | float64 |
| `CAP_LEASE` | Detailed description not available | float64 |

## Financials - Expenses
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `TOT_OP_EXP` | Total operating expenses. | float64 |
| `NONOP_EXP` | Detailed description not available | float64 |
| `EXP_DLY` | Detailed description not available | float64 |
| `EXP_AMB` | Detailed description not available | float64 |
| `EXP_ANC` | Ancillary service expenses. | float64 |
| `EXP_PIP` | Detailed description not available | float64 |
| `EXP_POP` | Detailed description not available | float64 |
| `EXP_RES` | Detailed description not available | float64 |
| `EXP_ED` | Detailed description not available | float64 |
| `EXP_GEN` | General services expenses. | float64 |
| `EXP_FISC` | Detailed description not available | float64 |
| `EXP_ADM` | Detailed description not available | float64 |
| `EXP_UNASSG` | Detailed description not available | float64 |
| `EXP_SAL` | Salary expenses. | float64 |
| `EXP_BEN` | Benefits expenses. | float64 |
| `EXP_PHYS` | Detailed description not available | float64 |
| `EXP_OTHPRO` | Detailed description not available | float64 |
| `EXP_SUPP` | Supply expenses. | float64 |
| `EXP_PURCH` | Detailed description not available | float64 |
| `EXP_DEPRE` | Detailed description not available | float64 |
| `EXP_LEASES` | Detailed description not available | float64 |
| `EXP_INSUR` | Detailed description not available | float64 |
| `EXP_INTRST` | Detailed description not available | float64 |
| `EXP_OTH` | Detailed description not available | float64 |
| `ACC_DEPRE` | Detailed description not available | float64 |

## Financials - Balance Sheet
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `CUR_ASST` | Current assets. | float64 |
| `ASST_LIMTD` | Detailed description not available | float64 |
| `INTAN_ASST` | Detailed description not available | float64 |
| `TOT_ASST` | Total assets. | float64 |
| `CUR_LIAB` | Detailed description not available | float64 |
| `DEF_CRED` | Detailed description not available | float64 |
| `EQUITY` | Total equity. | float64 |
| `LIAB_EQ` | Detailed description not available | float64 |
| `CASH` | Detailed description not available | float64 |
| `BLDGS` | Detailed description not available | float64 |
| `EQUIPMENT` | Detailed description not available | float64 |
| `TOT_PPE` | Property, Plant, and Equipment. | float64 |
| `MORT_PAY` | Detailed description not available | float64 |
| `BOND_PAY` | Detailed description not available | float64 |
| `TOT_LTDEBT` | Total long-term debt. | float64 |

## Staffing & Hours
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `HOSP_FTE` | Total hospital Full-Time Equivalents. | float64 |
| `NURS_FTE` | Nursing Full-Time Equivalents. | float64 |
| `PROD_HRS` | Productive hours worked. | float64 |
| `PAID_HRS` | Total paid hours. | float64 |
| `MED_STAFF` | Detailed description not available | float64 |
| `STDNT_FTE` | Detailed description not available | float64 |

## Services & Operations
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `SURG_IP` | Inpatient surgeries performed. | float64 |
| `SURG_OP` | Outpatient surgeries performed. | float64 |
| `C_SECTIONS` | Detailed description not available | float64 |
| `INTER_TFR` | Detailed description not available | float64 |
| `INTER_PAY` | Detailed description not available | float64 |
| `SHORT_DOYLE_SERVICES_OFFERED` | Service offered indicator. | object |
| `INPATIENT_HOSPICE_PROG_OFFERED` | Service offered indicator. | object |
| `INPATIENT_PALLIATIVE_CARE_PROG_OFFERED` | Service offered indicator. | object |
| `OUTPATIENT_PALLIATIVE_CARE_SERV_OFFERED` | Service offered indicator. | object |
| `MED_SURG_DISCHARGES` | Detailed description not available | float64 |
| `EMS_VISITS_NON_URGENT_TOT` | Emergency Medical Services visits. | float64 |
| `EMS_VISITS_URGENT_TOT` | Emergency Medical Services visits. | float64 |
| `EMS_VISITS_MODERATE_TOT` | Emergency Medical Services visits. | float64 |
| `EMS_VISITS_SEVERE_TOT` | Emergency Medical Services visits. | float64 |
| `EMS_VISITS_CRITICAL_TOT` | Emergency Medical Services visits. | float64 |
| `EMER_DEPT_VISITS_NOT_RESULT_ADMISSIONS_TOT` | Detailed description not available | float64 |
| `EMER_MED_TREAT_STATIONS_ON_1231` | Detailed description not available | float64 |
| `NON_EMER_VISITS_IN_EMER_DEPT` | Detailed description not available | float64 |
| `EMER_REGISTRATIONS_PATS_LEAVE_WO_BEING_SEEN` | Detailed description not available | float64 |
| `EMER_DEPT_AMBULANCE_DIVERSION_HOURS` | Detailed description not available | object |
| `ER_TRAFFIC_TOT` | Detailed description not available | float64 |
| `INPATIENT_SURG_OPER` | Outpatient surgeries performed. | float64 |
| `OUTPATIENT_SURG_OPER` | Outpatient surgeries performed. | float64 |
| `INPAT_OUTPAT_OPER_RM` | Detailed description not available | float64 |
| `OPER_RM_TOT` | Detailed description not available | float64 |
| `OFFER_AMBULATORY_SURG_PROG` | Service offered indicator. | object |
| `INPATIENT_SURG_OPER_RM_MINS` | Outpatient surgeries performed. | float64 |
| `OUTPATIENT_SURG_OPER_RM_MINS` | Outpatient surgeries performed. | float64 |
| `INPATIENT_AVG_PER_SURGERY` | Detailed description not available | float64 |
| `OUTPATIENT_AVG_PER_SURGERY` | Detailed description not available | float64 |
| `PROJ_OVER_1M` | Detailed description not available | object |

## Other/Uncategorized
| Column Name | Comprehensive Description | Type |
|---|---|---|
| `Year` | Detailed description not available | int64 |
| `Utilization Reported?` | Detailed description not available | int64 |
| `Financials Reported?` | Detailed description not available | int64 |
| `HCAI_ID` | Detailed description not available | float64 |
| `FACID` | Detailed description not available | float64 |
| `FACNAME` | Detailed description not available | object |
| `Total Records Found` | Detailed description not available | int64 |
| `Total Amount Due Final` | Detailed description not available | int64 |
| `BEG_DATE` | Detailed description not available | object |
| `END_DATE` | Detailed description not available | object |
| `DATA_IND` | Detailed description not available | object |
| `AUDIT_IND` | Detailed description not available | object |
| `TYPE_CNTRL` | Detailed description not available | object |
| `TYPE_CARE` | Detailed description not available | object |
| `TYPE_HOSP` | Detailed description not available | object |
| `MCAR_PRO#` | Detailed description not available | object |
| `BAS_NURSRY` | Detailed description not available | float64 |
| `DAYS_PIPS` | Detailed description not available | float64 |
| `OP_ROOM` | Detailed description not available | float64 |
| `OP_MIN_IP` | Detailed description not available | float64 |
| `OP_MIN_OP` | Detailed description not available | float64 |
| `INC_TAX` | Detailed description not available | float64 |
| `EXT_ITEM` | Detailed description not available | float64 |
| `C_ADJ_MCAR_TR` | Detailed description not available | float64 |
| `C_ADJ_MCAR_MC` | Detailed description not available | float64 |
| `C_ADJ_MCAL_TR` | Detailed description not available | float64 |
| `C_ADJ_MCAL_MC` | Detailed description not available | float64 |
| `DISP_855` | Detailed description not available | float64 |
| `C_ADJ_CNTY` | Detailed description not available | float64 |
| `C_ADJ_THRD_TR` | Detailed description not available | float64 |
| `C_ADJ_THRD_MC` | Detailed description not available | float64 |
| `SUB_INDGNT` | Detailed description not available | float64 |
| `NETRV_MCAR_TR` | Detailed description not available | float64 |
| `NETRV_MCAR_MC` | Detailed description not available | float64 |
| `NETRV_MCAL_TR` | Detailed description not available | float64 |
| `NETRV_MCAL_MC` | Detailed description not available | float64 |
| `NETRV_CNTY` | Detailed description not available | float64 |
| `NETRV_THRD_TR` | Detailed description not available | float64 |
| `NETRV_THRD_MC` | Detailed description not available | float64 |
| `NETRV_OTH_IND` | Detailed description not available | float64 |
| `NETRV_OTH` | Detailed description not available | float64 |
| `DISP_TRNFR` | Detailed description not available | float64 |
| `INC_INVEST` | Detailed description not available | float64 |
| `CONST_PROG` | Detailed description not available | float64 |
| `ALLOW_UNCOLL` | Detailed description not available | float64 |
| `CUR_MAT` | Detailed description not available | float64 |
| `INTER-REC` | Detailed description not available | float64 |
| `NON_PRD_HR` | Detailed description not available | float64 |
| `PRD_HR_MGT` | Detailed description not available | float64 |
| `PRD_HR_TCH` | Detailed description not available | float64 |
| `PRD_HR_RN` | Detailed description not available | float64 |
| `PRD_HR_LVN` | Detailed description not available | float64 |
| `PRD_HR_AID` | Detailed description not available | float64 |
| `PRD_HR_CLR` | Detailed description not available | float64 |
| `PRD_HR_ENV` | Detailed description not available | float64 |
| `PRD_HR_OTH` | Detailed description not available | float64 |
| `CNT_HR_RN` | Detailed description not available | float64 |
| `CNT_HR_OTH` | Detailed description not available | float64 |
| `PRD_HR_DLY` | Detailed description not available | float64 |
| `PRD_HR_AMB` | Detailed description not available | float64 |
| `PRD_HR_ANC` | Detailed description not available | float64 |
| `PRD_HR_ED` | Detailed description not available | float64 |
| `PRD_HR_GEN` | Detailed description not available | float64 |
| `PRD_HR_FIS` | Detailed description not available | float64 |
| `PRD_HR_ADM` | Detailed description not available | float64 |
| `PRD_HR_NON` | Detailed description not available | float64 |
| `PD_HR_DLY` | Detailed description not available | float64 |
| `PD_HR_AMB` | Detailed description not available | float64 |
| `PD_HR_ANC` | Detailed description not available | float64 |
| `PD_HR_ED` | Detailed description not available | float64 |
| `PD_HR_GEN` | Detailed description not available | float64 |
| `PD_HR_FIS` | Detailed description not available | float64 |
| `PD_HR_ADM` | Detailed description not available | float64 |
| `PD_HR_NON` | Detailed description not available | float64 |
| `SUBMITTED_DT` | Detailed description not available | object |
| `PRIN_SERVICE_TYPE` | Detailed description not available | object |
| `PERINATAL_DISCHARGES` | Detailed description not available | float64 |
| `IC_DISCHARGES` | Detailed description not available | float64 |
| `GAC_SUBTOT_DISCHARGES` | Detailed description not available | float64 |
| `TOT_DISCHARGES` | Detailed description not available | float64 |
| `NEWBORN_NURSERY_INFANTS` | Detailed description not available | float64 |
| `AVAIL_SERVICES_LAB_24HR` | Detailed description not available | object |
| `AVAIL_SERVICES_PHYSICIAN_24HR` | Detailed description not available | object |
| `AVAIL_SERVICES_RADIOLOGY_24HR` | Detailed description not available | object |
| `year` | Detailed description not available | int64 |

