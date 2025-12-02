import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function HospitalInput() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        OUTPATIENT_AVG_PER_SURGERY: 180,
        TOT_ALOS_PY: 4.5,
        PEDIATRIC_ALOS_PY: 3.2,
        NET_INCOME: 500000,
        EMS_VISITS_CRITICAL_ADMITTED: 150,
        EMS_VISITS_CRITICAL_TOT: 200,
        CONST_PROG: 100000,
        GR_IP_MCAR_TR: 2000000,
        INC_INVEST: 50000,
        GR_OP_THRD_TR: 1500000
    });

    // Feature metadata for display
    const featureMetadata = {
        OUTPATIENT_AVG_PER_SURGERY: {
            label: 'Outpatient Average Per Surgery (minutes)',
            type: 'number',
            min: 30,
            max: 600,
            step: 5,
            description: 'Average time per outpatient surgical procedure'
        },
        TOT_ALOS_PY: {
            label: 'Total Average Length of Stay - Previous Year (days)',
            type: 'number',
            min: 1,
            max: 30,
            step: 0.1,
            description: 'Average patient length of stay from previous year'
        },
        PEDIATRIC_ALOS_PY: {
            label: 'Pediatric Average Length of Stay - Previous Year (days)',
            type: 'number',
            min: 1,
            max: 20,
            step: 0.1,
            description: 'Average pediatric patient length of stay from previous year'
        },
        NET_INCOME: {
            label: 'Net Income ($)',
            type: 'number',
            min: -5000000,
            max: 10000000,
            step: 10000,
            description: 'Total net income (profit or loss)'
        },
        EMS_VISITS_CRITICAL_ADMITTED: {
            label: 'Critical EMS Visits Admitted',
            type: 'number',
            min: 0,
            max: 1000,
            step: 1,
            description: 'Number of critical emergency visits resulting in admission'
        },
        EMS_VISITS_CRITICAL_TOT: {
            label: 'Total Critical EMS Visits',
            type: 'number',
            min: 0,
            max: 2000,
            step: 1,
            description: 'Total number of critical emergency medical service visits'
        },
        CONST_PROG: {
            label: 'Construction in Progress ($)',
            type: 'number',
            min: 0,
            max: 10000000,
            step: 10000,
            description: 'Value of ongoing construction projects'
        },
        GR_IP_MCAR_TR: {
            label: 'Gross Inpatient Medicare Revenue ($)',
            type: 'number',
            min: 0,
            max: 20000000,
            step: 10000,
            description: 'Gross revenue from Medicare inpatient services'
        },
        INC_INVEST: {
            label: 'Investment Income ($)',
            type: 'number',
            min: 0,
            max: 1000000,
            step: 1000,
            description: 'Income generated from investments'
        },
        GR_OP_THRD_TR: {
            label: 'Gross Outpatient Third Party Revenue ($)',
            type: 'number',
            min: 0,
            max: 20000000,
            step: 10000,
            description: 'Gross revenue from third-party outpatient services'
        }
    };

    const handleInputChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Navigate to loading page immediately
        navigate('/loading');

        const startTime = Date.now();

        try {
            const response = await axios.post(`${API_URL}/predict/hospital`, {
                features: formData
            });

            console.log('Hospital prediction response:', response.data);

            // Ensure loading page shows for at least 7 seconds
            const elapsedTime = Date.now() - startTime;
            const minLoadingTime = 7000;
            const remainingTime = Math.max(0, minLoadingTime - elapsedTime);

            setTimeout(() => {
                navigate('/results', {
                    state: {
                        ...response.data,
                        facilityType: 'hospital'
                    }
                });
            }, remainingTime);
        } catch (error) {
            console.error('Error calculating risk:', error);
            console.error('Error details:', error.response?.data);
            alert(`Failed to calculate risk: ${error.response?.data?.detail || error.message}`);
            navigate('/input/hospital'); // Go back to input on error
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-12 px-4">
            <div className="max-w-4xl mx-auto">
                <div className="bg-white rounded-2xl shadow-lg p-8 border border-slate-200">
                    {/* Header */}
                    <div className="mb-8">
                        <h2 className="text-3xl font-bold text-slate-900 mb-2">Hospital Risk Assessment</h2>
                        <p className="text-slate-600">
                            Enter operational data for the top 10 most important risk factors
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {Object.entries(featureMetadata).map(([field, meta]) => (
                            <div key={field} className="space-y-2">
                                <label className="block">
                                    <div className="flex items-start justify-between mb-2">
                                        <span className="text-sm font-semibold text-slate-700">{meta.label}</span>
                                        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                                            High Impact
                                        </span>
                                    </div>
                                    <p className="text-xs text-slate-500 mb-2">{meta.description}</p>

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
                                </label>
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
        </div>
    );
}

export default HospitalInput;
