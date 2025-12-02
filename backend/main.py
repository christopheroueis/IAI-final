from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
from model import RiskModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CareEnforced AI API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Models
# Path relative to where main.py is run (usually from backend dir)
MODEL_PATH = "../models/risk_model.pkl"
HOSPITAL_MODEL_PATH = "../models/hospital_lightgbm_model.pkl"

risk_model = RiskModel(MODEL_PATH)

# Load hospital model
try:
    import pickle
    import json
    with open(HOSPITAL_MODEL_PATH, 'rb') as f:
        hospital_model = pickle.load(f)
    with open("../models/hospital_model_metadata.json", 'r') as f:
        hospital_metadata = json.load(f)
    print("Hospital model loaded successfully")
except Exception as e:
    print(f"Warning: Could not load hospital model: {e}")
    hospital_model = None
    hospital_metadata = None

class FacilityData(BaseModel):
    features: Dict[str, Any]

@app.get("/")
def read_root():
    return {"message": "CareEnforced AI API is running"}

@app.post("/predict")
def predict_risk(data: FacilityData):
    print(f"Received prediction request: {data.features}")
    result = risk_model.predict(data.features)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": risk_model.model is not None}

@app.get("/top-features")
def get_top_features():
    """Return metadata about top features for the frontend."""
    return {"top_features": risk_model.get_top_features_metadata()}

@app.post("/predict/hospital")
def predict_hospital_risk(data: FacilityData):
    """Predict risk for hospital facilities."""
    if hospital_model is None:
        raise HTTPException(status_code=503, detail="Hospital model not available")
    
    try:
        import pandas as pd
        import numpy as np
        
        # The model now expects only these 10 features
        expected_features = [
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
        
        # Create dataframe with the expected feature order
        input_data = {feat: data.features.get(feat, 0) for feat in expected_features}
        input_df = pd.DataFrame([input_data])
        
        print(f"Input data: {input_data}")
        
        # Make prediction
        prediction_proba = hospital_model.predict_proba(input_df)[0, 1]
        prediction = hospital_model.predict(input_df)[0]
        
        print(f"Prediction probability: {prediction_proba}")
        
        # Calculate SHAP values for feature importance
        try:
            import shap
            # Get scaled features
            X_scaled = hospital_model.named_steps['scaler'].transform(input_df)
            explainer = shap.TreeExplainer(hospital_model.named_steps['classifier'])
            shap_values = explainer.shap_values(X_scaled)
            
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # Positive class
            
            # Get top contributing features
            top_indices = np.argsort(np.abs(shap_values[0]))[-5:][::-1]
            feature_contributions = [
                {
                    "feature": expected_features[i],
                    "contribution": float(abs(shap_values[0][i])),
                    "impact": "increases" if shap_values[0][i] > 0 else "decreases"
                }
                for i in top_indices
            ]
        except Exception as e:
            print(f"SHAP calculation error: {e}")
            import traceback
            traceback.print_exc()
            feature_contributions = []
        
        # Format for results page
        top_risk_drivers = [
            {
                "feature": contrib["feature"],
                "contribution": contrib["contribution"]
            }
            for contrib in feature_contributions
        ]
        
        # Determine risk level
        if prediction_proba >= 0.7:
            risk_level = "High"
        elif prediction_proba >= 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            "risk_score": float(prediction_proba),
            "risk_level": risk_level,
            "top_risk_drivers": top_risk_drivers,
            "recommendations": []
        }
    except Exception as e:
        import traceback
        print(f"Hospital prediction error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/top-features/hospital")
def get_hospital_features():
    """Return metadata about top hospital features for the frontend."""
    if hospital_metadata is None:
        raise HTTPException(status_code=503, detail="Hospital metadata not available")
    return {"top_features": hospital_metadata.get("top_features", [])}
