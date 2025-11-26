import React from 'react';

function WelcomePage({ onStart }) {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-6">
            <div className="max-w-2xl w-full text-center">
                {/* Title - with shimmer animation */}
                <h1 className="text-6xl font-bold mb-6 tracking-tight shimmer-text">
                    CareEnforced AI
                </h1>

                {/* Subtitle */}
                <p className="text-2xl text-blue-200 mb-3 font-medium">
                    California's Long-Term Care Facility Risk Assessment
                </p>

                <div className="flex items-center justify-center gap-2 mb-12">
                    <p className="text-slate-300">Powered by</p>
                    <img
                        src="/calhhs-logo.png"
                        alt="CalHHS"
                        className="h-8 inline-block bg-gray-200 px-3 py-1 rounded"
                    />
                </div>

                {/* Features */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
                    <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                        <div className="text-3xl mb-2">🎯</div>
                        <h3 className="font-semibold text-white mb-1">Accurate Predictions</h3>
                        <p className="text-sm text-slate-400">Random Forest ML model trained on 10,000+ facilities</p>
                    </div>

                    <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                        <div className="text-3xl mb-2">💡</div>
                        <h3 className="font-semibold text-white mb-1">AI Recommendations</h3>
                        <p className="text-sm text-slate-400">Dynamic insights based on your facility's data</p>
                    </div>

                    <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                        <div className="text-3xl mb-2">📊</div>
                        <h3 className="font-semibold text-white mb-1">Risk Drivers</h3>
                        <p className="text-sm text-slate-400">Identify top factors contributing to enforcement risk</p>
                    </div>
                </div>

                {/* Start Button */}
                <button
                    onClick={onStart}
                    className="group relative inline-flex items-center justify-center px-12 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-500 rounded-full shadow-lg hover:shadow-blue-500/50 hover:scale-105 transition-all duration-200"
                >
                    <span>Start Risk Assessment</span>
                    <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                </button>

                {/* Footer */}
                <p className="mt-12 text-sm text-slate-500">
                    California Health and Human Services Agency
                </p>
            </div>
        </div>
    );
}

export default WelcomePage;
