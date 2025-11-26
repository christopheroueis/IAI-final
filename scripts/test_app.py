import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    print(f"Testing Health Endpoint ({BASE_URL}/health)...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data}")
            if not data.get("model_loaded"):
                print("❌ Warning: Model is not loaded!")
                return False
            return True
        else:
            print(f"❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_prediction():
    print(f"\nTesting Prediction Endpoint ({BASE_URL}/predict)...")
    payload = {
        "features": {
            "HSA": "11 - Los Angeles",
            "PRDHR_RN_Per_Day": 0.5,
            "PRDHR_NA_Per_Day": 2.0,
            "Net_Income_Margin": 0.05
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data}")
            if "risk_score" in data and "risk_level" in data:
                return True
            else:
                print("❌ Invalid Response Structure")
                return False
        else:
            print(f"❌ Failed: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    print("Starting Backend Integration Tests...")
    health_ok = test_health()
    pred_ok = test_prediction()
    
    if health_ok and pred_ok:
        print("\n✅ All Backend Tests Passed!")
        sys.exit(0)
    else:
        print("\n❌ Some Tests Failed.")
        sys.exit(1)
