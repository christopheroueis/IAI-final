# Data Visualizations

This folder contains comprehensive visualizations for the CareEnforced AI model analysis.

## SHAP Interpretability Visualizations (10 plots)

### Summary Plots
- **1_shap_summary_bar.png** - Feature importance ranking based on mean absolute SHAP values
- **2_shap_summary_beeswarm.png** - Feature impact distribution showing both magnitude and direction

### Individual Prediction Analysis
- **3_shap_waterfall.png** - How individual features push prediction from base value for a sample
- **4_shap_force_plot_1.png** - Force plot visualization (Prediction 1)
- **4_shap_force_plot_2.png** - Force plot visualization (Prediction 2)
- **4_shap_force_plot_3.png** - Force plot visualization (Prediction 3)

### Feature Dependence Analysis
- **5_shap_dependence_HSA_11_-_Los_Angeles.png** - Health Service Area 11 impact
- **5_shap_dependence_EXP_ADMN.png** - Administrative Expenses impact
- **5_shap_dependence_DAY_TOTL.png** - Total Patient Days impact
- **5_shap_dependence_COUNTY_x_Los_Angeles.png** - Los Angeles County (x) impact
- **5_shap_dependence_COUNTY_y_Los_Angeles.png** - Los Angeles County (y) impact

## Model Performance Visualizations (6 plots)

### Discrimination Performance
- **7_roc_curve_comparison.png** - ROC curves comparing all models (Baseline RF, Enhanced RF, Enhanced LR)
- **8_precision_recall_curve.png** - Precision-Recall curves showing trade-offs

### Prediction Quality
- **9_confusion_matrices.png** - Side-by-side confusion matrices for all models
- **10_calibration_plot.png** - Model calibration showing predicted vs actual probabilities

### Feature Analysis
- **11_feature_importance_rf.png** - Top 20 features by importance (Random Forest)

### Overall Comparison
- **12_metrics_comparison.png** - Side-by-side comparison of all metrics (ROC-AUC, F1, Precision, Recall)

## How to Regenerate

```bash
# SHAP visualizations (Random Forest)
.venv/bin/python scripts/visualize_shap.py

# Model performance visualizations
.venv/bin/python scripts/visualize_model_performance.py
```

## Key Insights from Visualizations

### From SHAP Analysis
1. **Los Angeles Region** (HSA 11) is the top risk factor
2. **Administrative Expenses** and **Patient Days** strongly influence predictions
3. Feature impacts are generally consistent across predictions

### From Performance Metrics
1. **Ensemble achieves highest ROC-AUC** (0.8151)
2. **Enhanced Logistic Regression has best recall** (69.08%)
3. **Trade-off**: Higher recall comes with lower precision (60-66%)
4. **Calibration**: Models are reasonably well-calibrated

## File Organization

Total: 17 visualization files
- 10 SHAP interpretability plots
- 6 model performance comparison plots
- All saved as high-resolution PNG (300 DPI)
