"""
Generate comprehensive model performance visualizations.
Saves all plots to Data Viz folder.
"""

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
from sklearn.metrics import (roc_curve, auc, precision_recall_curve, confusion_matrix,
                             classification_report)
try:
    from sklearn.calibration import calibration_curve
except ImportError:
    from sklearn.metrics import calibration_curve
from sklearn.model_selection import train_test_split

# Import feature name mapping
import sys
sys.path.append('/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/scripts')
from feature_names import map_feature_names

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Output directory
OUTPUT_DIR = Path('/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/Data Viz')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_test_data():
    """Load and prepare test data."""
    data_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/data/processed/longterm_care_cleaned.csv'
    df = pd.read_csv(data_path, low_memory=False)
    
    # Prepare target
    target_col = 'Penalized'
    if 'Penalized?' in df.columns:
        df.rename(columns={'Penalized?': target_col}, inplace=True)
    df[target_col] = df[target_col].astype(int)
    
    # Drop non-predictive columns
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
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    return X_test, y_test


def plot_roc_comparison():
    """Generate ROC curve comparison for all models."""
    print("\n1. Generating ROC curve comparison...")
    
    X_test, y_test = load_test_data()
    
    models = {
        'Baseline RF': 'models/risk_model.pkl',
        'Enhanced RF': 'models/random_forest_model.pkl',
        'Enhanced LR': 'models/logistic_regression_model.pkl'
    }
    
    plt.figure(figsize=(10, 8))
    
    for name, path in models.items():
        if os.path.exists(path):
            model = joblib.load(path)
            y_proba = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.4f})', linewidth=2)
    
    plt.plot([0, 1], [0, 1], 'k--', label='Baseline (AUC = 0.5000)', linewidth=1)
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curve Comparison', fontsize=16, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '7_roc_curve_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 7_roc_curve_comparison.png")


def plot_precision_recall_curve():
    """Generate Precision-Recall curve comparison."""
    print("\n2. Generating Precision-Recall curve...")
    
    X_test, y_test = load_test_data()
    
    models = {
        'Baseline RF': 'models/risk_model.pkl',
        'Enhanced RF': 'models/random_forest_model.pkl',
        'Enhanced LR': 'models/logistic_regression_model.pkl'
    }
    
    plt.figure(figsize=(10, 8))
    
    for name, path in models.items():
        if os.path.exists(path):
            model = joblib.load(path)
            y_proba = model.predict_proba(X_test)[:, 1]
            precision, recall, _ = precision_recall_curve(y_test, y_proba)
            plt.plot(recall, precision, label=name, linewidth=2)
    
    # Baseline (proportion of positive class)
    baseline = y_test.mean()
    plt.plot([0, 1], [baseline, baseline], 'k--', label=f'Baseline ({baseline:.2f})', linewidth=1)
    
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title('Precision-Recall Curve', fontsize=16, fontweight='bold')
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '8_precision_recall_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 8_precision_recall_curve.png")


