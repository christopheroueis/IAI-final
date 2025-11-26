import React, { useState, useEffect } from 'react';

const funFacts = [
    "California has over 1,200 skilled nursing facilities serving more than 100,000 residents.",
    "Random Forest models can analyze thousands of data points to predict enforcement risk patterns.",
    "Machine learning helps identify risk factors before they become compliance issues.",
    "The CDPH conducts routine inspections to ensure quality care standards are maintained.",
    "Data-driven insights help facilities improve patient safety and care quality.",
    "California's long-term care facilities employ over 200,000 healthcare professionals.",
    "Early risk detection can help facilities implement preventive measures proactively.",
    "AI models are trained on historical data spanning multiple years for accuracy.",
];

function LoadingPage() {
    const [progress, setProgress] = useState(0);
    const [currentFactIndex, setCurrentFactIndex] = useState(0);

    useEffect(() => {
        // Random initial fact
        setCurrentFactIndex(Math.floor(Math.random() * funFacts.length));

        // Progress animation
        const progressInterval = setInterval(() => {
            setProgress((prev) => {
                if (prev >= 100) {
                    clearInterval(progressInterval);
                    return 100;
                }
                // Slower progress for more engagement
                return prev + Math.random() * 3;
            });
        }, 100);

        // Change fact every 4 seconds
        const factInterval = setInterval(() => {
            setCurrentFactIndex((prev) => (prev + 1) % funFacts.length);
        }, 4000);

        return () => {
            clearInterval(progressInterval);
            clearInterval(factInterval);
        };
    }, []);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-6">
            <div className="max-w-2xl w-full">
                {/* Title */}
                <div className="text-center mb-12">
                    <div className="inline-block">
                        <div className="flex items-center justify-center gap-3 mb-4">
                            <div className="w-12 h-12 border-4 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                        </div>
                        <h2 className="text-3xl font-bold text-white mb-2">Analyzing Your Facility</h2>
                        <p className="text-blue-200">Our AI is processing your data...</p>
                    </div>
                </div>

                {/* Progress Bar */}
                <div className="mb-12">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium text-slate-300">Progress</span>
                        <span className="text-sm font-bold text-blue-400">{Math.floor(progress)}%</span>
                    </div>
                    <div className="w-full bg-slate-700/50 rounded-full h-4 overflow-hidden backdrop-blur-sm border border-slate-600">
                        <div
                            className="h-full bg-gradient-to-r from-blue-500 to-blue-400 rounded-full transition-all duration-300 ease-out relative overflow-hidden"
                            style={{ width: `${progress}%` }}
                        >
                            {/* Shimmer effect */}
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
                        </div>
                    </div>
                </div>

                {/* Fun Fact */}
                <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10">
                    <div className="flex items-start gap-4">
                        <div className="flex-shrink-0 text-3xl">💡</div>
                        <div>
                            <h3 className="text-lg font-semibold text-blue-300 mb-2">Did You Know?</h3>
                            <p className="text-slate-300 leading-relaxed">
                                {funFacts[currentFactIndex]}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Status Messages */}
                <div className="mt-8 space-y-2">
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></div>
                        <span>Running Random Forest model...</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                        <span>Analyzing feature contributions...</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                        <span>Generating AI recommendations...</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoadingPage;
