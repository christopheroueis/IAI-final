import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { checkHealth, predictRisk, getTopFeatures } from './api';
import WelcomePage from './components/WelcomePage';
import InputPage from './components/InputPage';
import HospitalInput from './pages/HospitalInput';
import FacilityTypeSelection from './pages/FacilityTypeSelection';
import ResultsPage from './components/ResultsPage';
import LoadingPage from './components/LoadingPage';
import './transitions.css';

// Wrapper component for InputPage to handle navigation
function LongTermInput() {
  const navigate = useNavigate();
  const [topFeatures, setTopFeatures] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getTopFeatures().then((data) => {
      setTopFeatures(data.top_features || []);
    });
  }, []);

  const handleCalculateRisk = async (data) => {
    setLoading(true);

    // Navigate to loading page immediately
    navigate('/loading');

    const startTime = Date.now();

    try {
      const result = await predictRisk(data);

      // Ensure loading page shows for at least 7 seconds
      const elapsedTime = Date.now() - startTime;
      const minLoadingTime = 7000;
      const remainingTime = Math.max(0, minLoadingTime - elapsedTime);

      setTimeout(() => {
        navigate('/results', { state: { ...result, facilityType: 'longterm' } });
      }, remainingTime);
    } catch (error) {
      console.error('Prediction error:', error);
      alert('Failed to calculate risk. Please try again.');
      navigate('/input/longterm');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-600 to-blue-500 p-2 rounded-lg">
                <svg className="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">CareEnforced AI</h1>
                <p className="text-sm text-slate-600">Long-Term Care Assessment</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <InputPage
        onCalculate={handleCalculateRisk}
        loading={loading}
        topFeatures={topFeatures}
      />
    </div>
  );
}

// Welcome page wrapper
function WelcomeWrapper() {
  const navigate = useNavigate();

  return <WelcomePage onStart={() => navigate('/select-type')} />;
}

// Results wrapper
function ResultsWrapper() {
  const navigate = useNavigate();
  const location = useLocation();
  const prediction = location.state || {};

  // If no prediction data, redirect to home
  if (!prediction.risk_score && !prediction.risk_category) {
    navigate('/');
    return null;
  }

  return (
    <ResultsPage
      prediction={prediction}
      facilityData={{}}
      onNewAnalysis={() => navigate('/select-type')}
      onBackToInput={() => navigate(-1)}
    />
  );
}

function App() {
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    checkHealth().then((data) => {
      setBackendStatus(data.status === 'healthy' ? 'online' : 'offline');
    });
  }, []);

  return (
    <BrowserRouter>
      <div className="page-transition">
        <Routes>
          <Route path="/" element={<WelcomeWrapper />} />
          <Route path="/select-type" element={<FacilityTypeSelection />} />
          <Route path="/input/longterm" element={<LongTermInput />} />
          <Route path="/input/hospital" element={<HospitalInput />} />
          <Route path="/loading" element={<LoadingPage />} />
          <Route path="/results" element={<ResultsWrapper />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;

