import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt

try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except Exception as e:
    XGB_AVAILABLE = False
    print(f"XGBoost not available ({e}), skipping.")

def train_models(input_file, model_dir, report_file):
    try:
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file, low_memory=False)
        
        # 1. Target Variable Creation
        target_col = 'Penalized'
        if 'Penalized?' in df.columns:
            df.rename(columns={'Penalized?': target_col}, inplace=True)
        
        # Ensure target is binary (True/False -> 1/0)
        df[target_col] = df[target_col].astype(int)
        
        print(f"Target distribution:\n{df[target_col].value_counts(normalize=True)}")
        
        # 2. Feature Selection & Engineering
        # Drop identifiers and non-predictive columns
        drop_cols = [
            'FAC_NO', 'FAC_NAME_x', 'FAC_NAME_y', 'FAC_NAME', 'LICENSE_NO_x', 'LICENSE_NO_y', 
            'HCAI_ID', 'FACID', 'FACNAME', 'LICENSE_NUMBER', 'ADMINIS', 
            'FAC_PAR_CORP_NAME', 'FAC_PAR_CORP_CITY', 'FAC_PAR_CORP_STATE', 'FAC_PAR_CORP_ZIP',
            'SUBMITTED_DT', 'LICENSE_EFF_DATE', 'LICENSE_EXP_DATE', 'FAC_OP_PER_BEGIN_DT', 
            'FAC_OP_PER_END_DT', 'BEG_DATE', 'END_DATE', 'CENSUS_KEY', 'ASSEMBLY_DIST', 
            'SENATE_DIST', 'CONGRESS_DIST', 'MED_SVC_STUDY_AREA', 'HEALTH_SVC_AREA',
            'CITY', 'ZIP_CODE', 'FAC_CITY', 'FAC_ZIP', 'ADDRESS', 'STREET',
            'Total Amount Due Final', 'Total Records Found'
        ]
        
        # Drop columns that are present in drop_cols and exist in df
        cols_to_drop = [c for c in drop_cols if c in df.columns]
        df_model = df.drop(columns=cols_to_drop)
        
        # Create Ratios (Example)
        # Net Income Margin
        df_model['Net_Income_Margin'] = df_model['NET_INCOME'] / df_model['TOT_HC_REV'].replace(0, np.nan)
        
        # Staffing Ratios (Hours per Patient Day)
        # Assuming DAY_TOTL is total patient days
        staffing_cols = ['PRDHR_RN', 'PRDHR_LVN', 'PRDHR_NA']
        for col in staffing_cols:
            if col in df_model.columns and 'DAY_TOTL' in df_model.columns:
                df_model[f'{col}_Per_Day'] = df_model[col] / df_model['DAY_TOTL'].replace(0, np.nan)
        
        # 3. Define X and y
        X = df_model.drop(columns=[target_col])
        y = df_model[target_col]
        
        # Identify numeric and categorical columns
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()
        
        # Exclude geographic features for fairness
        geographic_cols_to_exclude = ['COUNTY_x', 'COUNTY_y', 'HSA']
        categorical_features = [f for f in categorical_features if f not in geographic_cols_to_exclude]
        
        print(f"Numeric features: {len(numeric_features)}")
        print(f"Categorical features: {len(categorical_features)} (excluded geographic)")
        print(f"Excluded: {geographic_cols_to_exclude}")
        
        # 4. Preprocessing Pipeline
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        # 5. Split Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # 6. Model Training & Evaluation
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        if XGB_AVAILABLE:
            models['XGBoost'] = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
            
        best_model = None
        best_score = 0
        best_name = ""
        
        results = []
        
        print("\nTraining models...")
        for name, model in models.items():
            # Create full pipeline
            clf = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('classifier', model)])
            
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            y_proba = clf.predict_proba(X_test)[:, 1]
            
            roc_auc = roc_auc_score(y_test, y_proba)
            f1 = f1_score(y_test, y_pred)
            
            print(f"{name}: ROC-AUC = {roc_auc:.4f}, F1 = {f1:.4f}")
            
            results.append({
                'Model': name,
                'ROC-AUC': roc_auc,
                'F1-Score': f1,
                'Precision': precision_score(y_test, y_pred),
                'Recall': recall_score(y_test, y_pred)
            })
            
            if roc_auc > best_score:
                best_score = roc_auc
                best_model = clf
                best_name = name
        
        # 7. Save Best Model
        print(f"\nBest Model: {best_name} with ROC-AUC: {best_score:.4f}")
        model_path = os.path.join(model_dir, 'risk_model.pkl')
        joblib.dump(best_model, model_path)
        print(f"Model saved to {model_path}")
        
        # 8. Generate Report
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w') as f:
            f.write("# Model Performance Report\n\n")
            f.write(f"## Best Model: {best_name}\n")
            f.write(f"**ROC-AUC**: {best_score:.4f}\n\n")
            
            f.write("## Comparison\n")
            results_df = pd.DataFrame(results)
            f.write(results_df.to_string(index=False))
            f.write("\n\n")
            
            # Feature Importance (if applicable)
            if best_name in ['Random Forest', 'XGBoost']:
                f.write("## Top 10 Feature Importances\n")
                
                # Extract feature names
                # This is a bit tricky with pipelines and onehotencoder, doing best effort
                try:
                    feature_names = numeric_features.tolist()
                    if hasattr(best_model.named_steps['preprocessor'].transformers_[1][1]['encoder'], 'get_feature_names_out'):
                         cat_names = best_model.named_steps['preprocessor'].transformers_[1][1]['encoder'].get_feature_names_out(categorical_features)
                         feature_names.extend(cat_names)
                    
                    importances = best_model.named_steps['classifier'].feature_importances_
                    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(10)
                    f.write(feat_imp.to_string())
                except Exception as e:
                    f.write(f"Could not extract feature importances: {e}")
                    
        print(f"Report saved to {report_file}")

    except Exception as e:
        print(f"Error training models: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    input_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/data/processed/longterm_care_cleaned.csv'
    model_dir = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/models'
    report_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/docs/model_performance.md'
    train_models(input_path, model_dir, report_path)
