import axios from 'axios';

// Usa variable de entorno o fallback a localhost para desarrollo
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getFormOptions = async () => {
  const response = await api.get('/predictor/api/options/');
  return response.data;
};

export const predictPrice = async (data) => {
  const response = await api.post('/predictor/api/predict/', data);
  return response.data;
};

export const getDashboardStats = async () => {
  const response = await api.get('/predictor/api/stats/');
  return response.data;
};

export default api;
