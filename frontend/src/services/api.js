import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for analysis
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze a GitHub profile
 * @param {string} username - GitHub username
 * @param {boolean} includeAiFeedback - Whether to include AI-generated feedback
 * @returns {Promise} Analysis result
 */
export const analyzeProfile = async (username, includeAiFeedback = true) => {
  try {
    const response = await api.post(
      `/api/analyze/${username}`,
      null,
      {
        params: { include_ai_feedback: includeAiFeedback }
      }
    );
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.detail || 'Analysis failed');
    } else if (error.request) {
      // No response received
      throw new Error('Server not responding. Please check if the backend is running.');
    } else {
      // Request setup error
      throw new Error('Failed to send request: ' + error.message);
    }
  }
};

/**
 * Check API health
 * @returns {Promise} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    throw new Error('Health check failed');
  }
};

export default api;
