import React, { useState, useMemo } from 'react';
import { geoPath, geoMercator } from 'd3-geo';
import { feature } from 'topojson-client';
import caCountiesTopo from '../data/ca-counties.json';

function CaliforniaMap({ selectedHSA, onSelectHSA }) {
    const [hoveredCounty, setHoveredCounty] = useState(null);

    // Complete mapping of all 58 California counties to HSA regions
    const countyToHSA = {
        // HSA 01 - Northern California
        'Shasta': '01 - Northern California',
        'Tehama': '01 - Northern California',
        'Butte': '01 - Northern California',
        'Glenn': '01 - Northern California',
        'Lassen': '01 - Northern California',
        'Modoc': '01 - Northern California',
        'Plumas': '01 - Northern California',
        'Siskiyou': '01 - Northern California',
        'Trinity': '01 - Northern California',
        'Colusa': '01 - Northern California',
        'Del Norte': '01 - Northern California',
        'Humboldt': '01 - Northern California',
        'Lake': '01 - Northern California',
        'Mendocino': '01 - Northern California',

        // HSA 02 - Golden Empire
        'Placer': '02 - Golden Empire',
        'El Dorado': '02 - Golden Empire',
        'Nevada': '02 - Golden Empire',
        'Sierra': '02 - Golden Empire',
        'Yuba': '02 - Golden Empire',
        'Sutter': '02 - Golden Empire',

        // HSA 03 - North Bay
        'Marin': '03 - North Bay',
        'Napa': '03 - North Bay',
        'Sonoma': '03 - North Bay',
        'Solano': '03 - North Bay',

        // HSA 04 - West Bay
        'San Francisco': '04 - West Bay',
        'San Mateo': '04 - West Bay',

        // HSA 05 - East Bay
        'Alameda': '05 - East Bay',
        'Contra Costa': '05 - East Bay',

        // HSA 06 - North San Joaquin
        'Sacramento': '06 - North San Joaquin',
        'San Joaquin': '06 - North San Joaquin',
        'Stanislaus': '06 - North San Joaquin',
        'Yolo': '06 - North San Joaquin',
        'Amador': '06 - North San Joaquin',
        'Calaveras': '06 - North San Joaquin',

        // HSA 07 - Santa Clara
        'Santa Clara': '07 - Santa Clara',

        // HSA 08 - Mid-Coast
        'Monterey': '08 - Mid-Coast',
        'San Luis Obispo': '08 - Mid-Coast',
        'Santa Cruz': '08 - Mid-Coast',
        'San Benito': '08 - Mid-Coast',

        // HSA 09 - Central
        'Fresno': '09 - Central',
        'Kern': '09 - Central',
        'Tulare': '09 - Central',
        'Kings': '09 - Central',
        'Madera': '09 - Central',
        'Merced': '09 - Central',
        'Mariposa': '09 - Central',
        'Tuolumne': '09 - Central',
        'Alpine': '09 - Central',
        'Mono': '09 - Central',
        'Inyo': '09 - Central',

        // HSA 10 - Santa Barbara/Ventura
        'Santa Barbara': '10 - Santa Barbara/Ventura',
        'Ventura': '10 - Santa Barbara/Ventura',

        // HSA 11 - Los Angeles
        'Los Angeles': '11 - Los Angeles',

        // HSA 12 - Orange County
        'Orange': '12 - Orange County',

        // HSA 13 - Inland Empire
        'Riverside': '13 - Inland Empire',
        'San Bernardino': '13 - Inland Empire',

        // HSA 14 - San Diego/Imperial
        'San Diego': '14 - San Diego/Imperial',
        'Imperial': '14 - San Diego/Imperial',
    };

    // Convert TopoJSON to GeoJSON and setup D3 projection
    const { geoData, pathGenerator } = useMemo(() => {
        // Convert TopoJSON to GeoJSON features
        const geoJson = feature(caCountiesTopo, caCountiesTopo.objects.subunits);

        // Create a projection for California
        // Using Mercator projection, centered on California
        const projection = geoMercator()
            .fitSize([400, 600], geoJson);

        // Create path generator
        const path = geoPath().projection(projection);

        return {
            geoData: geoJson,
            pathGenerator: path
        };
    }, []);

    const handleCountyClick = (countyName) => {
        const hsa = countyToHSA[countyName];
        if (hsa) {
            onSelectHSA(hsa);
        }
    };

    const isCountySelected = (countyName) => {
        return countyToHSA[countyName] === selectedHSA;
    };

    const getCountyFill = (countyName) => {
        if (isCountySelected(countyName)) {
            return '#3b82f6'; // Blue for selected
        }
        return '#e2e8f0'; // Light gray for unselected
    };

    return (
        <div className="w-full">
            <div className="bg-white rounded-xl border-2 border-slate-300 p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">Select County on Map</h3>

                {/* California County Map using D3 and TopoJSON */}
                <svg viewBox="0 0 400 600" className="w-full h-auto">
                    <g>
                        {geoData.features.map((countyFeature, idx) => {
                            const countyName = countyFeature.properties.name;
                            const pathData = pathGenerator(countyFeature);

                            return (
                                <path
                                    key={idx}
                                    d={pathData}
                                    fill={getCountyFill(countyName)}
                                    stroke="#64748b"
                                    strokeWidth="0.5"
                                    className="cursor-pointer hover:fill-blue-300 transition-colors"
                                    onClick={() => handleCountyClick(countyName)}
                                    onMouseEnter={() => setHoveredCounty(countyName)}
                                    onMouseLeave={() => setHoveredCounty(null)}
                                />
                            );
                        })}
                    </g>

                    {/* Label */}
                    <text x="200" y="580" textAnchor="middle" className="text-sm fill-slate-600 font-medium">
                        California Counties
                    </text>
                </svg>

                {/* Selected/Hovered County Info */}
                <div className="mt-4 min-h-[60px]">
                    {hoveredCounty && (
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                            <p className="text-sm font-medium text-blue-900">{hoveredCounty} County</p>
                            <p className="text-xs text-blue-700 mt-1">
                                HSA: {countyToHSA[hoveredCounty] || 'Not mapped'}
                            </p>
                        </div>
                    )}
                    {!hoveredCounty && selectedHSA && (
                        <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
                            <p className="text-sm font-medium text-slate-900">Selected: {selectedHSA}</p>
                        </div>
                    )}
                </div>

                {/* Alternative: County List for easier access */}
                <div className="mt-4">
                    <p className="text-xs text-slate-500 mb-2">Or select from major counties:</p>
                    <div className="grid grid-cols-2 gap-2">
                        {['Los Angeles', 'San Francisco', 'San Diego', 'Orange', 'Riverside',
                            'Sacramento', 'Alameda', 'Santa Clara', 'Fresno', 'Kern'].map((county) => (
                                <button
                                    key={county}
                                    onClick={() => handleCountyClick(county)}
                                    className={`text-xs px-3 py-2 rounded-lg border transition-colors ${isCountySelected(county)
                                            ? 'bg-blue-100 border-blue-300 text-blue-700 font-medium'
                                            : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                                        }`}
                                >
                                    {county}
                                </button>
                            ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CaliforniaMap;
