"""
Generate comprehensive SHAP visualizations for model interpretability.
Saves all plots to Data Viz folder.
"""

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import shap
from pathlib import Path

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
    """Load test data for SHAP visualization."""
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
    
    # Use test split
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    return X_test, y_test


def generate_shap_visualizations():
    """Generate all SHAP visualizations for Random Forest model."""
    print("="*80)
    print("Generating SHAP Visualizations")
    print("="*80)
    
    # Load Random Forest model (tree-based for SHAP)
    model_path = 'models/random_forest_model.pkl'
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        return
    
    print(f"\nLoading model from {model_path}...")
    model = joblib.load(model_path)
    
    # Load data
    print("Loading test data...")
    X_test, y_test = load_test_data()
    
    # Transform data
    preprocessor = model.named_steps['preprocessor']
    classifier = model.named_steps['classifier']
    
    print("Transforming data...")
    X_test_transformed = preprocessor.transform(X_test)
    
    # Convert to dense array if sparse
    if hasattr(X_test_transformed, 'toarray'):
        X_test_transformed = X_test_transformed.toarray()
    
    # Get feature names
    numeric_features = list(preprocessor.transformers_[0][2])
    categorical_features = preprocessor.transformers_[1][2]
    encoder = preprocessor.transformers_[1][1]['encoder']
    
    feature_names = numeric_features.copy()
    if hasattr(encoder, 'get_feature_names_out'):
        cat_feature_names = encoder.get_feature_names_out(categorical_features)
        feature_names.extend(cat_feature_names)
    
    # Map to readable names
    readable_feature_names = map_feature_names(feature_names)
    
    # Sample data for SHAP (computational efficiency)
    sample_size = min(100, len(X_test))
    indices = np.random.RandomState(42).choice(len(X_test), sample_size, replace=False)
    X_sample = X_test_transformed[indices]
    
    print(f"Calculating SHAP values for {sample_size} samples...")
    
    # Create SHAP explainer
    explainer = shap.TreeExplainer(classifier)
    shap_values = explainer.shap_values(X_sample)
    
    # Handle multi-class output
    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # Positive class
    
    print(f"\n✓ SHAP values calculated (shape: {shap_values.shape})")
    
    # 1. SHAP Summary Plot (Bar)
    print("\n1. Generating SHAP summary plot (bar)...")
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_sample, feature_names=readable_feature_names, 
                      plot_type="bar", show=False, max_display=15)
    plt.title('SHAP Feature Importance (Random Forest)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '1_shap_summary_bar.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 1_shap_summary_bar.png")
    
    # 2. SHAP Summary Plot (Beeswarm)
    print("\n2. Generating SHAP summary plot (beeswarm)...")
    plt.figure(figsize=(12, 10))
    shap.summary_plot(shap_values, X_sample, feature_names=readable_feature_names, 
                      show=False, max_display=20)
    plt.title('SHAP Feature Impact Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '2_shap_summary_beeswarm.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 2_shap_summary_beeswarm.png")
    
    # 3. SHAP Waterfall Plot (first prediction)
    print("\n3. Generating SHAP waterfall plot...")
    try:
        plt.figure(figsize=(10, 8))
        base_value = explainer.expected_value
        if isinstance(base_value, (list, np.ndarray)):
            base_value = base_value[1] if len(base_value) > 1 else base_value[0]
        
        shap_explanation = shap.Explanation(
            values=shap_values[0],
            base_values=base_value,
            data=X_sample[0],
            feature_names=readable_feature_names
        )
        shap.waterfall_plot(shap_explanation, max_display=15, show=False)
        plt.title('SHAP Waterfall Plot - Sample Prediction', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / '3_shap_waterfall.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Saved: 3_shap_waterfall.png")
    except Exception as e:
        print(f"   ✗ Skipped waterfall plot: {e}")
    
    # 4. SHAP Force Plot (first 3 predictions)
    print("\n4. Generating SHAP force plots...")
    try:
        base_value = explainer.expected_value
        if isinstance(base_value, (list, np.ndarray)):
            base_value = base_value[1] if len(base_value) > 1 else base_value[0]
        
        for i in range(min(3, len(X_sample))):
            plt.figure(figsize=(14, 3))
            shap.force_plot(
                base_value,
                shap_values[i],
                X_sample[i],
                feature_names=readable_feature_names,
                matplotlib=True,
                show=False
            )
            plt.title(f'SHAP Force Plot - Prediction {i+1}', fontsize=12, fontweight='bold')
            plt.tight_layout()
            plt.savefig(OUTPUT_DIR / f'4_shap_force_plot_{i+1}.png', dpi=300, bbox_inches='tight')
            plt.close()
        print(f"   ✓ Saved: 4_shap_force_plot_1-3.png")
    except Exception as e:
        print(f"   ✗ Skipped force plots: {e}")
    
    # 5. SHAP Dependence Plots (top 5 features)
    print("\n5. Generating SHAP dependence plots...")
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    top_feature_indices = np.argsort(mean_abs_shap)[-5:][::-1]
    
    for idx in top_feature_indices:
        plt.figure(figsize=(10, 6))
        shap.dependence_plot(
            idx,
            shap_values,
            X_sample,
            feature_names=readable_feature_names,
            show=False
        )
        feature_name = readable_feature_names[idx].replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').replace(':', '')[:40]
        plt.title(f'SHAP Dependence Plot: {readable_feature_names[idx]}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f'5_shap_dependence_{feature_name}.png', dpi=300, bbox_inches='tight')
        plt.close()
    print(f"   ✓ Saved: 5_shap_dependence_*.png (top 5 features)")
    
    # 6. SHAP Decision Plot
    print("\n6. Generating SHAP decision plot...")
    plt.figure(figsize=(12, 10))
    shap.decision_plot(
        explainer.expected_value if not isinstance(explainer.expected_value, list) 
            else explainer.expected_value[1],
        shap_values[:20],  # First 20 predictions
        feature_names=feature_names,
        show=False,
        highlight=[0, 5, 10]  # Highlight a few predictions
    )
    plt.title('SHAP Decision Plot - Multiple Predictions', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '6_shap_decision_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: 6_shap_decision_plot.png")
    
    print(f"\n{'='*80}")
    print(f"✓ All SHAP visualizations saved to: {OUTPUT_DIR}")
    print(f"{'='*80}")


if __name__ == "__main__":
    os.chdir('/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject')
    generate_shap_visualizations()
