import React from 'react';
import { useNavigate } from 'react-router-dom';
import './FacilityTypeSelection.css';

function FacilityTypeSelection() {
    const navigate = useNavigate();

    return (
        <div className="facility-type-page">
            <div className="facility-type-container">
                <h1 className="facility-type-title">Select Facility Type</h1>
                <p className="facility-type-subtitle">
                    Choose the type of healthcare facility you want to assess
                </p>

                <div className="facility-cards">
                    <div
                        className="facility-card"
                        onClick={() => navigate('/input/longterm')}
                    >
                        <div className="facility-card-icon">🏥</div>
                        <h2>Long-Term Care Facility</h2>
                        <p>Skilled nursing facilities, assisted living, and long-term care centers</p>
                        <button className="facility-card-button">Select</button>
                    </div>

                    <div
                        className="facility-card"
                        onClick={() => navigate('/input/hospital')}
                    >
                        <div className="facility-card-icon">🏨</div>
                        <h2>Hospital</h2>
                        <p>Acute care hospitals, community hospitals, and medical centers</p>
                        <button className="facility-card-button">Select</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default FacilityTypeSelection;
