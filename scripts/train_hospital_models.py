import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, recall_score, precision_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import xgboost as xgb
import os
import sys

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hospital_feature_names import convert_feature_name

def train_models():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'processed', 'hospital_cleaned.csv')
    output_report = os.path.join(base_dir, 'docs-hospitals', 'hospital_model_comparison.md')

    print("Loading data...")
    df = pd.read_csv(input_file, low_memory=False)

    # 1. Define Target
    target_col = 'Penalized?'
    if target_col not in df.columns:
        print(f"Error: Target {target_col} not found.")
        return

    # 2. Preprocessing - Exclude penalty-related features
    print("Preprocessing...")
    drop_cols = ['FACID', 'FAC_NAME', 'LICENSE_NUMBER', 'ADDRESS', 'CITY', 'ZIP_CODE', 'year', 'FAC_NO', 'HCAI_ID']
    drop_cols += [c for c in df.columns if 'LICENSE' in c or 'NAME' in c or 'DATE' in c]
    
    # CRITICAL: Exclude penalty-related features
    penalty_related = ['Total Amount Due Final', 'Total Records Found']
    drop_cols += penalty_related
    
    print(f"Excluding penalty-related features: {penalty_related}")
    
    X = df.drop(columns=[target_col] + [c for c in drop_cols if c in df.columns])
    y = df[target_col]

    # Handle categorical and numeric features
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    print(f"Features: {len(X.columns)} ({len(numeric_features)} numeric, {len(categorical_features)} categorical)")

    # Create preprocessor
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 3. Model Training & Evaluation
    results = {}
    
    # Random Forest
    print("Training Random Forest...")
    rf = Pipeline(steps=[('preprocessor', preprocessor),
                         ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))])
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]
    results['Random Forest'] = {
        'Accuracy': accuracy_score(y_test, y_pred_rf),
        'ROC-AUC': roc_auc_score(y_test, y_prob_rf),
        'Recall': recall_score(y_test, y_pred_rf),
        'Precision': precision_score(y_test, y_pred_rf)
    }

    # Logistic Regression
    print("Training Logistic Regression...")
    lr = Pipeline(steps=[('preprocessor', preprocessor),
                         ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced'))])
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    y_prob_lr = lr.predict_proba(X_test)[:, 1]
    results['Logistic Regression'] = {
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'ROC-AUC': roc_auc_score(y_test, y_prob_lr),
        'Recall': recall_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr)
    }

    # LightGBM
    print("Training LightGBM...")
    lgbm = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', lgb.LGBMClassifier(n_estimators=100, random_state=42, class_weight='balanced', verbose=-1))])
    lgbm.fit(X_train, y_train)
    y_pred_lgbm = lgbm.predict(X_test)
    y_prob_lgbm = lgbm.predict_proba(X_test)[:, 1]
    results['LightGBM'] = {
        'Accuracy': accuracy_score(y_test, y_pred_lgbm),
        'ROC-AUC': roc_auc_score(y_test, y_prob_lgbm),
        'Recall': recall_score(y_test, y_pred_lgbm),
        'Precision': precision_score(y_test, y_pred_lgbm)
    }

    # XGBoost
    print("Training XGBoost...")
    xgbm = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', xgb.XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='logloss'))])
    xgbm.fit(X_train, y_train)
    y_pred_xgbm = xgbm.predict(X_test)
    y_prob_xgbm = xgbm.predict_proba(X_test)[:, 1]
    results['XGBoost'] = {
        'Accuracy': accuracy_score(y_test, y_pred_xgbm),
        'ROC-AUC': roc_auc_score(y_test, y_prob_xgbm),
        'Recall': recall_score(y_test, y_pred_xgbm),
        'Precision': precision_score(y_test, y_pred_xgbm)
    }

    # 4. Feature Importance (RF)
    print("Extracting Feature Importance...")
    feature_names = []
    if hasattr(rf.named_steps['preprocessor'], 'get_feature_names_out'):
         feature_names = rf.named_steps['preprocessor'].get_feature_names_out()
    else:
        feature_names = numeric_features.tolist() + list(rf.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot'].get_feature_names_out(categorical_features))

    importances = rf.named_steps['classifier'].feature_importances_
    feature_imp = pd.DataFrame({'feature': feature_names, 'importance': importances})
    top_features = feature_imp.sort_values('importance', ascending=False).head(20)
    
    # Convert to full names
    top_features['full_name'] = top_features['feature'].apply(convert_feature_name)

    # 5. Generate Report
    print(f"Generating report at {output_report}...")
    with open(output_report, 'w') as f:
        f.write("# Hospital Model Comparison\n\n")
        f.write("**Note**: Penalty-related features (`Total Amount Due Final`, `Total Records Found`) have been excluded from the model to prevent data leakage.\n\n")
        
        f.write("## Model Performance\n")
        f.write("| Model | Accuracy | ROC-AUC | Recall | Precision |\n")
        f.write("|---|---|---|---|---|\n")
        for model, metrics in results.items():
            f.write(f"| {model} | {metrics['Accuracy']:.4f} | {metrics['ROC-AUC']:.4f} | {metrics['Recall']:.4f} | {metrics['Precision']:.4f} |\n")
        
        f.write("\n## Top 20 Features (Random Forest)\n")
        f.write("| Feature | Full Name | Importance |\n")
        f.write("|---|---|---|\n")
        for _, row in top_features.iterrows():
            f.write(f"| `{row['feature']}` | {row['full_name']} | {row['importance']:.4f} |\n")

    print("Done.")

if __name__ == "__main__":
    train_models()
