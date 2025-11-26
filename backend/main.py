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

# Initialize Model
# Path relative to where main.py is run (usually from backend dir)
MODEL_PATH = "../models/risk_model.pkl"
risk_model = RiskModel(MODEL_PATH)

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
