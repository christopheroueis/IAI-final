import React, { useState, useEffect } from 'react';
import { checkHealth, predictRisk, getTopFeatures } from './api';
import WelcomePage from './components/WelcomePage';
import InputPage from './components/InputPage';
import ResultsPage from './components/ResultsPage';
import LoadingPage from './components/LoadingPage';

function App() {
  const [currentPage, setCurrentPage] = useState('welcome'); // 'welcome', 'input', 'loading', 'results'
  const [backendStatus, setBackendStatus] = useState('checking');
  const [topFeatures, setTopFeatures] = useState([]);
  const [facilityData, setFacilityData] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    // Check backend health on mount
    checkHealth().then((data) => {
      setBackendStatus(data.status === 'healthy' ? 'online' : 'offline');
    });

    // Load top features
    getTopFeatures().then((data) => {
      setTopFeatures(data.top_features || []);
    });
  }, []);

  const transitionToPage = (page, resetData = false) => {
    setIsAnimating(true);
    setTimeout(() => {
      setCurrentPage(page);
      if (resetData) {
        setFacilityData({});
        setPrediction(null);
      }
      setIsAnimating(false);
    }, 300);
  };

  const handleStartAssessment = () => {
    transitionToPage('input', true);
  };

  const handleCalculateRisk = async (data) => {
    setLoading(true);
    setFacilityData(data);

    // Transition to loading page first
    transitionToPage('loading');

    const startTime = Date.now();

    try {
      const result = await predictRisk(data);
      setPrediction(result);

      // Ensure loading page shows for at least 7 seconds
      const elapsedTime = Date.now() - startTime;
      const minLoadingTime = 7000; // 7 seconds
      const remainingTime = Math.max(0, minLoadingTime - elapsedTime);

      setTimeout(() => {
        transitionToPage('results');
      }, remainingTime);
    } catch (error) {
      console.error('Prediction error:', error);
      alert('Failed to calculate risk. Please try again.');
      transitionToPage('input');
    } finally {
      setLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    transitionToPage('input', true);
  };

  const handleBackToInput = () => {
    transitionToPage('input');
  };


  return (
    <div className={`${isAnimating ? 'page-exit-active' : 'page-enter-active'}`}>
      {currentPage === 'welcome' && (
        <WelcomePage onStart={handleStartAssessment} />
      )}

      {currentPage === 'input' && (
        <div className="min-h-screen bg-slate-50">
          {/* Header */}
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
                    <p className="text-sm text-slate-600">Step 1: Enter Facility Parameters</p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${backendStatus === 'online' ? 'bg-emerald-500' : 'bg-rose-500'}`}></div>
                  <span className="text-sm text-slate-600 font-medium">
                    {backendStatus === 'online' ? 'System Online' : 'System Offline'}
                  </span>
                </div>
              </div>
            </div>
          </header>

          <InputPage
            onCalculate={handleCalculateRisk}
            loading={loading}
            topFeatures={topFeatures}
            initialData={facilityData}
          />
        </div>
      )}

      {currentPage === 'loading' && (
        <LoadingPage />
      )}

      {currentPage === 'results' && prediction && (
        <ResultsPage
          prediction={prediction}
          facilityData={facilityData}
          onNewAnalysis={handleNewAnalysis}
          onBackToInput={handleBackToInput}
        />
      )}
    </div>
  );
}

export default App;
