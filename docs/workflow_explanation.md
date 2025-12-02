# Workflow Explanation

This document logs the steps taken to process and analyze the long-term care facility data.

## 1. Data Preparation
*   **Source Files**: `longterm_care_v2_2022.xlsx` and `longterm_care_v2_2024.xlsx`.
*   **Conversion**: Converted both Excel files to CSV format.
*   **Labeling**: Added a `year` column to each dataset to distinguish the source year (2022 and 2024).
*   **Merging**: Merged the two CSV files into a single dataset named `longterm_care_22_24.csv`.

## 2. Data Understanding
*   **Column Identification**: The column headers in the merged CSV were abbreviated and difficult to interpret.
*   **Research**: Performed online research to identify the data source as the California Department of Health Care Access and Information (HCAI).
*   **Data Dictionary**: Created `column_dictionary.md` to map the abbreviated column names (e.g., `FAC_NO`, `GR_RT_TOTL`) to their full definitions based on HCAI documentation.

## 3. Data Analysis
*   **Missing Data Analysis**: Analyzed `longterm_care_22_24.csv` to identify columns with significant missing data.
*   **Threshold**: Identified columns where more than 50% of the values are missing.
*   **Reporting**: Generated a list of these columns to inform data cleaning and feature selection decisions.

## 4. Data Cleaning
*   **Objective**: Create a cleaner dataset for analysis.
*   **Action**: Removed all columns identified as having more than 50% missing data.
*   **Result**: Created `longterm_care_cleaned.csv`.
    *   **Initial Columns**: 606
    *   **Columns Dropped**: 358
    *   **Remaining Columns**: 248

## 5. Project Organization
*   **Objective**: Organize the project directory for better maintainability.
*   **Action**: Created subfolders and moved files.
    *   `data/raw`: Original CSV files (`longterm_care_v2_2022.csv`, `longterm_care_v2_2024.csv`).
    *   `data/processed`: Processed data files (`longterm_care_22_24.csv`, `longterm_care_cleaned.csv`).
    *   `scripts`: Python scripts (`analyze_missing_data.py`, `clean_data.py`, `list_cleaned_columns.py`, `merge_data.py`).
    *   `docs`: Documentation files (`cleaned_data_dictionary.md`, `column_dictionary.md`, `workflow_explanation.md`).
    *   `output`: Analysis output (`missing_data_columns.md`).

## 6. Model Development (Risk Simulator)
*   **Objective**: Build a predictive model to estimate the likelihood of enforcement actions (`Penalized`).
*   **Phase 1: Feature Engineering**:
    *   Target Variable: `Penalized` (Binary).
    *   Dropped identifiers and non-predictive columns (e.g., `FAC_NO`, `ADDRESS`).
    *   Created derived features: `Net_Income_Margin`, `Staffing_Hours_Per_Patient_Day`.
    *   Handled missing values (Mean for numeric, Mode for categorical).
    *   One-Hot Encoded categorical variables.
*   **Phase 2: Model Training**:
    *   Trained **Logistic Regression** and **Random Forest** models.
    *   **Best Model**: Random Forest Classifier.
    *   **Performance**: ROC-AUC **0.8088**.
    *   **Key Findings**: Location (HSA 11 - Los Angeles) is a top risk predictor.
*   **Artifacts**:
    *   `models/risk_model.pkl`: Serialized model pipeline.
    *   `docs/model_performance.md`: Detailed performance report.

## 7. Model Enhancements (Multi-Model Ensemble)
*   **Objective**: Address model limitations and improve recall for detecting penalized facilities.
*   **Phase 1: Hyperparameter Optimization**:
    *   Implemented **RandomizedSearchCV** with 30 iterations, 3-fold CV.
    *   Optimized Random Forest: 300 trees, max_depth=20, balanced class weights.
    *   Optimized Logistic Regression: C=0.01, L2 penalty, balanced weights.
*   **Phase 2: Class Balancing**:
    *   Applied **class weights** to handle imbalanced data (36% positive class).
    *   Improved model sensitivity to minority class (penalized facilities).
*   **Phase 3: Multi-Model Ensemble**:
    *   Combined Random Forest and Logistic Regression with performance-based weighting.
    *   Implemented **confidence scoring** based on model agreement.
    *   Integrated **SHAP** values for accurate feature attribution.
*   **Performance Improvements**:
    *   **Baseline Recall**: 46.4% → **Enhanced Recall**: 69.1% (+48.96% improvement).
    *   **Ensemble ROC-AUC**: 0.8151 (+0.78% over baseline).
    *   **Trade-off**: Precision decreased to 60-66% (acceptable for regulatory context).
*   **Artifacts**:
    *   `models/random_forest_model.pkl`: Tuned Random Forest.
    *   `models/logistic_regression_model.pkl`: Tuned Logistic Regression.
    *   `models/ensemble_metadata.json`: Ensemble weights and configuration.
    *   `models/shap_explainer.pkl`: SHAP interpretability.
    *   `docs/enhanced_model_performance.md`: Enhanced performance report.
    *   `docs/model_comparison.md`: Baseline vs enhanced comparison.

## 8. Hospital Data Processing
*   **Objective**: Prepare hospital data for potential future analysis or integration.
*   **Source Files**: `hospital_v2_2022.xlsx` and `hospital_v2_2024.xlsx`.
*   **Process**:
    *   **Conversion**: Converted Excel files to CSV.
    *   **Labeling**: Added `year` column (2022 and 2024).
    *   **Merging**: Merged into `data/processed/hospital_22_24.csv` (1025 rows).
*   **Cleaning**:
    *   **Threshold**: Removed columns with >50% missing data.
    *   **Result**: Created `data/processed/hospital_cleaned.csv`.
        *   **Initial Columns**: 600
        *   **Columns Dropped**: 217
        *   **Remaining Columns**: 383
