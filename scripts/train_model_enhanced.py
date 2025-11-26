"""
Enhanced model training script with class balancing, hyperparameter tuning,
multi-model ensemble, and SHAP interpretability.
"""

import pandas as pd
import numpy as np
import os
import joblib
import yaml
import json
from datetime import datetime
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, roc_auc_score, f1_score,
    precision_score, recall_score, confusion_matrix
)
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt

try:
    import xgboost as xgb
    XGB_AVAILABLE = True
    print("XGBoost available")
except Exception as e:
    XGB_AVAILABLE = False
    print(f"XGBoost not available: {e}")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("SHAP not available, skipping SHAP calculations")


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def prepare_data(input_file, config):
    """Load and prepare data for training."""
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, low_memory=False)
    
    # Create target variable
    target_col = 'Penalized'
    if 'Penalized?' in df.columns:
        df.rename(columns={'Penalized?': target_col}, inplace=True)
    
    df[target_col] = df[target_col].astype(int)
    
    print(f"Target distribution:\n{df[target_col].value_counts(normalize=True)}")
    
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
    
    # Staffing ratios
    staffing_cols = ['PRDHR_RN', 'PRDHR_LVN', 'PRDHR_NA']
    for col in staffing_cols:
        if col in df_model.columns and 'DAY_TOTL' in df_model.columns:
            df_model[f'{col}_Per_Day'] = df_model[col] / df_model['DAY_TOTL'].replace(0, np.nan)
    
    # Separate features and target
    X = df_model.drop(columns=[target_col])
    y = df_model[target_col]
    
    return X, y


def create_preprocessor(X):
    """Create preprocessing pipeline, excluding LA geographic features."""
    # Get all numeric and categorical features
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()
    
    # Filter out LA geographic features from categorical
    # Remove COUNTY and HSA columns entirely - they'll be one-hot encoded with LA values
    geographic_cols_to_exclude = ['COUNTY_x', 'COUNTY_y', 'HSA']
    categorical_features = [f for f in categorical_features if f not in geographic_cols_to_exclude]
    
    print(f"Numeric features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)} (excluded geographic features)")
    print(f"Excluded: {geographic_cols_to_exclude}")
    
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
    
    return preprocessor, numeric_features, categorical_features


def apply_class_balancing(X_train, y_train, config):
    """Apply class balancing if configured."""
    method = config['class_balancing']['method']
    
    if method == 'smote':
        print("Applying SMOTE for class balancing...")
        smote = SMOTE(
            random_state=config['training']['random_state'],
            k_neighbors=config['class_balancing']['smote_k_neighbors'],
            sampling_strategy=config['class_balancing']['smote_sampling_strategy']
        )
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        print(f"After SMOTE: {len(X_train_balanced)} samples")
        return X_train_balanced, y_train_balanced
    else:
        print("Using class weights (no resampling)")
        return X_train, y_train


def train_model_with_tuning(name, model, param_dist, preprocessor, X_train, y_train, config):
    """Train a model with hyperparameter tuning."""
    print(f"\n{'='*60}")
    print(f"Training {name}...")
    print(f"{'='*60}")
    
    # Create pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])
    
    if config['hyperparameter_tuning']['enabled']:
        print(f"Hyperparameter tuning enabled (n_iter={config['hyperparameter_tuning']['n_iter']})")
        
        # Prefix parameters with 'classifier__'
        prefixed_params = {f"classifier__{k}": v for k, v in param_dist.items()}
        
        search = RandomizedSearchCV(
            pipeline,
            param_distributions=prefixed_params,
            n_iter=config['hyperparameter_tuning']['n_iter'],
            cv=config['hyperparameter_tuning']['cv_folds'],
            scoring=config['hyperparameter_tuning']['scoring'],
            random_state=config['training']['random_state'],
            n_jobs=config['hyperparameter_tuning']['n_jobs'],
            verbose=1
        )
        
        search.fit(X_train, y_train)
        print(f"Best parameters: {search.best_params_}")
        print(f"Best CV score: {search.best_score_:.4f}")
        
        return search.best_estimator_
    else:
        print("Hyperparameter tuning disabled, using default parameters")
        pipeline.fit(X_train, y_train)
        return pipeline


