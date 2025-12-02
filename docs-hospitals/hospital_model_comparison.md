# Hospital Model Comparison

**Note**: Penalty-related features (`Total Amount Due Final`, `Total Records Found`) have been excluded from the model to prevent data leakage.

## Model Performance
| Model | Accuracy | ROC-AUC | Recall | Precision |
|---|---|---|---|---|
| Random Forest | 0.8439 | 0.7950 | 0.1333 | 0.4000 |
| Logistic Regression | 0.8195 | 0.7036 | 0.4000 | 0.3871 |
| LightGBM | 0.8585 | 0.8021 | 0.3000 | 0.5294 |
| XGBoost | 0.8537 | 0.7644 | 0.3000 | 0.5000 |

## Top 20 Features (Random Forest)
| Feature | Full Name | Importance |
|---|---|---|
| `num__GR_PT_REV` | Gross PT REV | 0.0106 |
| `num__GR_REV_AMB` | Gross Revenue - Ambulatory | 0.0099 |
| `num__DAY_ACUTE` | Days - Acute Care | 0.0094 |
| `num__VIS_TOT` | Visits - TOT | 0.0093 |
| `num__IC_LIC_BED_DAYS` | Intensive Care Licensed Beds - DAYS | 0.0089 |
| `num__DAY_MCAL_MC` | Days - Medi-Cal MC | 0.0080 |
| `num__DIS_MCAL_MC` | Discharges - Medi-Cal MC | 0.0078 |
| `num__TOT_LIC_BED_DAYS` | Total Licensed Beds - DAYS | 0.0076 |
| `num__NETRV_MCAL_MC` | NETRV Medi-Cal MC | 0.0074 |
| `num__EXP_ANC` | Expense - Ancillary | 0.0072 |
| `num__VIS_ER` | Visits - ER | 0.0071 |
| `num__C_ADJ_MCAR_MC` | C ADJ Medicare MC | 0.0070 |
| `num__EXP_DLY` | Expense - Daily | 0.0070 |
| `num__NURS_FTE` | Nursing Full-Time Equivalents | 0.0069 |
| `num__BED_AVL` | Beds - AVL | 0.0069 |
| `num__ALOS_EXLTC` | Average Length of Stay EXLong-Term Care | 0.0066 |
| `num__NETRV_THRD_TR` | NETRV Third Party TR | 0.0065 |
| `num__SURG_OP` | Surgery OP | 0.0064 |
| `num__VIS_MCAR_MC` | Visits - Medicare MC | 0.0064 |
| `num__DIS_TOT` | Discharges - TOT | 0.0062 |
