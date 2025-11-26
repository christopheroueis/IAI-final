"""
Ensemble Risk Model for multi-model predictions with confidence scoring.
"""

import joblib
import pandas as pd
import numpy as np
import os
import json


class EnsembleRiskModel:
    """Multi-model ensemble for robust risk prediction."""
    
    def __init__(self, model_dir):
        """
        Initialize ensemble model.
        
        Args:
            model_dir: Directory containing trained models and ensemble metadata
        """
        self.model_dir = model_dir
        self.models = {}
        self.weights = {}
        self.metadata = None
        self.shap_explainer = None
        
        self._load_models()
        self._load_metadata()
        self._load_shap()
    
    def _load_models(self):
        """Load all available trained models."""
        model_files = {
            'random_forest': 'random_forest_model.pkl',
            'xgboost': 'xgboost_model.pkl',
            'logistic_regression': 'logistic_regression_model.pkl'
        }
        
        for name, filename in model_files.items():
            model_path = os.path.join(self.model_dir, filename)
            if os.path.exists(model_path):
                try:
                    self.models[name] = joblib.load(model_path)
                    print(f"Loaded {name} model from {model_path}")
                except Exception as e:
                    print(f"Error loading {name}: {e}")
        
        if not self.models:
            raise ValueError(f"No models found in {self.model_dir}")
    
    def _load_metadata(self):
        """Load ensemble metadata including weights."""
        metadata_path = os.path.join(self.model_dir, 'ensemble_metadata.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
                self.weights = self.metadata.get('weights', {})
                print(f"Loaded ensemble metadata: {self.weights}")
        else:
            # Default to equal weights
            n_models = len(self.models)
            self.weights = {name: 1/n_models for name in self.models.keys()}
            print(f"No metadata found, using equal weights: {self.weights}")
    
    def _load_shap(self):
        """Load SHAP explainer if available."""
        shap_path = os.path.join(self.model_dir, 'shap_explainer.pkl')
        
        if os.path.exists(shap_path):
            try:
                shap_data = joblib.load(shap_path)
                self.shap_explainer = shap_data.get('explainer')
                self.feature_names = shap_data.get('feature_names', [])
                print("Loaded SHAP explainer")
            except Exception as e:
                print(f"Error loading SHAP explainer: {e}")
    
    def predict_ensemble(self, input_data):
        """
        Generate predictions from all models and combine.
        
        Args:
            input_data: DataFrame with input features
            
        Returns:
            dict with ensemble prediction, individual predictions, and confidence
        """
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        
        predictions = {}
        probabilities = {}
        
        # Get predictions from each model
        for name, model in self.models.items():
            try:
                prob = model.predict_proba(input_data)[0][1]
                pred = model.predict(input_data)[0]
                
                predictions[name] = int(pred)
                probabilities[name] = float(prob)
            except Exception as e:
                print(f"Error predicting with {name}: {e}")
                # Use neutral prediction if model fails
                predictions[name] = 0
                probabilities[name] = 0.5
        
        # Calculate weighted ensemble probability
        # Normalize model names to match metadata format
        model_name_map = {
            'random_forest': 'Random Forest',
            'xgboost': 'XGBoost',
            'logistic_regression': 'Logistic Regression'
        }
        
        ensemble_prob = sum(
            probabilities[name] * self.weights.get(model_name_map.get(name, name), 1/len(self.models))
            for name in self.models.keys()
        )
        
        # Calculate confidence (inverse of standard deviation)
        prob_values = list(probabilities.values())
        std_dev = np.std(prob_values)
        confidence = max(0, min(1, 1 - std_dev * 2))  # Scale to [0,1]
        
        # Determine agreement level
        agreement_level = self._get_agreement_level(probabilities)
        
        return {
            'ensemble_risk_score': float(ensemble_prob),
            'individual_predictions': probabilities,
            'confidence': float(confidence),
            'agreement_level': agreement_level,
            'model_weights': self.weights
        }
    
    def explain_prediction_shap(self, input_data):
        """
        Use SHAP for accurate feature contributions.
        
        Args:
            input_data: DataFrame with input features
            
        Returns:
            list of dicts with feature contributions
        """
        if not self.shap_explainer:
            return []
        
        try:
            import shap
            
            # Use best performing model (typically first in models dict)
            best_model_name = list(self.models.keys())[0]
            best_model = self.models[best_model_name]
            
            # Transform input
            preprocessor = best_model.named_steps['preprocessor']
            X_transformed = preprocessor.transform(input_data)
            
            # Calculate SHAP values
            shap_values = self.shap_explainer(X_transformed)
            
            # Handle different SHAP output formats
            if hasattr(shap_values, 'values'):
                shap_array = shap_values.values
            else:
                shap_array = shap_values
            
            # Handle multi-class output
            if len(shap_array.shape) > 2:
                shap_array = shap_array[:, :, 1]  # Get positive class
            
            # Get top contributors
            shap_importance = np.abs(shap_array[0])
            top_indices = np.argsort(shap_importance)[-10:][::-1]
            
            contributions = []
            for idx in top_indices:
                if idx < len(self.feature_names):
                    value = float(shap_array[0, idx]) if len(shap_array.shape) == 2 else float(shap_array[idx])
                    contributions.append({
                        'feature': self._format_feature_name(self.feature_names[idx]),
                        'shap_value': value,
                        'impact': 'increases_risk' if value > 0 else 'decreases_risk',
                        'importance': float(shap_importance[idx])
                    })
            
            return contributions
        
        except Exception as e:
            print(f"Error calculating SHAP values: {e}")
            return []
    
    def _format_feature_name(self, name):
        """Format feature names for display."""
        name_map = {
            "HSA_11 - Los Angeles": "Los Angeles Region",
            "TOT_PAT_DAYS_FOR": "Total Patient Days",
            "HFPA": "Healthcare Facility Patient-Day Assessment",
            "DISCHARGES_7_MONTHS_AND_LT_1_YR": "7-12 Month Discharges",
            "DISCHARGES_3_MONTHS_AND_LT_7_MONTHS": "3-7 Month Discharges",
            "COUNTY_x_Los Angeles": "Los Angeles County",
            "EXP_ADMN": "Administrative Expenses",
            "SN_PAT_DAYS_FOR": "Skilled Nursing Patient Days",
            "PPE_BED": "Property/Equipment per Bed",
            "TOT_LIC_BEDS": "Total Licensed Beds",
            "PRDHR_RN_Per_Day": "RN Hours per Patient Day",
            "PRDHR_NA_Per_Day": "CNA Hours per Patient Day",
            "Net_Income_Margin": "Net Income Margin"
        }
        
        return name_map.get(name, name)
    
    def _get_agreement_level(self, probabilities):
        """
        Classify model agreement.
        
        Args:
            probabilities: dict of model probabilities
            
        Returns:
            str: 'high', 'medium', or 'low'
        """
        values = list(probabilities.values())
        std = np.std(values)
        
        if std < 0.05:
            return 'high'  # All models strongly agree
        elif std < 0.15:
            return 'medium'  # Models mostly agree
        else:
            return 'low'  # Models disagree significantly


def load_ensemble_or_single(model_dir, use_ensemble=True):
    """
    Load ensemble model or fall back to single model.
    
    Args:
        model_dir: Directory containing models
        use_ensemble: Whether to try loading ensemble
        
    Returns:
        EnsembleRiskModel or single model
    """
    if use_ensemble:
        try:
            ensemble = EnsembleRiskModel(model_dir)
            print("Loaded ensemble model")
            return ensemble
        except Exception as e:
            print(f"Could not load ensemble ({e}), falling back to single model")
    
    # Fall back to single model
    single_model_path = os.path.join(model_dir, 'risk_model_enhanced.pkl')
    if not os.path.exists(single_model_path):
        single_model_path = os.path.join(model_dir, 'risk_model.pkl')
    
    if os.path.exists(single_model_path):
        print(f"Loaded single model from {single_model_path}")
        return joblib.load(single_model_path)
    else:
        raise FileNotFoundError(f"No model found in {model_dir}")