def evaluate_model(name, model, X_test, y_test):
    """Evaluate model performance."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'model': name,
        'roc_auc': roc_auc_score(y_test, y_proba),
        'f1': f1_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred)
    }
    
    print(f"\n{name} Performance:")
    print(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")
    print(f"  F1-Score:  {metrics['f1']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    
    return metrics, y_pred, y_proba


def calculate_shap_values(model, X_train, X_test, feature_names, config):
    """Calculate SHAP values for model interpretability."""
    if not SHAP_AVAILABLE or not config['shap']['enabled']:
        return None
    
    print("\nCalculating SHAP values...")
    
    try:
        # Get preprocessor and classifier
        preprocessor = model.named_steps['preprocessor']
        classifier = model.named_steps['classifier']
        
        # Sample background data
        n_samples = min(config['shap']['background_samples'], len(X_train))
        X_background = X_train.sample(n=n_samples, random_state=42)
        X_background_transformed = preprocessor.transform(X_background)
        
        # Create explainer
        explainer = shap.TreeExplainer(classifier, X_background_transformed)
        
        # Calculate SHAP values for test set (sample if too large)
        n_test_samples = min(100, len(X_test))
        X_test_sample = X_test.sample(n=n_test_samples, random_state=42)
        X_test_transformed = preprocessor.transform(X_test_sample)
        
        shap_values = explainer.shap_values(X_test_transformed)
        
        # Handle multi-class output
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # Get SHAP values for positive class
        
        print(f"SHAP values calculated for {n_test_samples} test samples")
        
        return {
            'explainer': explainer,
            'shap_values': shap_values,
            'feature_names': feature_names,
            'X_test_sample': X_test_sample,
            'X_test_transformed': X_test_transformed
        }
    
    except Exception as e:
        print(f"Error calculating SHAP values: {e}")
        return None


def train_enhanced_models(input_file, config_path):
    """Main training function with all enhancements."""
    
    # Load configuration
    config = load_config(config_path)
    print("Configuration loaded:")
    print(yaml.dump(config, default_flow_style=False))
    
    # Prepare data
    X, y = prepare_data(input_file, config)
    
    # Create preprocessor
    preprocessor, numeric_features, categorical_features = create_preprocessor(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config['training']['test_size'],
        random_state=config['training']['random_state'],
        stratify=y if config['training']['stratify'] else None
    )
    
    print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Apply class balancing if using SMOTE
    if config['class_balancing']['method'] == 'smote':
        # Pre-process data for SMOTE
        X_train_preprocessed = preprocessor.fit_transform(X_train)
        X_train_balanced, y_train_balanced = apply_class_balancing(X_train_preprocessed, y_train, config)
        # Note: When using SMOTE, we need to fit preprocessor separately
    else:
        X_train_balanced, y_train_balanced = X_train, y_train
    
    # Define models
    models_config = {}
    
    if config['models']['random_forest']['enabled']:
        models_config['Random Forest'] = {
            'model': RandomForestClassifier(random_state=config['training']['random_state']),
            'params': config['models']['random_forest']['params']
        }
    
    if config['models']['xgboost']['enabled'] and XGB_AVAILABLE:
        models_config['XGBoost'] = {
            'model': xgb.XGBClassifier(
                random_state=config['training']['random_state'],
                use_label_encoder=False,
                eval_metric='logloss'
            ),
            'params': config['models']['xgboost']['params']
        }
    
    if config['models']['logistic_regression']['enabled']:
        models_config['Logistic Regression'] = {
            'model': LogisticRegression(random_state=config['training']['random_state']),
            'params': config['models']['logistic_regression']['params']
        }
    
    # Train models
    trained_models = {}
    all_metrics = []
    predictions = {}
    
    for name, model_config in models_config.items():
        trained_model = train_model_with_tuning(
            name,
            model_config['model'],
            model_config['params'],
            preprocessor,
            X_train_balanced,
            y_train_balanced,
            config
        )
        
        trained_models[name] = trained_model
        
        metrics, y_pred, y_proba = evaluate_model(name, trained_model, X_test, y_test)
        all_metrics.append(metrics)
        predictions[name] = {'pred': y_pred, 'proba': y_proba}
    
    # Find best model
    best_model_name = max(all_metrics, key=lambda x: x['roc_auc'])['model']
    best_model = trained_models[best_model_name]
    
    print(f"\n{'='*60}")
    print(f"Best Model: {best_model_name}")
    print(f"{'='*60}")
    
    # Calculate SHAP values for best model
    shap_data = None
    if config['shap']['enabled']:
        # Get all feature names after preprocessing from the fitted best model
        best_preprocessor = best_model.named_steps['preprocessor']
        
        feature_names = list(numeric_features)
        # Access the fitted encoder  
        encoder = best_preprocessor.transformers_[1][1]['encoder']
        if hasattr(encoder, 'get_feature_names_out'):
            cat_feature_names = encoder.get_feature_names_out(categorical_features)
            feature_names.extend(cat_feature_names)
        
        shap_data = calculate_shap_values(best_model, X_train, X_test, feature_names, config)
    
    # Save models
    model_dir = config['output']['model_dir']
    os.makedirs(model_dir, exist_ok=True)
    
    if config['output']['save_individual_models']:
        for name, model in trained_models.items():
            model_filename = name.lower().replace(' ', '_') + '_model.pkl'
            model_path = os.path.join(model_dir, model_filename)
            joblib.dump(model, model_path)
            print(f"Saved {name} to {model_path}")
    
    # Save best model as default
    best_model_path = os.path.join(model_dir, 'risk_model_enhanced.pkl')
    joblib.dump(best_model, best_model_path)
    print(f"Saved best model to {best_model_path}")
    
    # Save ensemble metadata
    if config['ensemble']['enabled']:
        ensemble_metadata = {
            'models': list(trained_models.keys()),
            'weights': {name: metrics['roc_auc'] for name, metrics in zip(trained_models.keys(), all_metrics)},
            'best_model': best_model_name,
            'weighting_method': config['ensemble']['weighting_method']
        }
        
        # Normalize weights
        if ensemble_metadata['weighting_method'] == 'performance':
            total_weight = sum(ensemble_metadata['weights'].values())
            ensemble_metadata['weights'] = {
                k: v / total_weight for k, v in ensemble_metadata['weights'].items()
            }
        else:  # equal weighting
            n_models = len(trained_models)
            ensemble_metadata['weights'] = {k: 1/n_models for k in trained_models.keys()}
        
        ensemble_path = os.path.join(model_dir, 'ensemble_metadata.json')
        with open(ensemble_path, 'w') as f:
            json.dump(ensemble_metadata, f, indent=2)
        print(f"Saved ensemble metadata to {ensemble_path}")
    
    # Save SHAP explainer
    if shap_data and config['shap']['save_explainer']:
        shap_path = os.path.join(model_dir, 'shap_explainer.pkl')
        joblib.dump({
            'explainer': shap_data['explainer'],
            'feature_names': shap_data['feature_names']
        }, shap_path)
        print(f"Saved SHAP explainer to {shap_path}")
    
    # Generate report
    generate_report(all_metrics, best_model, best_model_name, shap_data, config, y_test, predictions)
    
    return trained_models, all_metrics, shap_data


def generate_report(all_metrics, best_model, best_model_name, shap_data, config, y_test, predictions):
    """Generate comprehensive performance report."""
    report_dir = config['output']['report_dir']
    os.makedirs(report_dir, exist_ok=True)
    
    report_path = os.path.join(report_dir, 'enhanced_model_performance.md')
    
    with open(report_path, 'w') as f:
        f.write("# Enhanced Model Performance Report\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Training Configuration\n\n")
        f.write(f"- **Class Balancing**: {config['class_balancing']['method']}\n")
        f.write(f"- **Hyperparameter Tuning**: {'Enabled' if config['hyperparameter_tuning']['enabled'] else 'Disabled'}\n")
        f.write(f"- **Ensemble**: {'Enabled' if config['ensemble']['enabled'] else 'Disabled'}\n")
        f.write(f"- **SHAP**: {'Enabled' if config['shap']['enabled'] else 'Disabled'}\n\n")
        
        f.write("## Model Comparison\n\n")
        f.write("| Model | ROC-AUC | F1-Score | Precision | Recall |\n")
        f.write("|-------|---------|----------|-----------|--------|\n")
        
        for metrics in all_metrics:
            f.write(f"| {metrics['model']} | {metrics['roc_auc']:.4f} | {metrics['f1']:.4f} | ")
            f.write(f"{metrics['precision']:.4f} | {metrics['recall']:.4f} |\n")
        
        f.write(f"\n## Best Model: {best_model_name}\n\n")
        best_metrics = next(m for m in all_metrics if m['model'] == best_model_name)
        f.write(f"- **ROC-AUC**: {best_metrics['roc_auc']:.4f}\n")
        f.write(f"- **F1-Score**: {best_metrics['f1']:.4f}\n")
        f.write(f"- **Precision**: {best_metrics['precision']:.4f}\n")
        f.write(f"- **Recall**: {best_metrics['recall']:.4f}\n\n")
        
        # Feature importance if available
        if hasattr(best_model.named_steps['classifier'], 'feature_importances_'):
            f.write("## Top 10 Feature Importances\n\n")
            
            try:
                preprocessor = best_model.named_steps['preprocessor']
                numeric_features = preprocessor.transformers_[0][2]
                categorical_features = preprocessor.transformers_[1][2]
                encoder = preprocessor.transformers_[1][1]['encoder']
                
                feature_names = list(numeric_features)
                if hasattr(encoder, 'get_feature_names_out'):
                    cat_names = encoder.get_feature_names_out(categorical_features)
                    feature_names.extend(cat_names)
                
                importances = best_model.named_steps['classifier'].feature_importances_
                feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(10)
                
                for feature, importance in feat_imp.items():
                    f.write(f"- **{feature}**: {importance:.6f}\n")
                
            except Exception as e:
                f.write(f"Could not extract feature importances: {e}\n")
        
        # SHAP summary if available
        if shap_data:
            f.write("\n## SHAP Analysis\n\n")
            f.write("SHAP values calculated successfully. Use `scripts/visualize_shap.py` to generate visualizations.\n")
    
    print(f"\nReport saved to {report_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train enhanced risk prediction models')
    parser.add_argument('--config', type=str, default='config/model_config.yaml',
                        help='Path to configuration file')
    parser.add_argument('--data', type=str,
                        default='data/processed/longterm_care_cleaned.csv',
                        help='Path to training data')
    
    args = parser.parse_args()
    
    # Construct full paths
    base_dir = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject'
    config_path = os.path.join(base_dir, args.config)
    data_path = os.path.join(base_dir, args.data)
    
    print("="*60)
    print("Enhanced Model Training")
    print("="*60)
    print(f"Config: {config_path}")
    print(f"Data: {data_path}")
    print("="*60)
    
    trained_models, metrics, shap_data = train_enhanced_models(data_path, config_path)
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
