import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_dynamic_prediction():
    print(f"Testing Dynamic Predictions ({BASE_URL}/predict)...")
    
    # Case 1: Low Risk Inputs (High Staffing, High Profit)
    payload_low = {
        "features": {
            "HSA": "11 - Los Angeles",
            "PRDHR_RN_Per_Day": 2.0,  # High RN
            "PRDHR_NA_Per_Day": 5.0,  # High CNA
            "Net_Income_Margin": 0.5  # High Profit
        }
    }
    
    # Case 2: High Risk Inputs (Low Staffing, Low Profit)
    payload_high = {
        "features": {
            "HSA": "11 - Los Angeles",
            "PRDHR_RN_Per_Day": 0.0,  # Low RN
            "PRDHR_NA_Per_Day": 0.0,  # Low CNA
            "Net_Income_Margin": -0.5 # Low Profit
        }
    }
    
    try:
        resp_low = requests.post(f"{BASE_URL}/predict", json=payload_low)
        resp_high = requests.post(f"{BASE_URL}/predict", json=payload_high)
        
        if resp_low.status_code == 200 and resp_high.status_code == 200:
            data_low = resp_low.json()
            data_high = resp_high.json()
            
            score_low = data_low.get("risk_score")
            score_high = data_high.get("risk_score")
            
            print(f"Low Risk Input Score: {score_low}")
            print(f"High Risk Input Score: {score_high}")
            
            if score_low != score_high:
                print("✅ Success: Predictions are dynamic!")
                if score_high > score_low:
                     print("✅ Logic Check: High risk inputs produced higher score.")
                else:
                     print("⚠️ Warning: High risk inputs produced lower score (Model logic might be complex).")
                return True
            else:
                print("❌ Failed: Predictions are static (same score for different inputs).")
                return False
        else:
            print(f"❌ Failed: API Error. Status {resp_low.status_code} / {resp_high.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    if test_dynamic_prediction():
        sys.exit(0)
    else:
        sys.exit(1)
