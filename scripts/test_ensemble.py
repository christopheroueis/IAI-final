"""
Test ensemble model API integration.
"""

import sys
import os
sys.path.append('/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject/backend')

from model import RiskModel
import pandas as pd


def test_single_model():
    """Test single model (backward compatibility)."""
    print("="*80)
    print("Testing Single Model Mode (Backward Compatibility)")
    print("="*80)
    
    model = RiskModel(
        model_path='models/risk_model.pkl',
        use_ensemble=False
    )
    
    # Test input
    test_input = {
        'TOT_LIC_BEDS': 120,
        'PRDHR_RN_Per_Day': 0.8,
        'PRDHR_NA_Per_Day': 2.5,
        'Net_Income_Margin': -0.05
    }
    
    result = model.predict(test_input)
    
    print(f"\nRisk Score: {result.get('risk_score', 'N/A'):.4f}")
    print(f"Risk Level: {result.get('risk_level', 'N/A')}")
    print(f"\nTop Risk Drivers:")
    for i, driver in enumerate(result.get('top_risk_drivers', [])[:3], 1):
        print(f"  {i}. {driver.get('feature', 'N/A')}: {driver.get('contribution', 0):.2f}")
    
    return result


def test_ensemble_model():
    """Test ensemble model."""
    print("\n" + "="*80)
    print("Testing Ensemble Model Mode")
    print("="*80)
    
    model = RiskModel(
        model_path='models/risk_model_enhanced.pkl',
        use_ensemble=True
    )
    
    # Test input
    test_input = {
        'TOT_LIC_BEDS': 120,
        'PRDHR_RN_Per_Day': 0.8,
        'PRDHR_NA_Per_Day': 2.5,
        'Net_Income_Margin': -0.05
    }
    
    result = model.predict(test_input)
    
    print(f"\nEnsemble Risk Score: {result.get('risk_score', 'N/A'):.4f}" if isinstance(result.get('risk_score'), (int, float)) else f"\nEnsemble Risk Score: {result.get('risk_score', 'N/A')}")
    print(f"Risk Level: {result.get('risk_level', 'N/A')}")
    confidence = result.get('confidence', 'N/A')
    if isinstance(confidence, (int, float)):
        print(f"Confidence: {confidence:.4f}")
    else:
        print(f"Confidence: {confidence}")
    print(f"Model Agreement: {result.get('model_agreement', 'N/A')}")
    
    if 'individual_models' in result:
        print(f"\nIndividual Model Predictions:")
        for model_name, prob in result['individual_models'].items():
            print(f"  {model_name}: {prob:.4f}")
    
    print(f"\nTop Risk Drivers:")
    for i, driver in enumerate(result.get('top_risk_drivers', [])[:3], 1):
        feature = driver.get('feature', 'N/A')
        if 'shap_value' in driver:
            impact = driver.get('impact', 'N/A')
            print(f"  {i}. {feature} ({impact})")
        else:
            contribution = driver.get('contribution', 0)
            print(f"  {i}. {feature}: {contribution:.2f}")
    
    print(f"\nExplanation Type: {result.get('explanation_type', 'N/A')}")
    print(f"Model Type: {result.get('model_type', 'N/A')}")
    
    return result


def test_different_inputs():
    """Test ensemble with different input scenarios."""
    print("\n" + "="*80)
    print("Testing Multiple Input Scenarios")
    print("="*80)
    
    model = RiskModel(
        model_path='models/risk_model_enhanced.pkl',
        use_ensemble=True
    )
    
    scenarios = [
        {
            'name': 'Low Risk Facility',
            'data': {
                'TOT_LIC_BEDS': 100,
                'PRDHR_RN_Per_Day': 1.5,
                'PRDHR_NA_Per_Day': 4.0,
                'Net_Income_Margin': 0.10
            }
        },
        {
            'name': 'High Risk Facility',
            'data': {
                'TOT_LIC_BEDS': 200,
                'PRDHR_RN_Per_Day': 0.5,
                'PRDHR_NA_Per_Day': 1.5,
                'Net_Income_Margin': -0.15
            }
        },
        {
            'name': 'Medium Risk Facility',
            'data': {
                'TOT_LIC_BEDS': 150,
                'PRDHR_RN_Per_Day': 1.0,
                'PRDHR_NA_Per_Day': 3.0,
                'Net_Income_Margin': 0.02
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print("-" * 40)
        result = model.predict(scenario['data'])
        print(f"  Risk Score: {result.get('risk_score', 'N/A'):.4f}")
        print(f"  Risk Level: {result.get('risk_level', 'N/A')}")
        print(f"  Confidence: {result.get('confidence', 'N/A'):.4f}")
        print(f"  Agreement: {result.get('model_agreement', 'N/A')}")


if __name__ == "__main__":
    os.chdir('/Users/macintoshhd/Desktop/95891 - Intro to AI/Final Project/FinalProject')
    
    # Test single model
    single_result = test_single_model()
    
    # Test ensemble model
    ensemble_result = test_ensemble_model()
    
    # Test different scenarios
    test_different_inputs()
    
    print("\n" + "="*80)
    print("✓ All tests completed successfully!")
    print("="*80)
