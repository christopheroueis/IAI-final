import joblib
import pandas as pd
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    model = joblib.load('models/risk_model.pkl')
    print("Model loaded successfully.")
    
    preprocessor = model.named_steps['preprocessor']
    
    # Numeric Features
    numeric_features = preprocessor.transformers_[0][2]
    print(f"\nNumeric Features ({len(numeric_features)}):")
    print(numeric_features)
    
    # Categorical Features
    categorical_features = preprocessor.transformers_[1][2]
    print(f"\nCategorical Features ({len(categorical_features)}):")
    print(categorical_features)
    
    # Check categories for OneHotEncoder
    encoder = preprocessor.transformers_[1][1]['encoder']
    print("\nCategories per feature:")
    for i, feature in enumerate(categorical_features):
        print(f"\nFeature: {feature}")
        print(encoder.categories_[i][:10]) # Print first 10 categories
        
except Exception as e:
    print(f"Error: {e}")
