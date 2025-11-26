# Random Forest Model Documentation

## Overview

The **CareEnforced AI** system uses a Random Forest classifier to predict the risk of California long-term care facilities being penalized by regulatory authorities. This document provides comprehensive details about the model architecture, training process, features, and performance metrics.

## Model Type

**Random Forest Classifier** (ensemble learning method)

- **Library**: scikit-learn (`sklearn.ensemble.RandomForestClassifier`)
- **Version**: Implemented as part of an ML pipeline
- **Model File**: `risk_model.pkl` (5.76 MB)

## Training Configuration

### Hyperparameters

```python
RandomForestClassifier(
    n_estimators=100,      # Number of trees in the forest
    random_state=42,       # For reproducibility
    # Other parameters use scikit-learn defaults
)
```

### Key Parameters

- **n_estimators**: 100 decision trees
- **random_state**: 42 (ensures reproducible results)
- **criterion**: Gini impurity (default)
- **max_features**: sqrt(n_features) (default for classification)
- **bootstrap**: True (default - bootstrap samples for building trees)

## Data Pipeline

### 1. Preprocessing Architecture

The model uses a scikit-learn `Pipeline` with a `ColumnTransformer` for preprocessing:

#### Numeric Features Pipeline
```python
Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])
```

- **Imputation**: Missing values filled with column mean
- **Scaling**: Standardized to zero mean and unit variance

#### Categorical Features Pipeline
```python
Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])
```

- **Imputation**: Missing values filled with most frequent category
- **Encoding**: One-hot encoding for categorical variables
- **Unknown handling**: Ignores unseen categories during prediction

### 2. Train-Test Split

```python
train_test_split(X, y, 
    test_size=0.2,        # 80/20 split
    random_state=42,      # Reproducibility
    stratify=y            # Maintains class distribution
)
```

## Features

### Feature Engineering

The model includes several engineered features:

1. **Net Income Margin**
   ```python
   Net_Income_Margin = NET_INCOME / TOT_HC_REV
   ```

2. **Staffing Ratios** (Hours per Patient Day)
   ```python
   PRDHR_RN_Per_Day = PRDHR_RN / DAY_TOTL
   PRDHR_LVN_Per_Day = PRDHR_LVN / DAY_TOTL
   PRDHR_NA_Per_Day = PRDHR_NA / DAY_TOTL
   ```

### Excluded Features

The following identifier and administrative columns are excluded from training:

- Facility identifiers: `FAC_NO`, `FAC_NAME`, `LICENSE_NO`, `HCAI_ID`, etc.
- Administrative details: `FAC_PAR_CORP_NAME`, `FAC_PAR_CORP_CITY`, etc.
- Temporal data: `SUBMITTED_DT`, `LICENSE_EFF_DATE`, `BEG_DATE`, etc.
- Geographic identifiers: `CITY`, `ZIP_CODE`, `ADDRESS`, etc.
- Jurisdictional data: `ASSEMBLY_DIST`, `SENATE_DIST`, `CONGRESS_DIST`, etc.
- Penalty details: `Total Amount Due Final`, `Total Records Found`

### Top 10 Most Important Features

Based on Gini importance from the trained Random Forest:

| Rank | Feature Name | Importance | Description |
|------|--------------|------------|-------------|
| 1 | `HSA_11 - Los Angeles` | 0.0132 | Health Service Area 11 (Los Angeles) |
| 2 | `TOT_PAT_DAYS_FOR` | 0.0107 | Total Patient Days (Foreign) |
| 3 | `HFPA` | 0.0105 | Healthcare Facility Patient-Day Assessment |
| 4 | `DISCHARGES_7_MONTHS_AND_LT_1_YR` | 0.0101 | Discharges between 7 months and 1 year |
| 5 | `DISCHARGES_3_MONTHS_AND_LT_7_MONTHS` | 0.0093 | Discharges between 3-7 months |
| 6 | `COUNTY_x_Los Angeles` | 0.0091 | Los Angeles County indicator |
| 7 | `EXP_ADMN` | 0.0091 | Administrative Expenses |
| 8 | `SN_PAT_DAYS_FOR` | 0.0086 | Skilled Nursing Patient Days (Foreign) |
| 9 | `PPE_BED` | 0.0081 | Property, Plant & Equipment per Bed |
| 10 | `TOT_LIC_BEDS` | 0.0078 | Total Licensed Beds |

