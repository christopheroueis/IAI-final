import joblib
import pandas as pd
import os
import numpy as np
import json

try:
    from backend.ensemble_model import EnsembleRiskModel
    ENSEMBLE_AVAILABLE = True
except ImportError:
    ENSEMBLE_AVAILABLE = False

class RiskModel:
    def __init__(self, model_path, top_features_path=None, use_ensemble=None):
        self.model_path = model_path
        self.top_features_path = top_features_path or os.path.join(os.path.dirname(model_path), '../backend/top_features.json')
        
        # Determine ensemble mode from env var or parameter
        if use_ensemble is None:
            use_ensemble = os.getenv('USE_ENSEMBLE', 'false').lower() == 'true'
        
        self.use_ensemble = use_ensemble and ENSEMBLE_AVAILABLE
        self.model = None
        self.ensemble = None
        self.top_features = None
        
        self.load_model()
        self.load_top_features()

    def load_model(self):
        try:
            model_dir = os.path.dirname(self.model_path)
            
            # Try to load ensemble if enabled
            if self.use_ensemble:
                try:
                    self.ensemble = EnsembleRiskModel(model_dir)
                    print("Loaded ensemble model")
                    # Use first model for feature extraction
                    first_model = list(self.ensemble.models.values())[0]
                    preprocessor = first_model.named_steps['preprocessor']
                    self.numeric_features = preprocessor.transformers_[0][2]
                    self.categorical_features = preprocessor.transformers_[1][2]
                    return
                except Exception as e:
                    print(f"Could not load ensemble: {e}, falling back to single model")
                    self.use_ensemble = False
            
            # Load single model
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print(f"Model loaded from {self.model_path}")
                
                # Extract expected features
                try:
                    preprocessor = self.model.named_steps['preprocessor']
                    self.numeric_features = preprocessor.transformers_[0][2]
                    self.categorical_features = preprocessor.transformers_[1][2]
                    print(f"Expected features: {len(self.numeric_features)} numeric, {len(self.categorical_features)} categorical")
                except Exception as e:
                    print(f"Could not extract feature names: {e}")
                    self.numeric_features = []
                    self.categorical_features = []
            else:
                print(f"Model not found at {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")

    def load_top_features(self):
        """Load top features from JSON file."""
        try:
            if os.path.exists(self.top_features_path):
                with open(self.top_features_path, 'r') as f:
                    data = json.load(f)
                    self.top_features = data['top_features']
                print(f"Loaded {len(self.top_features)} top features")
            else:
                print(f"Top features file not found at {self.top_features_path}")
                self.top_features = []
        except Exception as e:
            print(f"Error loading top features: {e}")
            self.top_features = []

    def predict(self, input_data):
        """
        Predicts risk probability and returns top drivers and recommendations.
        input_data: dict or DataFrame containing feature values.
        """
        if not self.model and not self.ensemble:
            return {"error": "Model not loaded"}

        # Use ensemble if available
        if self.ensemble:
            return self._predict_ensemble(input_data)
        else:
            return self._predict_single(input_data)
    
    def _predict_ensemble(self, input_data):
        """Multi-model prediction with SHAP explanations."""
        try:
            df = pd.DataFrame([input_data])
            
            # Get ensemble predictions
            ensemble_result = self.ensemble.predict_ensemble(df)
            
            # Get SHAP-based explanations
            shap_contributions = self.ensemble.explain_prediction_shap(df)
            
            # Fall back to feature importance if SHAP fails
            if not shap_contributions:
                shap_contributions = self._calculate_feature_contributions(df)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(shap_contributions, input_data)
            
            return {
                'risk_score': float(ensemble_result['ensemble_risk_score']),
                'risk_level': self._get_risk_level(ensemble_result['ensemble_risk_score']),
                'confidence': ensemble_result['confidence'],
                'model_agreement': ensemble_result['agreement_level'],
                'individual_models': ensemble_result['individual_predictions'],
                'top_risk_drivers': shap_contributions[:5],
                'recommendations': recommendations,
                'explanation_type': 'shap' if shap_contributions else 'feature_importance',
                'model_type': 'ensemble'
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _predict_single(self, input_data):
        """Original single model prediction."""
        try:
            # Create DataFrame from input
            df = pd.DataFrame([input_data])
            
            # Ensure all expected columns exist
            if hasattr(self, 'numeric_features'):
                for col in self.numeric_features:
                    if col not in df.columns:
                        df[col] = np.nan  # Use NaN so SimpleImputer(strategy='mean') works

            if hasattr(self, 'categorical_features'):
                for col in self.categorical_features:
                    if col not in df.columns:
                        df[col] = np.nan # Use NaN so SimpleImputer(strategy='most_frequent') works
            
            # Get probability of class 1 (Penalized)
            probability = self.model.predict_proba(df)[0][1]
            
            # Calculate feature contributions
            feature_contributions = self._calculate_feature_contributions(df)
            
            # Generate dynamic recommendations
            recommendations = self._generate_recommendations(feature_contributions, input_data)
            
            return {
                "risk_score": float(probability),
                "risk_level": self._get_risk_level(probability),
                "top_risk_drivers": feature_contributions[:5],  # Top 5 contributors
                "recommendations": recommendations
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _calculate_feature_contributions(self, df):
        """
        Calculate feature contributions to the risk score.
        This is a simplified approach based on feature importance and deviation from mean.
        """
        try:
            if not self.top_features:
                return []
            
            contributions = []
            
            # Get all feature names after preprocessing
            preprocessor = self.model.named_steps['preprocessor']
            
            # Transform the input through preprocessor
            X_transformed = preprocessor.transform(df)
            
            # Get feature names
            numeric_features = list(self.numeric_features)
            categorical_features = self.categorical_features
            encoder = preprocessor.transformers_[1][1]['encoder']
            
            feature_names = numeric_features.copy()
            if hasattr(encoder, 'get_feature_names_out'):
                cat_feature_names = encoder.get_feature_names_out(categorical_features)
                feature_names.extend(cat_feature_names)
            
            # Calculate contributions for top features
            for top_feature in self.top_features:
                feature_name = top_feature['name']
                importance = top_feature['importance']
                
                # Find feature index
                if feature_name in feature_names:
                    idx = feature_names.index(feature_name)
                    # Get the transformed value
                    value = X_transformed[0, idx] if hasattr(X_transformed, 'toarray') else X_transformed[0][idx]
                    
                    # Contribution score (combining importance and value)
                    # Higher absolute value means more contribution
                    contribution_score = abs(float(value)) * importance * 100
                    
                    contributions.append({
                        "feature": self._format_feature_name(feature_name),
                        "contribution": contribution_score,
                        "importance": importance
                    })
            
            # Sort by contribution
            contributions.sort(key=lambda x: x['contribution'], reverse=True)
            
            return contributions
            
        except Exception as e:
            print(f"Error calculating contributions: {e}")
            return []

    def _format_feature_name(self, name):
        """Format feature names for display."""
        # Map common feature names to readable labels
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

    def _generate_recommendations(self, feature_contributions, input_data):
        """Generate dynamic recommendations based on feature contributions."""
        recommendations = []
        
        # Analyze top contributors
        if len(feature_contributions) > 0:
            top_contributor = feature_contributions[0]
            feature_name = top_contributor['feature']
            
            # Recommendation based on top risk driver
            if "RN Hours" in feature_name or "CNA Hours" in feature_name:
                # Check if staffing is low
                rn_hours = input_data.get('PRDHR_RN_Per_Day', 0)
                cna_hours = input_data.get('PRDHR_NA_Per_Day', 0)
                
                if rn_hours < 1.0:
                    recommendations.append({
                        "title": "Increase RN Staffing",
                        "description": f"Current RN hours ({rn_hours:.2f}/patient-day) are below recommended levels. Increasing to 1.5+ hours/patient-day could reduce risk by ~15%.",
                        "impact": "high"
                    })
                
                if cna_hours < 3.0:
                    recommendations.append({
                        "title": "Enhance CNA Coverage",
                        "description": f"Current CNA hours ({cna_hours:.2f}/patient-day) should be increased to 4+ hours/patient-day for optimal care quality.",
                        "impact": "high"
                    })
            
            elif "Net Income Margin" in feature_name or "Administrative Expenses" in feature_name:
                margin = input_data.get('Net_Income_Margin', 0)
                
                if margin < 0:
                    recommendations.append({
                        "title": "Financial Review Required",
                        "description": f"Negative profit margin ({margin*100:.1f}%) indicates financial stress. Consider cost optimization and revenue enhancement strategies.",
                        "impact": "high"
                    })
                else:
                    recommendations.append({
                        "title": "Monitor Financial Health",
                        "description": f"Current margin ({margin*100:.1f}%) is stable. Continue monitoring to maintain financial sustainability.",
                        "impact": "medium"
                    })
            
            elif "Los Angeles" in feature_name:
                recommendations.append({
                    "title": "Regional Compliance Focus",
                    "description": "Los Angeles region has heightened regulatory scrutiny. Ensure all compliance protocols are strictly followed.",
                    "impact": "high"
                })
            
            elif "Patient Days" in feature_name or "Licensed Beds" in feature_name:
                recommendations.append({
                    "title": "Optimize Capacity Utilization",
                    "description": "Review patient census patterns and bed utilization to ensure efficient operations and quality care delivery.",
                    "impact": "medium"
                })
        
        # Add general recommendations if none specific
        if len(recommendations) == 0:
            recommendations.append({
                "title": "Maintain Current Standards",
                "description": "Current facility parameters are within acceptable ranges. Continue monitoring key metrics.",
                "impact": "low"
            })
        
        # Always add staffing recommendation as fallback
        if not any("Staffing" in r['title'] for r in recommendations):
            recommendations.append({
                "title": "Staffing Optimization",
                "description": "Regularly review staffing ratios to ensure they meet or exceed regulatory requirements and patient care needs.",
                "impact": "medium"
            })
        
        return recommendations[:3]  # Return top 3 recommendations

    def _get_risk_level(self, probability):
        if probability < 0.3:
            return "Low"
        elif probability < 0.7:
            return "Medium"
        else:
            return "High"

    def get_top_features_metadata(self):
        """Return top features for frontend display."""
        return self.top_features if self.top_features else []
