# Model Selection Guide for CareEnforced AI

## Executive Summary

**Recommendation**: Use **Enhanced XGBoost** for production deployment.

- **Best overall performance**: Highest ROC-AUC (0.8035), balanced precision/recall
- **No geographic bias**: All features are actional
- **Strong recall**: Catches 54.11% of penalized facilities (vs 44.93% baseline)
- **Stable**: Well-calibrated, reliable predictions

---

## All Models Compared

### Performance Metrics

| Model | ROC-AUC | F1-Score | Precision | Recall | Status |
|-------|---------|----------|-----------|--------|--------|
| **Baseline RF** | 0.7861 | 0.5376 | **0.6691** | 0.4493 | Legacy |
| **Enhanced RF** | 0.7812 | 0.5514 | 0.6258 | 0.4928 | Available |
| **Enhanced XGBoost** | **0.8035** | 0.5957 | 0.6627 | 0.5411 | ⭐ Recommended |
| **Enhanced LR** | 0.7661 | 0.6034 | 0.5447 | **0.6763** | Available |
| **Ensemble (3)** | **0.8054** | **0.6108** | 0.6231 | 0.5990 | Available |

### Key Changes from Baseline
- **Removed geographic features** (LA County, HSA 11) for fairness
- **Added hyperparameter tuning** for all models
- **Implemented class weights** to handle imbalance
- **Created 3-model ensemble** with weighted voting

---

## Decision Framework

### 1. Enhanced XGBoost ⭐ **RECOMMENDED**

**Best For**: Production deployment, general use

**Strengths**:
- ✅ **Highest single-model ROC-AUC** (0.8035)
- ✅ **Balanced performance** - good precision (66.27%) and recall (54.11%)
- ✅ **Robust gradient boosting** algorithm
- ✅ **Strong feature interactions** captured
- ✅ **Well-calibrated** predictions
- ✅ **Fast inference** time

**Weaknesses**:
- ⚠️ **Less interpretable** than Logistic Regression
- ⚠️ **Requires libomp** library (installed)
- ⚠️ **Cannot explain** using traditional coefficients

**Use When**:
- You need the best overall discrimination (ROC-AUC)
- Balanced precision/recall is important
- You can accept gradient boosting complexity
- Performance > interpretability

**Recommended Threshold**: 0.5 (default) or 0.45 for higher recall

---

### 2. Ensemble (3 Models) 🎯 **ALTERNATIVE BEST**

**Best For**: Maximum performance, mission-critical decisions

**Strengths**:
- ✅ **Highest ROC-AUC overall** (0.8054)
- ✅ **Best F1-Score** (0.6108) - optimal precision/recall balance
- ✅ **Confidence scoring** - knows when models disagree
- ✅ **Robust** - combines RF, XGBoost, LR strengths
- ✅ **Highest recall** among top performers (59.90%)
- ✅ **Model agreement metrics** for transparency

**Weaknesses**:
- ⚠️ **3x storage** (~15MB vs 5MB)
- ⚠️ **3x inference time** (still fast: <5010ms vs <50ms)
- ⚠️ **More complex** to maintain
- ⚠️ **Harder to debug** individual predictions

**Use When**:
- Maximum accuracy is critical
- You need confidence scores
- Storage/latency are not constraints
- You want model agreement transparency

**Recommended Threshold**: 0.5 (ensemble already optimized)

---

### 3. Enhanced Logistic Regression 🔍 **FOR HIGH RECALL**

**Best For**: Regulatory compliance, catching all violations

**Strengths**:
- ✅ **Highest recall** (67.63%) - catches most penalized facilities
- ✅ **Most interpretable** - coefficient-based explanations
- ✅ **Fastest training** and inference
- ✅ **Smallest model** size (~2MB)
- ✅ **Regulatory friendly** - explainable coefficients
- ✅ **No dependencies** beyond scikit-learn

**Weaknesses**:
- ⚠️ **Lowest ROC-AUC** (0.7661)
- ⚠️ **Lowest precision** (54.47%) - more false positives
- ⚠️ **Linear assumptions** - misses complex interactions
- ⚠️ **Lower F1** (0.6034)

**Use When**:
- **Recall is paramount** - must catch violations
- Interpretability is required (regulatory)
- False positives are acceptable
- Simple deployment needed
- Coefficient explanations valuable

**Recommended Threshold**: 0.4 for even higher recall (>70%)

---

### 4. Enhanced Random Forest

**Best For**: Balancing precision and interpretability

**Strengths**:
- ✅ **Feature importances** easy to extract
- ✅ **Handles non-linearity** well
- ✅ **Robust to outliers**
- ✅ **No scaling required**

**Weaknesses**:
- ⚠️ **Lower ROC-AUC** (0.7812) than XGBoost/Ensemble
- ⚠️ **Larger model size** (~8MB)
- ⚠️ **Slower than** Logistic Regression

**Use When**:
- You need tree-based interpretability
- XGBoost isn't available
- Moderate performance is acceptable

---