> **Note**: The importance values are relatively distributed across many features, indicating that the model considers multiple factors in making predictions rather than relying heavily on just a few features.

## Target Variable

- **Name**: `Penalized`
- **Type**: Binary classification
- **Values**: 
  - `1` = Facility was penalized
  - `0` = Facility was not penalized
- **Original column**: `Penalized?` (boolean) converted to integer

## Model Performance

### Best Model Selection

The Random Forest was selected as the best model after comparing multiple algorithms:

| Model | ROC-AUC | F1-Score | Precision | Recall |
|-------|---------|----------|-----------|--------|
| **Random Forest** | **0.8088** | **0.5647** | **0.7218** | **0.4638** |
| Logistic Regression | 0.7978 | 0.6150 | 0.6611 | 0.5749 |

### Performance Metrics

- **ROC-AUC**: 0.8088
  - Indicates good discrimination ability between penalized and non-penalized facilities
  - 80.88% probability that the model ranks a randomly chosen penalized facility higher than a non-penalized one

- **F1-Score**: 0.5647
  - Harmonic mean of precision and recall
  - Balanced measure of model performance

- **Precision**: 0.7218
  - 72.18% of facilities predicted as "penalized" were actually penalized
  - High precision reduces false alarms for facility operators

- **Recall**: 0.4638
  - Model identifies 46.38% of all actually penalized facilities
  - Conservative approach that prioritizes accuracy over catching all violations

### Model Trade-offs

The Random Forest achieves:
- ✅ **Higher precision** (72.2% vs 66.1%) - fewer false positives
- ✅ **Better ROC-AUC** (0.809 vs 0.798) - better overall discrimination
- ⚠️ **Lower recall** (46.4% vs 57.5%) - misses more actual penalties
- ⚠️ **Lower F1** (0.565 vs 0.615) - lower balanced performance

The model prioritizes **precision over recall**, making it suitable for risk assessment where false alarms should be minimized.

## Prediction Output

### Risk Score Calculation

```python
risk_score = model.predict_proba(X)[0][1]  # Probability of class 1 (Penalized)
```

The model outputs a probability between 0 and 1, representing the likelihood of penalty.

### Risk Level Classification

| Risk Score Range | Risk Level |
|------------------|------------|
| 0.00 - 0.30 | Low |
| 0.30 - 0.70 | Medium |
| 0.70 - 1.00 | High |

### Feature Contribution Analysis

The model calculates feature contributions using:

```python
contribution_score = abs(transformed_value) * feature_importance * 100
```

This approach combines:
1. The transformed feature value (after preprocessing)
2. The feature's importance in the random forest
3. Scaling factor for interpretability

### Dynamic Recommendations

The system generates context-aware recommendations based on:
- **Top risk drivers**: Features contributing most to the risk score
- **Input values**: Actual facility characteristics
- **Threshold logic**: Comparing inputs to recommended benchmarks

#### Example Recommendation Rules

1. **Staffing-related** (RN hours < 1.0 or CNA hours < 3.0)
   - Increase staffing ratios to meet or exceed standards
   
2. **Financial-related** (Negative Net Income Margin)
   - Review cost structure and revenue optimization
   
3. **Geographic-related** (Los Angeles region)
   - Enhanced compliance protocols for high-scrutiny areas
   
4. **Capacity-related** (Patient days, licensed beds)
   - Optimize utilization and resource allocation

## Model Storage and Loading

### File Location
```
/models/risk_model.pkl
```

### Loading Method
```python
import joblib
model = joblib.load('models/risk_model.pkl')
```

### Model Components

The saved pipeline includes:
1. **Preprocessor**: ColumnTransformer with numeric and categorical pipelines
2. **Classifier**: Trained RandomForestClassifier with 100 trees
3. **Feature metadata**: Expected numeric and categorical feature names

## Integration Architecture

### Backend Implementation

**File**: `backend/model.py`

**Class**: `RiskModel`

**Key methods**:
- `load_model()`: Loads the trained pipeline
- `load_top_features()`: Loads feature importance metadata
- `predict(input_data)`: Generates risk assessment with explanations
- `_calculate_feature_contributions()`: Computes feature-level contributions
- `_generate_recommendations()`: Creates actionable recommendations

### API Endpoint

**File**: `backend/main.py`

