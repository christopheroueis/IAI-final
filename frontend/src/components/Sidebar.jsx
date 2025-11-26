import React from 'react';

const Sidebar = ({ inputs, setInputs, onPredict }) => {
    const handleChange = (e) => {
        const { name, value } = e.target;
        setInputs(prev => ({ ...prev, [name]: value }));
    };

    const handleSliderChange = (name, value) => {
        setInputs(prev => ({ ...prev, [name]: value }));
    };

    return (
        <aside className="w-96 bg-white border-r border-slate-200 h-[calc(100vh-64px)] overflow-y-auto flex flex-col shadow-[4px_0_24px_rgba(0,0,0,0.02)] z-10">
            <div className="p-6 flex-1">
                <div className="flex items-center gap-2 mb-8">
                    <div className="h-8 w-1 bg-primary rounded-full"></div>
                    <h3 className="text-lg font-bold text-slate-800">Facility Parameters</h3>
                </div>

                <div className="space-y-8">
                    {/* Location */}
                    <div className="space-y-3">
                        <label className="block text-sm font-semibold text-slate-700">Location (HSA)</label>
                        <div className="relative">
                            <select
                                name="HSA"
                                value={inputs.HSA || ''}
                                onChange={handleChange}
                                className="w-full appearance-none bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all outline-none cursor-pointer hover:bg-slate-100"
                            >
                                <option value="">Select Area</option>
                                <option value="11 - Los Angeles">11 - Los Angeles</option>
                                <option value="05 - East Bay">05 - East Bay</option>
                                <option value="14 - San Diego/Imperial">14 - San Diego/Imperial</option>
                                <option value="Other">Other</option>
                            </select>
                            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    {/* Staffing Section */}
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
                            <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Staffing Levels</span>
                        </div>

                        {/* RN Hours */}
                        <div>
                            <div className="flex justify-between items-center mb-3">
                                <label className="text-sm font-medium text-slate-700">RN Hours / Patient Day</label>
                                <span className="text-sm font-bold text-primary bg-primary/10 px-2 py-1 rounded-md min-w-[3rem] text-center">
                                    {inputs.PRDHR_RN_Per_Day || 0}
                                </span>
                            </div>
                            <input
                                type="range"
                                min="0"
                                max="2"
                                step="0.01"
                                value={inputs.PRDHR_RN_Per_Day || 0}
                                onChange={(e) => handleSliderChange('PRDHR_RN_Per_Day', parseFloat(e.target.value))}
                                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary hover:accent-primary/80 transition-all"
                            />
                        </div>

                        {/* CNA Hours */}
                        <div>
                            <div className="flex justify-between items-center mb-3">
                                <label className="text-sm font-medium text-slate-700">CNA Hours / Patient Day</label>
                                <span className="text-sm font-bold text-primary bg-primary/10 px-2 py-1 rounded-md min-w-[3rem] text-center">
                                    {inputs.PRDHR_NA_Per_Day || 0}
                                </span>
                            </div>
                            <input
                                type="range"
                                min="0"
                                max="5"
                                step="0.01"
                                value={inputs.PRDHR_NA_Per_Day || 0}
                                onChange={(e) => handleSliderChange('PRDHR_NA_Per_Day', parseFloat(e.target.value))}
                                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary hover:accent-primary/80 transition-all"
                            />
                        </div>
                    </div>

                    {/* Financials Section */}
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
                            <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Financial Health</span>
                        </div>

                        <div>
                            <div className="flex justify-between items-center mb-3">
                                <label className="text-sm font-medium text-slate-700">Net Income Margin</label>
                                <span className={`text-sm font-bold px-2 py-1 rounded-md min-w-[4rem] text-center ${(inputs.Net_Income_Margin || 0) >= 0
                                        ? 'text-emerald-700 bg-emerald-100'
                                        : 'text-rose-700 bg-rose-100'
                                    }`}>
                                    {(inputs.Net_Income_Margin * 100).toFixed(1)}%
                                </span>
                            </div>
                            <input
                                type="range"
                                min="-0.5"
                                max="0.5"
                                step="0.01"
                                value={inputs.Net_Income_Margin || 0}
                                onChange={(e) => handleSliderChange('Net_Income_Margin', parseFloat(e.target.value))}
                                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary hover:accent-primary/80 transition-all"
                            />
                            <div className="flex justify-between text-[10px] font-medium text-slate-400 mt-2 uppercase tracking-wide">
                                <span>-50% (Loss)</span>
                                <span>0%</span>
                                <span>+50% (Profit)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="p-6 border-t border-slate-200 bg-slate-50">
                <button
                    onClick={onPredict}
                    className="w-full bg-primary text-white py-4 rounded-xl font-bold hover:bg-primary/90 transition-all shadow-lg shadow-primary/20 active:scale-[0.98] flex items-center justify-center gap-2"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    Calculate Risk Profile
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;
