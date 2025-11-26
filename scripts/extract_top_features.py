import joblib
import json
import os

def extract_top_features(model_path, output_path, top_n=10):
    """Extract top N feature importances from the trained model."""
    try:
        # Load model
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        
        # Get the Random Forest classifier
        classifier = model.named_steps['classifier']
        
        # Check if it has feature_importances_
        if not hasattr(classifier, 'feature_importances_'):
            print("Error: Model does not have feature_importances_ attribute")
            return
        
        # Get preprocessor to extract feature names
        preprocessor = model.named_steps['preprocessor']
        
        # Numeric features
        numeric_features = preprocessor.transformers_[0][2]
        
        # Categorical features (need to get one-hot encoded names)
        categorical_features = preprocessor.transformers_[1][2]
        encoder = preprocessor.transformers_[1][1]['encoder']
        
        # Build full feature names list
        feature_names = list(numeric_features)
        
        # Add categorical feature names (one-hot encoded)
        if hasattr(encoder, 'get_feature_names_out'):
            cat_feature_names = encoder.get_feature_names_out(categorical_features)
            feature_names.extend(cat_feature_names)
        
        # Get feature importances
        importances = classifier.feature_importances_
        
        # Create list of (feature_name, importance) tuples
        feature_importance_pairs = list(zip(feature_names, importances))
        
        # Sort by importance (descending)
        feature_importance_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N
        top_features = feature_importance_pairs[:top_n]
        
        # Prepare output
        output_data = {
            "top_features": [
                {
                    "name": name,
                    "importance": float(importance),
                    "rank": i + 1
                }
                for i, (name, importance) in enumerate(top_features)
            ]
        }
        
        # Save to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\nTop {top_n} Features:")
        for i, (name, importance) in enumerate(top_features, 1):
            print(f"{i}. {name}: {importance:.6f}")
        
        print(f"\nSaved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    model_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/models/risk_model.pkl'
    output_path = '/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/backend/top_features.json'
    extract_top_features(model_path, output_path, top_n=10)
