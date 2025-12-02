import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, confusion_matrix, accuracy_score, roc_auc_score, recall_score, precision_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import xgboost as xgb
import shap
import os
import sys

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hospital_feature_names import convert_feature_name, convert_feature_names

def visualize_hospital_models():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'processed', 'hospital_cleaned.csv')
    output_dir = os.path.join(base_dir, 'dataviz-hospitals')
    
    print("Loading data...")
    df = pd.read_csv(input_file, low_memory=False)
    
    # Prepare data
    target_col = 'Penalized?'
    drop_cols = ['FACID', 'FAC_NAME', 'LICENSE_NUMBER', 'ADDRESS', 'CITY', 'ZIP_CODE', 'year', 'FAC_NO', 'HCAI_ID']
    drop_cols += [c for c in df.columns if 'LICENSE' in c or 'NAME' in c or 'DATE' in c]
    
    # CRITICAL: Exclude penalty-related features
    penalty_related = ['Total Amount Due Final', 'Total Records Found']
    drop_cols += penalty_related
    
    X = df.drop(columns=[target_col] + [c for c in drop_cols if c in df.columns])
    y = df[target_col]
    
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns
    
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
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train models
    print("Training models...")
    rf = Pipeline(steps=[('preprocessor', preprocessor),
                         ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))])
    rf.fit(X_train, y_train)
    
    lr = Pipeline(steps=[('preprocessor', preprocessor),
                         ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced'))])
    lr.fit(X_train, y_train)
    
    lgbm = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', lgb.LGBMClassifier(n_estimators=100, random_state=42, class_weight='balanced', verbose=-1))])
    lgbm.fit(X_train, y_train)
    
    xgbm = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', xgb.XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='logloss'))])
    xgbm.fit(X_train, y_train)
    
    # Predictions
    y_pred_rf = rf.predict(X_test)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]
    y_pred_lr = lr.predict(X_test)
    y_prob_lr = lr.predict_proba(X_test)[:, 1]
    y_pred_lgbm = lgbm.predict(X_test)
    y_prob_lgbm = lgbm.predict_proba(X_test)[:, 1]
    y_pred_xgbm = xgbm.predict(X_test)
    y_prob_xgbm = xgbm.predict_proba(X_test)[:, 1]
    
    # Metrics
    metrics = {
        'Random Forest': {
            'Accuracy': accuracy_score(y_test, y_pred_rf),
            'ROC-AUC': roc_auc_score(y_test, y_prob_rf),
            'Recall': recall_score(y_test, y_pred_rf),
            'Precision': precision_score(y_test, y_pred_rf)
        },
        'Logistic Regression': {
            'Accuracy': accuracy_score(y_test, y_pred_lr),
            'ROC-AUC': roc_auc_score(y_test, y_prob_lr),
            'Recall': recall_score(y_test, y_pred_lr),
            'Precision': precision_score(y_test, y_pred_lr)
        },
        'LightGBM': {
            'Accuracy': accuracy_score(y_test, y_pred_lgbm),
            'ROC-AUC': roc_auc_score(y_test, y_prob_lgbm),
            'Recall': recall_score(y_test, y_pred_lgbm),
            'Precision': precision_score(y_test, y_pred_lgbm)
        },
        'XGBoost': {
            'Accuracy': accuracy_score(y_test, y_pred_xgbm),
            'ROC-AUC': roc_auc_score(y_test, y_prob_xgbm),
            'Recall': recall_score(y_test, y_pred_xgbm),
            'Precision': precision_score(y_test, y_pred_xgbm)
        }
    }
    
    # Feature names
    if hasattr(rf.named_steps['preprocessor'], 'get_feature_names_out'):
        feature_names = rf.named_steps['preprocessor'].get_feature_names_out()
    else:
        feature_names = numeric_features.tolist() + list(rf.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot'].get_feature_names_out(categorical_features))
    
    # 1. Top 10 Features
    print("Creating feature importance plot...")
    importances = rf.named_steps['classifier'].feature_importances_
    indices = np.argsort(importances)[-10:]
    
    # Convert to full names
    full_names = [convert_feature_name(feature_names[i]) for i in indices]
    
    plt.figure(figsize=(12, 7))
    plt.barh(range(10), importances[indices], color='steelblue')
    plt.yticks(range(10), full_names, fontsize=10)
    plt.xlabel('Importance', fontsize=12)
    plt.title('Top 10 Features - Random Forest', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_top_10_features.png'), dpi=300)
    plt.close()
    
    # 2. Model Comparison Metrics
    print("Creating model comparison plot...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    metric_names = ['Accuracy', 'ROC-AUC', 'Recall', 'Precision']
    model_names = ['RF', 'LR', 'LightGBM', 'XGBoost']
    colors = ['steelblue', 'coral', 'mediumseagreen', 'gold']
    
    for idx, metric in enumerate(metric_names):
        ax = axes[idx // 2, idx % 2]
        values = [metrics[m][metric] for m in ['Random Forest', 'Logistic Regression', 'LightGBM', 'XGBoost']]
        bars = ax.bar(model_names, values, color=colors)
        ax.set_ylabel(metric, fontsize=11)
        ax.set_ylim(0, 1)
        ax.set_title(f'{metric} Comparison', fontsize=12, fontweight='bold')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_model_comparison_metrics.png'), dpi=300)
    plt.close()
    
    # 3. ROC Curves
    print("Creating ROC curves...")
    fpr_rf, tpr_rf, _ = roc_curve(y_test, y_prob_rf)
    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_prob_lr)
    fpr_lgbm, tpr_lgbm, _ = roc_curve(y_test, y_prob_lgbm)
    fpr_xgbm, tpr_xgbm, _ = roc_curve(y_test, y_prob_xgbm)
    
    roc_auc_rf = auc(fpr_rf, tpr_rf)
    roc_auc_lr = auc(fpr_lr, tpr_lr)
    roc_auc_lgbm = auc(fpr_lgbm, tpr_lgbm)
    roc_auc_xgbm = auc(fpr_xgbm, tpr_xgbm)
    
    plt.figure(figsize=(10, 7))
    plt.plot(fpr_rf, tpr_rf, color='steelblue', lw=2, label=f'Random Forest (AUC = {roc_auc_rf:.3f})')
    plt.plot(fpr_lr, tpr_lr, color='coral', lw=2, label=f'Logistic Regression (AUC = {roc_auc_lr:.3f})')
    plt.plot(fpr_lgbm, tpr_lgbm, color='mediumseagreen', lw=2, label=f'LightGBM (AUC = {roc_auc_lgbm:.3f})')
    plt.plot(fpr_xgbm, tpr_xgbm, color='gold', lw=2, label=f'XGBoost (AUC = {roc_auc_xgbm:.3f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_roc_curves.png'), dpi=300)
    plt.close()
    
    # 4. Confusion Matrices
    print("Creating confusion matrices...")
    cm_rf = confusion_matrix(y_test, y_pred_rf)
    cm_lr = confusion_matrix(y_test, y_pred_lr)
    cm_lgbm = confusion_matrix(y_test, y_pred_lgbm)
    cm_xgbm = confusion_matrix(y_test, y_pred_xgbm)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0], cbar=False)
    axes[0, 0].set_title('Random Forest', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Predicted', fontsize=11)
    axes[0, 0].set_ylabel('Actual', fontsize=11)
    
    sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Oranges', ax=axes[0, 1], cbar=False)
    axes[0, 1].set_title('Logistic Regression', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Predicted', fontsize=11)
    axes[0, 1].set_ylabel('Actual', fontsize=11)
    
    sns.heatmap(cm_lgbm, annot=True, fmt='d', cmap='Greens', ax=axes[1, 0], cbar=False)
    axes[1, 0].set_title('LightGBM', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Predicted', fontsize=11)
    axes[1, 0].set_ylabel('Actual', fontsize=11)
    
    sns.heatmap(cm_xgbm, annot=True, fmt='d', cmap='YlOrBr', ax=axes[1, 1], cbar=False)
    axes[1, 1].set_title('XGBoost', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Predicted', fontsize=11)
    axes[1, 1].set_ylabel('Actual', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_confusion_matrices.png'), dpi=300)
    plt.close()
    
    # 5. SHAP Summary Plot
    print("Creating SHAP visualizations...")
    X_train_transformed = rf.named_steps['preprocessor'].transform(X_train)
    
    # Convert sparse matrix to dense array if needed
    if hasattr(X_train_transformed, 'toarray'):
        X_train_transformed = X_train_transformed.toarray()
    
    explainer = shap.TreeExplainer(rf.named_steps['classifier'])
    shap_values = explainer.shap_values(X_train_transformed[:100])  # Use subset for speed
    
    # SHAP values can be 2D or 3D depending on sklearn version
    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # Positive class
    
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_train_transformed[:100], feature_names=feature_names, show=False, max_display=10)
    plt.title('SHAP Summary Plot - Top 10 Features', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_shap_summary.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. SHAP Waterfall Plot
    print("Creating SHAP waterfall plot...")
    plt.figure(figsize=(10, 6))
    shap.waterfall_plot(shap.Explanation(values=shap_values[0], 
                                         base_values=explainer.expected_value if not isinstance(explainer.expected_value, np.ndarray) else explainer.expected_value[1],
                                         data=X_train_transformed[0],
                                         feature_names=feature_names),
                       max_display=10, show=False)
    plt.title('SHAP Waterfall Plot - Example Prediction', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_shap_waterfall.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"All visualizations saved to {output_dir}")

if __name__ == "__main__":
    visualize_hospital_models()