## Use Case Recommendations

### Scenario 1: Proactive Facility Monitoring (Production)
**Recommendation**: **Enhanced XGBoost**
- Need: Balance of precision/recall
- Goal: Identify at-risk facilities for early intervention
- Tolerance: ~45% false negatives acceptable if precision is good

### Scenario 2: Regulatory Enforcement Prioritization
**Recommendation**: **Enhanced Logistic Regression**
- Need: High recall to catch violations
- Goal: Ensure no penalized facilities are missed
- Tolerance: False positives okay (can manually review)
- Benefit: Easy to explain to regulators

### Scenario 3: Mission-Critical Decisions
**Recommendation**: **Ensemble**
- Need: Absolute best accuracy
- Goal: High-stakes facility certifications
- Tolerance: Can afford extra computation
- Benefit: Confidence scoring shows model certainty

### Scenario 4: Research/Analysis
**Recommendation**: **Enhanced Random Forest**
- Need: Understand feature relationships
- Goal: Policy research, feature importance studies
- Benefit: SHAP values work well with RF

---

## Performance Trade-Offs

### High Recall (Catch More Violations)
- **Choice**: Enhanced LR (67.63% recall)
- **Cost**: Lower precision (54.47%) → more false alarms
- **Benefit**: Fewer missed violations

### Balanced Performance
- **Choice**: Enhanced XGBoost or Ensemble
- **Cost**: Moderate recall (~54-60%)
- **Benefit**: Better precision (~62-66%), higher ROC-AUC

### High Precision (Fewer False Alarms)
- **Choice**: Baseline RF (66.91% precision)
- **Cost**: Lower recall (44.93%) → miss more violations
- **Note**: Not recommended due to geographic bias

---

## Implementation Considerations

### Storage Requirements
- Logistic Regression: **~2MB**
- Random Forest: **~8MB**
- XGBoost: **~5MB**
- Ensemble (all 3): **~15MB**

### Inference Latency (avg per prediction)
- Logistic Regression: **<10ms**
- Random Forest: **<50ms**
- XGBoost: **<30ms**
- Ensemble: **<100ms** (parallel prediction possible)

### Dependencies
- **All models**: scikit-learn, numpy, pandas
- **XGBoost**: xgboost, libomp (installed)
- **Ensemble**: All of the above

### Maintenance Complexity
1. Logistic Regression: ⭐ (simplest)
2. Random Forest: ⭐⭐
3. XGBoost: ⭐⭐⭐
4. Ensemble: ⭐⭐⭐⭐ (most complex)

---

## Threshold Tuning

### Current Default: 0.5
All models use 0.5 probability threshold for classification.

### Recommended Adjustments

**For Higher Recall** (catch more violations):
- Enhanced LR: Lower to **0.40** → Recall ~75%, Precision ~50%
- Enhanced XGBoost: Lower to **0.45** → Recall ~62%, Precision ~60%
- Ensemble: Lower to **0.45** → Recall ~65%, Precision ~58%

**For Higher Precision** (fewer false alarms):
- Enhanced XGBoost: Raise to **0.55** → Recall ~48%, Precision ~72%
- Ensemble: Raise to **0.55** → Recall ~54%, Precision ~68%

---

## Final Recommendation

### Primary Model for Production
**Enhanced XGBoost** (ROC-AUC: 0.8035)

**Rationale**:
1. Best single-model performance
2. Balanced precision (66.27%) and recall (54.11%)
3. No geographic bias
4. Well-calibrated predictions
5. Reasonable computational cost
6. All dependencies installed

### Backup/Alternative
**Enhanced Logistic Regression** for high-recall scenarios

**Enable Ensemble**: If maximum accuracy needed and computational resources available

---

## Migration Path

### From Current (Baseline RF with LA features)
1. ✅ **Immediate**: Switch to Enhanced XGBoost (ready to deploy)
2. ⚠️ **Expect**: Slight ROC-AUC decrease (0.8088 → 0.8035) but fairer predictions
3. ✅ **Benefit**: All features now actionable, no geographic discrimination
4. 📊 **Monitor**: Track recall improvement (44.93% → 54.11%)

### Testing Before Full Deployment
1. A/B test Enhanced XGBoost vs current for 2 weeks
2. Compare precision/recall on new facilities
3. Gather user feedback on recommendations
4. Validate fairness across all regions
5. Full rollout if metrics acceptable

---

## Model Files Location

All retrained models (without geographic features) available at:
```
models/
├── risk_model.pkl              # Baseline RF (no LA)
├── random_forest_model.pkl     # Enhanced RF
├── xgboost_model.pkl          # ⭐ Enhanced XGBoost (RECOMMENDED)
├── logistic_regression_model.pkl
├── risk_model_enhanced.pkl    # Symlink to XGBoost
└── ensemble_metadata.json     # Ensemble weights
```

---

**Last Updated**: 2025-11-24  
**Models Trained**: Without LA County/HSA 11 geographic features  
**All Features**: Actionable, operational factors only