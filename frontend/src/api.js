import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const checkHealth = async () => {
    try {
        const response = await axios.get(`${API_URL}/health`);
        return response.data;
    } catch (error) {
        console.error('Health check failed:', error);
        return { status: 'offline' };
    }
};

export const predictRisk = async (features) => {
    try {
        const response = await axios.post(`${API_URL}/predict`, { features });
        return response.data;
    } catch (error) {
        console.error('Prediction failed:', error);
        throw error;
    }
};

export const getTopFeatures = async () => {
    try {
        const response = await axios.get(`${API_URL}/top-features`);
        return response.data;
    } catch (error) {
        console.error('Failed to get top features:', error);
        return { top_features: [] };
    }
};
