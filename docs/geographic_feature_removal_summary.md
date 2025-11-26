# Geographic Feature Removal Summary

## Changes Made

### 1. Removed Geographic Features
**Excluded from Training:**
- `COUNTY_x` - County (x-axis)
- `COUNTY_y` - County (y-axis)  
- `HSA` - Health Service Area

**Rationale:**
- Geographic location is **not actionable** - facilities cannot change their location
- LA region (HSA 11, LA County) was top predictor but represents enforcement bias, not facility quality
- Removal creates **fairer, more actionable** predictions focused on operational factors

### 2. Performance Impact

#### Before (With LA Geographic Features)
| Model | ROC-AUC | Recall |
|-------|---------|--------|
| Baseline RF | **0.8088** | 46.38% |
| Enhanced LR | 0.8035 | **69.08%** |
| Ensemble | 0.8151 | 62.80% |

#### After (Without Geographic Features)
| Model | ROC-AUC | Recall |
|-------|---------|--------|
| Baseline RF | **0.7861** | 44.93% |
| Enhanced RF | 0.7812 | 49.28% |
| Enhanced XGBoost | **0.8035** | 54.11% |
| Enhanced LR | 0.7661 | **67.63%** |

**Key Findings:**
- ROC-AUC decreased by **0.02-0.04** across models (expected trade-off)
- **Performance remains strong** - still above 0.76 ROC-AUC
- **XGBoost emerged** as best balanced model (ROC-AUC: 0.8035, Recall: 54.11%)
- Logistic Regression maintains **highest recall** (67.63%)
- Trade-off is **acceptable** for fairness and actionability

### 3. New Top Features (Post-Removal)

Based on feature importance visualizations, the new top risk drivers are:

**Top 5 Actionable Features:**
1. **Administrative Expenses** - Operational efficiency indicator
2. **Total Patient Days** - Utilization metric
3. **Employee Benefits** - Staffing cost indicator
4. **Net Income** - Financial health
5. **RN Hours per Patient Day** - Staffing quality

**All features are now actionable** - facilities can improve these through:
- Better financial management
- Improved staffing ratios
- Operational efficiency initiatives

### 4. Visualizations Updated

**All 16 visualizations regenerated with:**
- ✅ Geographic features removed
- ✅ Full, readable feature names (not abbreviations)
- ✅ Updated performance metrics

**SHAP Visualizations (10):**
- Summary bar chart
- Beeswarm plot
- Waterfall plot
- 3 force plots
- 5 dependence plots

**Model Performance (6):**
- ROC curves
- Precision-Recall curves
- Confusion matrices
- Calibration plot
- Feature importance chart
- Metrics comparison

### 5. Implementation Changes

**Training Scripts Updated:**
- `scripts/train_model.py` - Baseline training
- `scripts/train_model_enhanced.py` - Enhanced training

**Feature Name Mapping:**
- `scripts/feature_names.py` - New module for readable labels

**Visualization Scripts:**
- `scripts/visualize_shap.py` - Updated with feature mapping
- `scripts/visualize_model_performance.py` - Updated with feature mapping

### 6. Model Artifacts Updated

**Retrained Models:**
- `models/risk_model.pkl` - Baseline RF (no geographic features)
- `models/random_forest_model.pkl` - Enhanced RF
- `models/xgboost_model.pkl` - **NEW: Enhanced XGBoost (best model)**
- `models/logistic_regression_model.pkl` - Enhanced LR
- `models/risk_model_enhanced.pkl` - Best single model (XGBoost)
- `models/ensemble_metadata.json` - 3-model ensemble weights

## Recommendations

### For Production Deployment
1. **Use Enhanced XGBoost** (ROC-AUC: 0.8035, balanced performance)
2. **Alternative: Enhanced Logistic Regression** if recall is priority (67.63%)
3. **Ensemble needs debugging** - appears to have loading issues

### Next Steps
1. Fix ensemble prediction logic (currently showing poor performance)
2. Update frontend to display new top features
3. Test API predictions without geographic features
4. Update user documentation

## Conclusion

✅ **Successfully removed geographic bias**  
✅ **Maintained strong predictive performance** (>0.76 ROC-AUC)  
✅ **All features now actionable** - facilities can improve their scores  
✅ **Visualizations updated** with readable names  
✅ **Fairer model** - no regional discrimination  

**Trade-off:** Small performance decrease (~0.02-0.03 ROC-AUC) is acceptable for improved fairness and actionability.
