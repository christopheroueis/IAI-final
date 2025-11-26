import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

const Dashboard = ({ prediction, loading }) => {
    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center h-full bg-slate-50/50">
                <div className="flex flex-col items-center gap-4">
                    <div className="animate-spin rounded-full h-12 w-12 border-4 border-slate-200 border-t-primary"></div>
                    <p className="text-slate-500 font-medium animate-pulse">Analyzing Facility Data...</p>
                </div>
            </div>
        );
    }

    if (!prediction) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center h-full text-slate-400 bg-slate-50/50 p-8">
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center max-w-md text-center">
                    <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-6">
                        <svg className="w-10 h-10 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    </div>
                    <h3 className="text-xl font-bold text-slate-800 mb-2">Ready to Analyze</h3>
                    <p className="text-slate-500 leading-relaxed">
                        Adjust the facility parameters in the sidebar and click <span className="font-semibold text-primary">Calculate Risk</span> to generate a comprehensive risk profile.
                    </p>
                </div>
            </div>
        );
    }

    const { risk_score, risk_level } = prediction;

    // Gauge Data
    const gaugeData = [
        { name: 'Score', value: risk_score * 100 },
        { name: 'Remaining', value: 100 - (risk_score * 100) }
    ];

    const COLORS = risk_level === 'High' ? ['#DC2626', '#F3F4F6'] :
        risk_level === 'Medium' ? ['#FDB813', '#F3F4F6'] :
            ['#10B981', '#F3F4F6'];

    return (
        <div className="flex-1 p-8 overflow-y-auto bg-slate-50/50">
            <div className="max-w-6xl mx-auto space-y-8">

                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Analysis Results</h2>
                        <p className="text-slate-500 mt-1">Generated on {new Date().toLocaleDateString()}</p>
                    </div>
                    <button className="text-sm font-medium text-primary hover:text-primary/80 flex items-center gap-2 bg-white px-4 py-2 rounded-lg border border-slate-200 shadow-sm hover:shadow transition-all">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        Export Report
                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

                    {/* Risk Score Card */}
                    <div className="bg-white rounded-2xl shadow-[0_2px_20px_rgba(0,0,0,0.04)] border border-slate-100 p-8 flex flex-col items-center relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-secondary"></div>
                        <h3 className="text-lg font-bold text-slate-700 mb-6 w-full flex items-center gap-2">
                            <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Predicted Risk Score
                        </h3>
                        <div className="h-64 w-full relative">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={gaugeData}
                                        cx="50%"
                                        cy="50%"
                                        startAngle={180}
                                        endAngle={0}
                                        innerRadius={85}
                                        outerRadius={120}
                                        paddingAngle={0}
                                        dataKey="value"
                                        stroke="none"
                                    >
                                        {gaugeData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                            <div className="absolute inset-0 flex flex-col items-center justify-center pt-16">
                                <span className="text-6xl font-extrabold text-slate-800 tracking-tight">{(risk_score * 100).toFixed(1)}%</span>
                                <span className={`text-sm font-bold mt-2 px-4 py-1.5 rounded-full uppercase tracking-wide ${risk_level === 'High' ? 'bg-rose-100 text-rose-700' :
                                    risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                                        'bg-emerald-100 text-emerald-700'
                                    }`}>
                                    {risk_level} Risk
                                </span>
                            </div>
                        </div>
                        <p className="text-center text-slate-500 mt-2 text-sm max-w-xs">
                            Probability of enforcement action based on current facility parameters.
                        </p>
                    </div>

                    {/* Top Drivers Card */}
                    <div className="bg-white rounded-2xl shadow-[0_2px_20px_rgba(0,0,0,0.04)] border border-slate-100 p-8 flex flex-col relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-slate-200 to-slate-300"></div>
                        <h3 className="text-lg font-bold text-slate-700 mb-6 flex items-center gap-2">
                            <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            Top Risk Drivers
                        </h3>
                        <div className="flex-1 flex flex-col items-center justify-center text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-200 p-6">
                            <svg className="w-12 h-12 mb-3 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                            </svg>
                            <p className="font-medium">Feature contribution analysis</p>
                            <p className="text-sm mt-1">Requires advanced model interpretation</p>
                        </div>
                    </div>

                </div>

                {/* Recommendations */}
                <div className="bg-white rounded-2xl shadow-[0_2px_20px_rgba(0,0,0,0.04)] border border-slate-100 p-8 relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 to-teal-500"></div>
                    <h3 className="text-lg font-bold text-slate-700 mb-6 flex items-center gap-2">
                        <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        AI Recommendations
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {risk_level === 'High' && (
                            <div className="flex items-start gap-4 p-5 bg-rose-50 rounded-xl border border-rose-100 hover:shadow-md transition-shadow">
                                <div className="bg-rose-100 p-2 rounded-lg text-rose-600">
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                    </svg>
                                </div>
                                <div>
                                    <h4 className="font-bold text-rose-800 mb-1">Immediate Action Required</h4>
                                    <p className="text-sm text-rose-700 leading-relaxed">Risk is critically high. Consider increasing RN staffing levels immediately to mitigate potential enforcement actions.</p>
                                </div>
                            </div>
                        )}
                        <div className="flex items-start gap-4 p-5 bg-blue-50 rounded-xl border border-blue-100 hover:shadow-md transition-shadow">
                            <div className="bg-blue-100 p-2 rounded-lg text-blue-600">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                            </div>
                            <div>
                                <h4 className="font-bold text-blue-800 mb-1">Staffing Optimization</h4>
                                <p className="text-sm text-blue-700 leading-relaxed">Increasing CNA hours by 0.5 per patient day is projected to reduce risk by ~12% based on historical data.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
