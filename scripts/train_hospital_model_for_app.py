import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import pickle
import os

def train_simplified_hospital_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'processed', 'hospital_cleaned.csv')
    model_output = os.path.join(base_dir, 'models', 'hospital_lightgbm_model.pkl')
    metadata_output = os.path.join(base_dir, 'models', 'hospital_model_metadata.json')

    print("Loading data...")
    df = pd.read_csv(input_file, low_memory=False)

    # Define Target
    target_col = 'Penalized?'
    
    # ONLY use the top 10 features we're collecting from users
    selected_features = [
        'OUTPATIENT_AVG_PER_SURGERY',
        'TOT_ALOS_PY',
        'PEDIATRIC_ALOS_PY',
        'NET_INCOME',
        'EMS_VISITS_CRITICAL_ADMITTED',
        'EMS_VISITS_CRITICAL_TOT',
        'CONST_PROG',
        'GR_IP_MCAR_TR',
        'INC_INVEST',
        'GR_OP_THRD_TR'
    ]
    
    print(f"Using {len(selected_features)} features")
    
    # Keep only selected features and target
    available_features = [f for f in selected_features if f in df.columns]
    print(f"Available features: {len(available_features)}")
    
    X = df[available_features].copy()
    y = df[target_col].copy()
    
    # Fill any missing values in the selected features
    X = X.fillna(X.mean())
    
    print(f"Features shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train LightGBM with scaling
    print("Training LightGBM model...")
    model = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('classifier', lgb.LGBMClassifier(
            n_estimators=100,
            random_state=42,
            class_weight='balanced',
            verbose=-1,
            learning_rate=0.1,
            max_depth=5
        ))
    ])
    model.fit(X_train, y_train)
    
    # Evaluate
    from sklearn.metrics import accuracy_score, roc_auc_score
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print(f"\nModel Performance:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    # Get feature importance
    importances = model.named_steps['classifier'].feature_importances_
    for feat, imp in zip(available_features, importances):
        print(f"{feat}: {imp:.4f}")
    
    # Extract metadata
    print("\nExtracting feature metadata...")
    feature_metadata = []
    
    for feat_name in available_features:
        feature_metadata.append({
            'name': feat_name,
            'original_name': feat_name,
            'type': 'numeric',
            'min': float(df[feat_name].min()),
            'max': float(df[feat_name].max()),
            'mean': float(df[feat_name].mean())
        })
    
    # Save model
    print(f"Saving model to {model_output}...")
    with open(model_output, 'wb') as f:
        pickle.dump(model, f)
    
    # Save metadata
    print(f"Saving metadata to {metadata_output}...")
    metadata = {
        'top_features': feature_metadata,
        'feature_names': available_features
    }
    with open(metadata_output, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\nDone! Model uses only the 10 user-input features.")

if __name__ == "__main__":
    train_simplified_hospital_model()