def plot_confusion_matrices():
    """Generate confusion matrices for all models."""
    print("\n3. Generating confusion matrices...")
    
    X_test, y_test = load_test_data()
    
    models = {
        'Baseline Random Forest': 'models/risk_model.pkl',
        'Enhanced Random Forest': 'models/random_forest_model.pkl',
        'Enhanced Logistic Regression': 'models/logistic_regression_model.pkl'
    }
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for idx, (name, path) in enumerate(models.items()):
        if os.path.exists(path):
            model = joblib.load(path)
            y_pred = model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['Not Penalized', 'Penalized'],
                       yticklabels=['Not Penalized', 'Penalized'])
            axes[idx].set_title(name, fontsize=12, fontweight='bold')
            axes[idx].set_ylabel('Actual')
            axes[idx].set_xlabel('Predicted')
    
    plt.suptitle('Confusion Matrices Comparison', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '9_confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 9_confusion_matrices.png")


def plot_calibration_curve():
    """Generate calibration plot."""
    print("\n4. Generating calibration curve...")
    
    X_test, y_test = load_test_data()
    
    models = {
        'Baseline RF': 'models/risk_model.pkl',
        'Enhanced RF': 'models/random_forest_model.pkl',
        'Enhanced LR': 'models/logistic_regression_model.pkl'
    }
    
    plt.figure(figsize=(10, 8))
    
    for name, path in models.items():
        if os.path.exists(path):
            model = joblib.load(path)
            y_proba = model.predict_proba(X_test)[:, 1]
            
            fraction_of_positives, mean_predicted_value = calibration_curve(
                y_test, y_proba, n_bins=10, strategy='uniform'
            )
            plt.plot(mean_predicted_value, fraction_of_positives, marker='o',
                    label=name, linewidth=2, markersize=8)
    
    plt.plot([0, 1], [0, 1], 'k--', label='Perfectly calibrated', linewidth=1)
    plt.xlabel('Mean Predicted Probability', fontsize=12)
    plt.ylabel('Fraction of Positives', fontsize=12)
    plt.title('Calibration Plot', fontsize=16, fontweight='bold')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '10_calibration_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 10_calibration_plot.png")


def plot_feature_importance_comparison():
    """Compare feature importances between models."""
    print("\n5. Generating feature importance comparison...")
    
    # Get Random Forest feature importances
    rf_model = joblib.load('models/random_forest_model.pkl')
    rf_classifier = rf_model.named_steps['classifier']
    
    if hasattr(rf_classifier, 'feature_importances_'):
        preprocessor = rf_model.named_steps['preprocessor']
        numeric_features = list(preprocessor.transformers_[0][2])
        categorical_features = preprocessor.transformers_[1][2]
        encoder = preprocessor.transformers_[1][1]['encoder']
        
        feature_names = numeric_features.copy()
        if hasattr(encoder, 'get_feature_names_out'):
            cat_names = encoder.get_feature_names_out(categorical_features)
            feature_names.extend(cat_names)
        
        # Map to readable names
        readable_feature_names = map_feature_names(feature_names)
        
        importances = rf_classifier.feature_importances_
        
        # Get top 20 features
        indices = np.argsort(importances)[-20:]
        
        plt.figure(figsize=(12, 10))
        plt.barh(range(len(indices)), importances[indices], color='steelblue')
        plt.yticks(range(len(indices)), [readable_feature_names[i] for i in indices], fontsize=9)
        plt.xlabel('Importance', fontsize=12)
        plt.title('Top 20 Feature Importances (Random Forest)', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / '11_feature_importance_rf.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Saved: 11_feature_importance_rf.png")


def plot_metrics_comparison():
    """Create bar chart comparing all metrics across models."""
    print("\n6. Generating metrics comparison chart...")
    
    # Updated data with XGBoost and corrected Ensemble
    metrics_data = {
        'Baseline RF': {'ROC-AUC': 0.7861, 'F1': 0.5376, 'Precision': 0.6691, 'Recall': 0.4493},
        'Enhanced RF': {'ROC-AUC': 0.7812, 'F1': 0.5514, 'Precision': 0.6258, 'Recall': 0.4928},
        'Enhanced XGBoost': {'ROC-AUC': 0.8035, 'F1': 0.5957, 'Precision': 0.6627, 'Recall': 0.5411},
        'Enhanced LR': {'ROC-AUC': 0.7661, 'F1': 0.6034, 'Precision': 0.5447, 'Recall': 0.6763},
        'Ensemble (3 models)': {'ROC-AUC': 0.8054, 'F1': 0.6108, 'Precision': 0.6231, 'Recall': 0.5990}
    }
    
    df = pd.DataFrame(metrics_data).T
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    metrics = ['ROC-AUC', 'F1', 'Precision', 'Recall']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]
        df[metric].plot(kind='bar', ax=ax, color=colors)
        ax.set_title(metric, fontsize=14, fontweight='bold')
        ax.set_ylabel('Score', fontsize=11)
        ax.set_xlabel('')
        ax.set_xticklabels(df.index, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0, 1])
        
        # Add value labels on bars
        for i, v in enumerate(df[metric]):
            ax.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom', fontsize=9)
    
    plt.suptitle('Model Performance Metrics Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '12_metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 12_metrics_comparison.png")


if __name__ == "__main__":
    os.chdir('/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject')
    
    print("="*80)
    print("Generating Model Performance Visualizations")
    print("="*80)
    
    plot_roc_comparison()
    plot_precision_recall_curve()
    plot_confusion_matrices()
    plot_calibration_curve()
    plot_feature_importance_comparison()
    plot_metrics_comparison()
    
    print(f"\n{'='*80}")
    print(f"✓ All model visualizations saved to: {OUTPUT_DIR}")
    print(f"{'='*80}")
