import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

function ResultsPage({ prediction, facilityData, onNewAnalysis, onBackToInput }) {
    const { risk_score, risk_level, top_risk_drivers = [], recommendations = [] } = prediction;

    // Risk level colors
    const getRiskColor = (level) => {
        switch (level) {
            case 'High': return { bg: 'bg-rose-100', text: 'text-rose-700', border: 'border-rose-300', gauge: '#ef4444' };
            case 'Medium': return { bg: 'bg-amber-100', text: 'text-amber-700', border: 'border-amber-300', gauge: '#f59e0b' };
            case 'Low': return { bg: 'bg-emerald-100', text: 'text-emerald-700', border: 'border-emerald-300', gauge: '#10b981' };
            default: return { bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-300', gauge: '#64748b' };
        }
    };

    const riskColors = getRiskColor(risk_level);
    const riskPercentage = (risk_score * 100).toFixed(1);

    // Gauge data
    const gaugeData = [
        { name: 'Risk', value: risk_score * 100 },
        { name: 'Safe', value: (1 - risk_score) * 100 }
    ];

    // Impact colors for recommendations
    const getImpactBadge = (impact) => {
        switch (impact) {
            case 'high': return 'bg-rose-100 text-rose-700 border-rose-300';
            case 'medium': return 'bg-amber-100 text-amber-700 border-amber-300';
            case 'low': return 'bg-emerald-100 text-emerald-700 border-emerald-300';
            default: return 'bg-slate-100 text-slate-700 border-slate-300';
        }
    };

    const handleExportPDF = async () => {
        const content = document.getElementById('results-content');
        if (!content) return;

        try {
            // Capture the content as canvas
            const canvas = await html2canvas(content, {
                scale: 2,
                useCORS: true,
                logging: false,
                backgroundColor: '#f8fafc'
            });

            const imgData = canvas.toDataURL('image/png');
            const pdf = new jsPDF('p', 'mm', 'a4');

            const imgWidth = 210; // A4 width in mm
            const pageHeight = 297; // A4 height in mm
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            let heightLeft = imgHeight;
            let position = 0;

            // Add first page
            pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;

            // Add additional pages if content is longer
            while (heightLeft > 0) {
                position = heightLeft - imgHeight;
                pdf.addPage();
                pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;
            }

            // Generate filename with current date
            const date = new Date().toISOString().split('T')[0];
            pdf.save(`CareEnforced_Risk_Report_${date}.pdf`);
        } catch (error) {
            console.error('Error generating PDF:', error);
            alert('Failed to generate PDF. Please try again.');
        }
    };

    return (
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
                                <p className="text-sm text-slate-600">Step 2: Analysis Results</p>
                            </div>
                        </div>

                        <div className="flex gap-2">
                            <button
                                onClick={onBackToInput}
                                className="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
                            >
                                ← Back to Edit
                            </button>
                            <button
                                onClick={onNewAnalysis}
                                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
                            >
                                New Analysis
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            <div id="results-content" className="max-w-7xl mx-auto px-6 py-8">
                {/* Risk Score Card */}
                <div className="bg-white rounded-2xl shadow-lg p-8 mb-6 border border-slate-200">
                    <h2 className="text-2xl font-bold text-slate-900 mb-6">Predicted Risk Score</h2>

                    <div className="grid md:grid-cols-2 gap-8 items-center">
                        {/* Gauge Chart */}
                        <div className="flex flex-col items-center">
                            <ResponsiveContainer width="100%" height={250}>
                                <PieChart>
                                    <Pie
                                        data={gaugeData}
                                        cx="50%"
                                        cy="50%"
                                        startAngle={180}
                                        endAngle={0}
                                        innerRadius={80}
                                        outerRadius={120}
                                        paddingAngle={0}
                                        dataKey="value"
                                    >
                                        <Cell fill={riskColors.gauge} />
                                        <Cell fill="#e2e8f0" />
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                            <div className="text-center -mt-20">
                                <div className="text-5xl font-bold text-slate-900">{riskPercentage}%</div>
                                <div className={`inline-block mt-2 px-4 py-2 rounded-full border-2 ${riskColors.bg} ${riskColors.text} ${riskColors.border} font-semibold uppercase text-sm tracking-wide`}>
                                    {risk_level} Risk
                                </div>
                            </div>
                        </div>

                        {/* Description */}
                        <div className="space-y-4">
                            <p className="text-slate-700 leading-relaxed">
                                Based on the facility parameters you provided, this facility has a <strong>{risk_level.toLowerCase()}</strong> probability
                                ({riskPercentage}%) of enforcement action.
                            </p>
                            <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                                <h3 className="font-semibold text-slate-900 mb-2">What this means:</h3>
                                <p className="text-sm text-slate-600">
                                    {risk_level === 'High' && 'This facility should prioritize immediate compliance improvements and closely monitor all risk factors.'}
                                    {risk_level === 'Medium' && 'This facility should address identified risk factors proactively to prevent escalation.'}
                                    {risk_level === 'Low' && 'This facility maintains good compliance standards. Continue monitoring to sustain performance.'}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                    {/* Top Risk Drivers */}
                    <div className="bg-white rounded-2xl shadow-lg p-8 border border-slate-200">
                        <div className="flex items-center gap-2 mb-6">
                            <svg className="w-6 h-6 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                            </svg>
                            <h2 className="text-xl font-bold text-slate-900">Top Risk Drivers</h2>
                        </div>

                        {top_risk_drivers && top_risk_drivers.length > 0 ? (
                            <div className="space-y-4">
                                {top_risk_drivers.map((driver, idx) => {
                                    const maxContribution = Math.max(...top_risk_drivers.map(d => d.contribution));
                                    const percentage = (driver.contribution / maxContribution) * 100;

                                    return (
                                        <div key={idx} className="space-y-1">
                                            <div className="flex justify-between items-baseline">
                                                <span className="text-sm font-medium text-slate-700">{driver.feature}</span>
                                                <span className="text-xs text-slate-500">
                                                    {driver.contribution.toFixed(2)}
                                                </span>
                                            </div>
                                            <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-gradient-to-r from-rose-500 to-rose-600 rounded-full transition-all duration-500"
                                                    style={{ width: `${percentage}%` }}
                                                />
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <div className="text-center py-8 text-slate-500">
                                <p>No risk drivers identified</p>
                            </div>
                        )}
                    </div>

                    {/* AI Recommendations */}
                    <div className="bg-white rounded-2xl shadow-lg p-8 border border-slate-200">
                        <div className="flex items-center gap-2 mb-6">
                            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                            <h2 className="text-xl font-bold text-slate-900">AI Recommendations</h2>
                        </div>

                        <div className="space-y-4">
                            {recommendations && recommendations.length > 0 ? (
                                recommendations.map((rec, idx) => (
                                    <div key={idx} className="bg-slate-50 rounded-xl p-4 border border-slate-200 hover:shadow-md transition-shadow">
                                        <div className="flex items-start justify-between mb-2">
                                            <h3 className="font-semibold text-slate-900">{rec.title}</h3>
                                            <span className={`text-xs px-2 py-1 rounded-full border ${getImpactBadge(rec.impact)} font-medium uppercase`}>
                                                {rec.impact}
                                            </span>
                                        </div>
                                        <p className="text-sm text-slate-600 leading-relaxed">{rec.description}</p>
                                    </div>
                                ))
                            ) : (
                                <div className="text-center py-8 text-slate-500">
                                    <p>No recommendations available</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Export Button */}
                <div className="mt-8 text-center">
                    <button
                        onClick={handleExportPDF}
                        className="inline-flex items-center gap-2 px-6 py-3 bg-white border-2 border-slate-300 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Export Report (PDF)
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ResultsPage;
