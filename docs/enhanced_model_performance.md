# Enhanced Model Performance Report

**Generated**: 2025-11-24 15:23:09

## Training Configuration

- **Class Balancing**: class_weights
- **Hyperparameter Tuning**: Enabled
- **Ensemble**: Enabled
- **SHAP**: Enabled

## Model Comparison

| Model | ROC-AUC | F1-Score | Precision | Recall |
|-------|---------|----------|-----------|--------|
| Random Forest | 0.7812 | 0.5514 | 0.6258 | 0.4928 |
| XGBoost | 0.8035 | 0.5957 | 0.6627 | 0.5411 |
| Logistic Regression | 0.7661 | 0.6034 | 0.5447 | 0.6763 |

## Best Model: XGBoost

- **ROC-AUC**: 0.8035
- **F1-Score**: 0.5957
- **Precision**: 0.6627
- **Recall**: 0.5411

## Top 10 Feature Importances

- **LIC_CAT_x_SNF**: 0.024258
- **TOT_DEC_31_PY_CEN**: 0.021613
- **EXP_ADMN**: 0.020475
- **DISCHARGES_7_MONTHS_AND_LT_1_YR**: 0.015977
- **SELF_PAY_PATS**: 0.014841
- **LEGAL_ORG_Other**: 0.013502
- **DAY_SN**: 0.013250
- **GR_PHARM**: 0.012389
- **HFPA**: 0.011906
- **TOT_LIC_BED_DAYS**: 0.009486
