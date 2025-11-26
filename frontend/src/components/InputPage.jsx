import React, { useState, useEffect } from 'react';
import CaliforniaMap from './CaliforniaMap';

function InputPage({ onCalculate, loading, topFeatures, initialData }) {
    const [formData, setFormData] = useState({
        HSA: '11 - Los Angeles',
        TOT_PAT_DAYS_FOR: 15000,
        HFPA: 500,
        DISCHARGES_7_MONTHS_AND_LT_1_YR: 50,
        DISCHARGES_3_MONTHS_AND_LT_7_MONTHS: 30,
        EXP_ADMN: 200000,
        SN_PAT_DAYS_FOR: 12000,
        PPE_BED: 15000,
        TOT_LIC_BEDS: 100,
        ...initialData
    });

    // Feature metadata for display
    const featureMetadata = {
        HSA: {
            label: 'Health Service Area',
            type: 'select',
            options: [
                '01 - Northern California',
                '02 - Golden Empire',
                '03 - North Bay',
                '04 - West Bay',
                '05 - East Bay',
                '06 - North San Joaquin',
                '07 - Santa Clara',
                '08 - Mid-Coast',
                '09 - Central',
                '10 - Santa Barbara/Ventura',
                '11 - Los Angeles',
                '12 - Orange County',
                '13 - Inland Empire',
                '14 - San Diego/Imperial'
            ],
            description: 'Geographic region of the facility'
        },
        TOT_PAT_DAYS_FOR: {
            label: 'Total Patient Days',
            type: 'number',
            min: 0,
            max: 50000,
            step: 100,
            description: 'Total patient days for the reporting period'
        },
        HFPA: {
            label: 'HFPA (Healthcare Facility Patient Assessment)',
            type: 'number',
            min: 0,
            max: 5000,
            step: 10,
            description: 'Healthcare facility patient-day assessment value'
        },
        DISCHARGES_7_MONTHS_AND_LT_1_YR: {
            label: 'Discharges (7-12 Months)',
            type: 'number',
            min: 0,
            max: 500,
            step: 1,
            description: 'Number of patient discharges between 7 and 12 months'
        },
        DISCHARGES_3_MONTHS_AND_LT_7_MONTHS: {
            label: 'Discharges (3-7 Months)',
            type: 'number',
            min: 0,
            max: 500,
            step: 1,
            description: 'Number of patient discharges between 3 and 7 months'
        },
        EXP_ADMN: {
            label: 'Administrative Expenses ($)',
            type: 'number',
            min: 0,
            max: 5000000,
            step: 1000,
            description: 'Total administrative expenses'
        },
        SN_PAT_DAYS_FOR: {
            label: 'Skilled Nursing Patient Days',
            type: 'number',
            min: 0,
            max: 40000,
            step: 100,
            description: 'Total skilled nursing patient days'
        },
        PPE_BED: {
            label: 'Property & Equipment per Bed ($)',
            type: 'number',
            min: 0,
            max: 100000,
            step: 100,
            description: 'Property and equipment value per licensed bed'
        },
        TOT_LIC_BEDS: {
            label: 'Total Licensed Beds',
            type: 'number',
            min: 1,
            max: 500,
            step: 1,
            description: 'Total number of licensed beds in facility'
        }
    };

    const handleInputChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onCalculate(formData);
    };

    return (
        <div className="max-w-4xl mx-auto px-6 py-8">
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-slate-200">
                {/* Header */}
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-slate-900 mb-2">Facility Parameters</h2>
                    <p className="text-slate-600">
                        Enter data for the top 10 most important risk factors identified by our AI model
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {Object.entries(featureMetadata).map(([field, meta]) => (
                        <div key={field} className="space-y-2">
                            {field === 'HSA' ? (
                                // Use California Map for HSA selection
                                <div className="space-y-2">
                                    <div className="flex items-start justify-between mb-2">
                                        <span className="text-sm font-semibold text-slate-700">{meta.label}</span>
                                        {topFeatures.find(f => f.name.includes(field.split('_')[0])) && (
                                            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                                                High Impact
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-xs text-slate-500 mb-2">{meta.description}</p>
                                    <CaliforniaMap
                                        selectedHSA={formData[field]}
                                        onSelectHSA={(hsa) => handleInputChange(field, hsa)}
                                    />
                                </div>
                            ) : (
                                // Regular input for other fields
                                <label className="block">
                                    <div className="flex items-start justify-between mb-2">
                                        <span className="text-sm font-semibold text-slate-700">{meta.label}</span>
                                        {topFeatures.find(f => f.name.includes(field.split('_')[0])) && (
                                            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                                                High Impact
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-xs text-slate-500 mb-2">{meta.description}</p>

                                    {meta.type === 'select' ? (
                                        <select
                                            value={formData[field]}
                                            onChange={(e) => handleInputChange(field, e.target.value)}
                                            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-slate-900"
                                        >
                                            {meta.options.map(option => (
                                                <option key={option} value={option}>{option}</option>
                                            ))}
                                        </select>
                                    ) : (
                                        <div className="space-y-2">
                                            <input
                                                type="number"
                                                value={formData[field]}
                                                onChange={(e) => handleInputChange(field, parseFloat(e.target.value) || 0)}
                                                min={meta.min}
                                                max={meta.max}
                                                step={meta.step}
                                                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-slate-900"
                                            />
                                            <input
                                                type="range"
                                                value={formData[field]}
                                                onChange={(e) => handleInputChange(field, parseFloat(e.target.value))}
                                                min={meta.min}
                                                max={meta.max}
                                                step={meta.step}
                                                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                                            />
                                            <div className="flex justify-between text-xs text-slate-500">
                                                <span>{meta.min?.toLocaleString()}</span>
                                                <span className="font-medium text-blue-600">{formData[field]?.toLocaleString()}</span>
                                                <span>{meta.max?.toLocaleString()}</span>
                                            </div>
                                        </div>
                                    )}
                                </label>
                            )}
                        </div>
                    ))}

                    {/* Submit Button */}
                    <div className="pt-6 border-t border-slate-200">
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold py-4 px-6 rounded-xl hover:shadow-lg hover:shadow-blue-500/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                    </svg>
                                    <span>Analyzing...</span>
                                </>
                            ) : (
                                <>
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                    </svg>
                                    <span>Calculate Risk Profile</span>
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default InputPage;
