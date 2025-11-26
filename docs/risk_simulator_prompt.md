# California Long-Term Care Facility Risk Score Simulator
## AI-Powered Enforcement Action Prediction System

---

## 🎯 Project Overview

Build an interactive web application that predicts the likelihood of California long-term care facilities receiving enforcement actions. The system enables facilities and the California Department of Public Health (CDPH) to perform "what-if" scenario analysis by modifying facility characteristics and observing real-time risk score changes.

---

## 📊 Dataset Information

**Primary Dataset:** `longterm_care_cleaned.csv`
- **248 features** covering facility identification, operations, financials, staffing, and utilization metrics
- **Target Variable:** `Penalized` (binary) - indicates whether a facility received an enforcement action
- **Years Covered:** 2022 and 2024
- **Facility Type:** California skilled nursing facilities and long-term care centers

### Key Feature Categories:
1. **Facility Characteristics** (ownership, certification, programs offered)
2. **Financial Metrics** (revenue, expenses, ratios, balance sheet items)
3. **Utilization Data** (occupancy rates, patient days, admissions/discharges)
4. **Staffing Information** (hours by role, turnover, temporary staff usage)
5. **Patient Demographics** (payer mix, diagnoses, length of stay distributions)
6. **Quality Indicators** (derived from operational and financial data)

---

## 🎓 Academic Context

**Course:** Introduction to AI
**Allowed Techniques:** Machine Learning, Deep Learning, NLP, Computer Vision, Reinforcement Learning, etc.
**Deployment Environment:** Google Colab (Antigravity environment)

---

## 🛠️ Technical Requirements

### Core Functionality
1. **Predictive Model Development**
   - Train classification model(s) to predict `Penalized` binary outcome
   - Achieve high performance with interpretability (consider ensemble methods, tree-based models, or neural networks)
   - Implement feature importance analysis to identify key risk drivers
   - Handle class imbalance if present (SMOTE, class weights, etc.)

2. **Interactive Web Application**
   - User-friendly interface for facility staff and CDPH regulators
   - Real-time risk score calculation as users modify features
   - Feature input validation and reasonable constraint enforcement
   - Visual risk indicators (gauges, color-coded alerts, probability percentages)

3. **Scenario Analysis Engine**
   - Allow users to modify multiple features simultaneously
   - Compare "current state" vs. "modified state" risk scores
   - Show which specific changes have the greatest impact on risk
   - Provide actionable recommendations based on model insights

4. **Explainability & Transparency**
   - SHAP values or LIME for individual prediction explanations
   - Feature contribution breakdowns (e.g., "Staffing accounts for 35% of risk")
   - Clear documentation of model limitations and confidence intervals

### Advanced Features (Optional Enhancement)
- **Clustering Analysis:** Group similar facilities to provide peer comparisons
- **Time Series Forecasting:** Predict risk trajectory over time if temporal data available
- **Natural Language Reports:** Generate automated compliance reports using LLMs
- **Batch Prediction Mode:** Allow CDPH to upload multiple facility profiles for risk assessment

---

## 🎨 Web Application Design

### User Personas
1. **Facility Administrator:** Wants to understand compliance risks and improve operations
2. **CDPH Regulator:** Needs to prioritize inspections and allocate resources efficiently

### Key UI Components
- **Dashboard:** Overview of facility profile and current risk score
- **Feature Modifier Panel:** Interactive sliders, dropdowns, and inputs for key features
- **Risk Visualization:** Dynamic charts showing risk breakdown by category
- **Comparison View:** Side-by-side current vs. modified scenario
- **Recommendation Engine:** AI-generated suggestions for risk reduction
- **Export Functionality:** Save reports as PDF or share links

### Technology Stack Suggestions
- **Backend:** Python (Flask/FastAPI) or run entirely in Colab
- **Frontend:** Streamlit (easiest), Gradio, or custom HTML/JS
- **ML Framework:** scikit-learn, XGBoost, TensorFlow/PyTorch
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Explainability:** SHAP, LIME, ELI5

---

## 📈 Evaluation Metrics