**Endpoint**: `POST /predict`

**Request format**:
```json
{
  "facility_data": {
    "TOT_LIC_BEDS": 120,
    "PRDHR_RN_Per_Day": 0.8,
    "PRDHR_NA_Per_Day": 2.5,
    "Net_Income_Margin": -0.05,
    ...
  }
}
```

**Response format**:
```json
{
  "risk_score": 0.65,
  "risk_level": "Medium",
  "top_risk_drivers": [
    {
      "feature": "RN Hours per Patient Day",
      "contribution": 12.5,
      "importance": 0.0132
    }
  ],
  "recommendations": [
    {
      "title": "Increase RN Staffing",
      "description": "Current RN hours (0.80/patient-day) are below recommended levels. Increasing to 1.5+ hours/patient-day could reduce risk by ~15%.",
      "impact": "high"
    }
  ]
}
```

## Training Scripts

### Main Training Script

**File**: `scripts/train_model.py`

**Functionality**:
- Data loading and preprocessing
- Feature engineering
- Model training with cross-validation
- Performance evaluation
- Model serialization
- Report generation

**Execution**:
```bash
python scripts/train_model.py
```

### Feature Extraction

**File**: `scripts/extract_top_features.py`

**Purpose**: Extract and save top-N feature importances from trained model

**Output**: `backend/top_features.json`

**Execution**:
```bash
python scripts/extract_top_features.py
```

## Model Validation

### Model Inspection

**File**: `scripts/inspect_model.py`

**Purpose**: Verify model structure and feature specifications

**Outputs**:
- List of numeric features
- List of categorical features
- OneHotEncoder categories per feature

### Prediction Verification

**File**: `scripts/verify_dynamic_prediction.py`

**Purpose**: Test that predictions change with different inputs

## Data Sources

The model is trained on combined California long-term care facility data:

1. **Financial data**: Revenue, expenses, margins
2. **Operational data**: Bed counts, patient days, discharge patterns
3. **Staffing data**: RN, LVN, CNA hours
4. **Geographic data**: County, Health Service Area (HSA)
5. **Regulatory data**: Historical penalty records

**Data file**: `data/processed/longterm_care_cleaned.csv`

## Limitations and Considerations

### 1. Class Imbalance
- The target variable may be imbalanced (penalties are relatively rare events)
- Stratified splitting helps maintain class distribution
- Precision-focused metrics are more relevant than accuracy

### 2. Feature Importance Distribution
- Importance is spread across many features (top feature: 1.32%)
- No single dominant predictor
- Model captures complex interactions between multiple factors

### 3. Temporal Considerations
- Model trained on historical data (2022, 2024)
- May need retraining to capture regulatory changes
- Temporal drift should be monitored

### 4. Geographic Bias
- Los Angeles region prominently featured in top features
- May reflect actual regulatory patterns or data imbalance
- Regional variations should be considered in interpretation

### 5. Interpretability
- Random Forest provides feature importance but not direct coefficients
- Contribution calculation is simplified (linear approximation)
- For regulatory decisions, consider multiple model perspectives

## Future Improvements

1. **Hyperparameter Tuning**: Grid search or random search for optimal parameters
2. **Feature Selection**: Systematic removal of low-importance features
3. **Class Balancing**: SMOTE or class weights to handle imbalanced data
4. **Ensemble Methods**: Combine with other models (XGBoost, LightGBM)
5. **Temporal Validation**: Time-based train/test split for better generalization
6. **SHAP Values**: Use SHAP for more accurate feature contribution analysis
7. **Model Monitoring**: Track performance drift over time

## References

- **scikit-learn Documentation**: [Random Forest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- **Model Performance Report**: [model_performance.md](file:///Users/macintoshhd/Desktop/95891%20-%20Intro%20to%20AI/Final%20Project/FinalProject/docs/model_performance.md)
- **Training Script**: [train_model.py](file:///Users/macintoshhd/Desktop/95891%20-%20Intro%20to%20AI/Final%20Project/FinalProject/scripts/train_model.py)
- **Model Implementation**: [model.py](file:///Users/macintoshhd/Desktop/95891%20-%20Intro%20to%20AI/Final%20Project/FinalProject/backend/model.py)

---

**Last Updated**: 2025-11-24  
**Model Version**: 1.0  
**Contact**: CareEnforced AI Team
