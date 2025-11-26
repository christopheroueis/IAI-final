"""
Compare baseline model vs enhanced ensemble models.
"""

import joblib
import pandas as pd
import numpy as np
import os
import json
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score


def load_test_data():
    """Load and prepare test data."""
    data_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/data/processed/longterm_care_cleaned.csv'
    df = pd.read_csv(data_path, low_memory=False)
    
    # Create target
    target_col = 'Penalized'
    if 'Penalized?' in df.columns:
        df.rename(columns={'Penalized?': target_col}, inplace=True)
    df[target_col] = df[target_col].astype(int)
    
    # Drop same columns as training
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
    cols_to_drop = [c for c in drop_cols if c in df.columns]
    df_model = df.drop(columns=cols_to_drop)
    
    # Feature engineering
    df_model['Net_Income_Margin'] = df_model['NET_INCOME'] / df_model['TOT_HC_REV'].replace(0, np.nan)
    
    staffing_cols = ['PRDHR_RN', 'PRDHR_LVN', 'PRDHR_NA']
    for col in staffing_cols:
        if col in df_model.columns and 'DAY_TOTL' in df_model.columns:
            df_model[f'{col}_Per_Day'] = df_model[col] / df_model['DAY_TOTL'].replace(0, np.nan)
    
    X = df_model.drop(columns=[target_col])
    y = df_model[target_col]
    
    # Use last 20% as test set (same split as training)
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    return X_test, y_test


def compare_models():
    """Compare baseline vs enhanced models."""
    print("="*80)
    print("Model Performance Comparison")
    print("="*80)
    
    # Load test data
    print("\nLoading test data...")
    X_test, y_test = load_test_data()
    print(f"Test set size: {len(X_test)}")
    print(f"Positive class rate: {y_test.mean():.2%}")
    
    # Load models
    baseline_path = 'models/risk_model.pkl'
    rf_enhanced_path = 'models/random_forest_model.pkl'
    xgb_enhanced_path = 'models/xgboost_model.pkl'
    lr_enhanced_path = 'models/logistic_regression_model.pkl'
    
    results = {}
    
    # Baseline model
    print("\n" + "-"*80)
    print("Evaluating Baseline Random Forest...")
    print("-"*80)
    if os.path.exists(baseline_path):
        baseline = joblib.load(baseline_path)
        y_pred_baseline = baseline.predict(X_test)
        y_prob_baseline = baseline.predict_proba(X_test)[:, 1]
        
        results['Baseline Random Forest'] = {
            'ROC-AUC': roc_auc_score(y_test, y_prob_baseline),
            'F1-Score': f1_score(y_test, y_pred_baseline),
            'Precision': precision_score(y_test, y_pred_baseline),
            'Recall': recall_score(y_test, y_pred_baseline)
        }
        
        for metric, value in results['Baseline Random Forest'].items():
            print(f"  {metric:12s}: {value:.4f}")
    else:
        print("  Baseline model not found")
    
    # Enhanced Random Forest
    print("\n" + "-"*80)
    print("Evaluating Enhanced Random Forest (tuned)...")
    print("-"*80)
    if os.path.exists(rf_enhanced_path):
        rf_enhanced = joblib.load(rf_enhanced_path)
        y_pred_rf = rf_enhanced.predict(X_test)
        y_prob_rf = rf_enhanced.predict_proba(X_test)[:, 1]
        
        results['Enhanced Random Forest'] = {
            'ROC-AUC': roc_auc_score(y_test, y_prob_rf),
            'F1-Score': f1_score(y_test, y_pred_rf),
            'Precision': precision_score(y_test, y_pred_rf),
            'Recall': recall_score(y_test, y_pred_rf)
        }
        
        for metric, value in results['Enhanced Random Forest'].items():
            print(f"  {metric:12s}: {value:.4f}")
    
    # Enhanced Logistic Regression
    print("\n" + "-"*80)
    print("Evaluating Enhanced Logistic Regression (tuned)...")
    print("-"*80)
    if os.path.exists(lr_enhanced_path):
        lr_enhanced = joblib.load(lr_enhanced_path)
        y_pred_lr = lr_enhanced.predict(X_test)
        y_prob_lr = lr_enhanced.predict_proba(X_test)[:, 1]
        
        results['Enhanced Logistic Regression'] = {
            'ROC-AUC': roc_auc_score(y_test, y_prob_lr),
            'F1-Score': f1_score(y_test, y_pred_lr),
            'Precision': precision_score(y_test, y_pred_lr),
            'Recall': recall_score(y_test, y_pred_lr)
        }
        
        for metric, value in results['Enhanced Logistic Regression'].items():
            print(f"  {metric:12s}: {value:.4f}")
    
    # Enhanced XGBoost
    print("\n" + "-"*80)
    print("Evaluating Enhanced XGBoost (tuned)...")
    print("-"*80)
    if os.path.exists(xgb_enhanced_path):
        xgb_enhanced = joblib.load(xgb_enhanced_path)
        y_pred_xgb = xgb_enhanced.predict(X_test)
        y_prob_xgb = xgb_enhanced.predict_proba(X_test)[:, 1]
        
        results['Enhanced XGBoost'] = {
            'ROC-AUC': roc_auc_score(y_test, y_prob_xgb),
            'F1-Score': f1_score(y_test, y_pred_xgb),
            'Precision': precision_score(y_test, y_pred_xgb),
            'Recall': recall_score(y_test, y_pred_xgb)
        }
        
        for metric, value in results['Enhanced XGBoost'].items():
            print(f"  {metric:12s}: {value:.4f}")
    
    # Ensemble (weighted average of all 3 models)
    if 'Enhanced Random Forest' in results and 'Enhanced XGBoost' in results and 'Enhanced Logistic Regression' in results:
        print("\n" + "-"*80)
        print("Evaluating Ensemble (weighted voting)...")
        print("-"*80)
        
        # Load ensemble weights
        with open('models/ensemble_metadata.json', 'r') as f:
            ensemble_meta = json.load(f)
        
        print(f"  Weights: {ensemble_meta['weights']}")
        
        # Weighted ensemble prediction (all 3 models)
        y_prob_ensemble = (
            y_prob_rf * ensemble_meta['weights']['Random Forest'] +
            y_prob_xgb * ensemble_meta['weights']['XGBoost'] +
            y_prob_lr * ensemble_meta['weights']['Logistic Regression']
        )
        y_pred_ensemble = (y_prob_ensemble > 0.5).astype(int)
        
        results['Ensemble'] = {
            'ROC-AUC': roc_auc_score(y_test, y_prob_ensemble),
            'F1-Score': f1_score(y_test, y_pred_ensemble),
            'Precision': precision_score(y_test, y_pred_ensemble),
            'Recall': recall_score(y_test, y_pred_ensemble)
        }
        
        for metric, value in results['Ensemble'].items():
            print(f"  {metric:12s}: {value:.4f}")
    
    # Summary comparison
    print("\n" + "="*80)
    print("Summary Comparison")
    print("="*80)
    print(f"{'Model':<35} {'ROC-AUC':>10} {'F1':>10} {'Precision':>10} {'Recall':>10}")
    print("-"*80)
    
    for model_name, metrics in results.items():
        print(f"{model_name:<35} {metrics['ROC-AUC']:>10.4f} {metrics['F1-Score']:>10.4f} "
              f"{metrics['Precision']:>10.4f} {metrics['Recall']:>10.4f}")
    
    # Improvements over baseline
    if 'Baseline Random Forest' in results:
        print("\n" + "="*80)
        print("Improvements Over Baseline")
        print("="*80)
        
        baseline_metrics = results['Baseline Random Forest']
        
        for model_name, metrics in results.items():
            if model_name == 'Baseline Random Forest':
                continue
            
            print(f"\n{model_name}:")
            for metric in ['ROC-AUC', 'F1-Score', 'Precision', 'Recall']:
                improvement = metrics[metric] - baseline_metrics[metric]
                pct_change = (improvement / baseline_metrics[metric]) * 100 if baseline_metrics[metric] > 0 else 0
                sign = "+" if improvement > 0 else ""
                print(f"  {metric:12s}: {sign}{improvement:>7.4f} ({sign}{pct_change:>6.2f}%)")
    
    # Save comparison report
    save_comparison_report(results)
    
    return results