### Model Performance
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC and Precision-Recall curves
- Confusion matrix analysis
- Cross-validation scores (5-10 fold)

### Application Usability
- Response time for risk score updates (< 2 seconds ideal)
- UI intuitiveness (qualitative assessment)
- Feature importance alignment with domain knowledge

---

## 🚀 Deliverables

1. **Trained ML Model(s)** with serialized weights (.pkl, .h5, .pt files)
2. **Interactive Web Application** (hosted in Colab or deployed externally)
3. **Documentation:**
   - Model development notebook with EDA, feature engineering, training
   - User guide for the web application
   - Technical documentation explaining model architecture and decisions
4. **Presentation Materials:**
   - Demo video or live walkthrough
   - Slides explaining problem, approach, results, and impact

---

## 💡 Project Success Criteria

### Technical Excellence
- Model achieves strong predictive performance (AUC > 0.75)
- Code is well-documented and reproducible
- Application runs smoothly without errors

### Innovation & Impact
- Actionable insights that facilities can implement
- Regulatory efficiency improvements for CDPH
- Clear demonstration of AI value in healthcare compliance

### Presentation Quality
- Compelling narrative about elder care safety
- Professional UI/UX design
- Evidence of thorough testing with edge cases

---

## 🔍 Suggested Implementation Workflow

### Phase 1: Data Understanding & Preparation (Week 1)
- Load and explore `longterm_care_cleaned.csv`
- Conduct EDA: distributions, correlations, missing patterns
- Engineer derived features (ratios, trends, categorical encodings)
- Address class imbalance and split data (train/validation/test)

### Phase 2: Model Development (Week 2)
- Baseline models (Logistic Regression, Decision Trees)
- Advanced models (Random Forest, XGBoost, Neural Networks)
- Hyperparameter tuning and ensemble methods
- Model interpretation and feature importance analysis

### Phase 3: Application Development (Week 3)
- Build web interface with interactive components
- Integrate trained model for real-time predictions
- Implement scenario comparison logic
- Add explainability visualizations

### Phase 4: Testing & Refinement (Week 4)
- User testing with sample scenarios
- Performance optimization and bug fixes
- Documentation and presentation preparation
- Final demo and deployment

---

## 🎁 Bonus Ideas to Stand Out

1. **Regulatory Compliance Assistant:** LLM-powered chatbot that answers facility questions about compliance
2. **Peer Benchmarking:** Show how a facility compares to similar facilities in their county/region
3. **Risk Trajectory Visualization:** Animated timeline showing how risk evolves with proposed changes
4. **Mobile Responsive Design:** Ensure app works on tablets/phones for on-the-go access
5. **Automated Alerts:** Email notifications when a facility's risk crosses critical thresholds

---

## 📚 Key Questions to Answer Through Analysis

1. What are the top 5 predictors of enforcement actions?
2. Are for-profit facilities penalized more than non-profits?
3. Does staffing quality (turnover, temp usage) correlate with penalties?
4. Are financial distress indicators early warning signs?
5. Do certain patient populations (Alzheimer's, AIDS) correlate with higher risk?

---

## ⚠️ Important Considerations

- **Ethics:** Be mindful of bias - don't unfairly penalize facilities serving disadvantaged populations
- **Data Privacy:** No PHI or personally identifiable information in displays
- **Regulatory Alignment:** Ensure predictions align with actual CDPH priorities
- **Actionability:** Focus on modifiable features, not immutable characteristics (location, license date)

---

## 🏆 Making This Project Exceptional

To elevate beyond a standard ML classification project:
- **Tell a Story:** Frame this as protecting California's elderly population
- **Show Real Impact:** Calculate potential inspection hours saved or harm prevented
- **Professional Polish:** High-quality UI that looks like a real SaaS product
- **Domain Expertise:** Demonstrate understanding of healthcare regulations and challenges
- **Technical Depth:** Go beyond basic sklearn - show advanced techniques

---

**Good luck! This project has significant potential to demonstrate both technical skills and real-world impact. Focus on making it polished, interpretable, and genuinely useful for end users.**