def save_comparison_report(results):
    """Save comparison to markdown file."""
    report_path = 'docs/model_comparison.md'
    
    with open(report_path, 'w') as f:
        f.write("# Model Performance Comparison\\n\\n")
        f.write("Comparison between baseline and enhanced models.\\n\\n")
        
        f.write("## Performance Metrics\\n\\n")
        f.write("| Model | ROC-AUC | F1-Score | Precision | Recall |\\n")
        f.write("|-------|---------|----------|-----------|--------|\\n")
        
        for model_name, metrics in results.items():
            f.write(f"| {model_name} | {metrics['ROC-AUC']:.4f} | {metrics['F1-Score']:.4f} | ")
            f.write(f"{metrics['Precision']:.4f} | {metrics['Recall']:.4f} |\\n")
        
        # Key improvements
        if 'Baseline Random Forest' in results and 'Enhanced Logistic Regression' in results:
            f.write("\\n## Key Improvements\\n\\n")
            
            baseline = results['Baseline Random Forest']
            best_enhanced = results['Enhanced Logistic Regression']
            
            recall_improvement = best_enhanced['Recall'] - baseline['Recall']
            recall_pct = (recall_improvement / baseline['Recall']) * 100
            
            f.write(f"- **Recall**: Improved from {baseline['Recall']:.2%} to {best_enhanced['Recall']:.2%} ")
            f.write(f"(+{recall_improvement:.2%}, +{recall_pct:.1f}% relative improvement)\\n")
            f.write(f"- **ROC-AUC**: Maintained at {best_enhanced['ROC-AUC']:.4f}\\n")
            f.write(f"- **F1-Score**: Improved from {baseline['F1-Score']:.4f} to {best_enhanced['F1-Score']:.4f}\\n")
    
    print(f"\\nComparison report saved to {report_path}")


if __name__ == "__main__":
    os.chdir('/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject')
    results = compare_models()
