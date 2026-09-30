import os

project_root = r"D:\Lymphoma Detection Project"
api_path = os.path.join(project_root, "frontend", "src", "services", "api.js")

api_content = """import axios from 'axios';

const API_BASE = '/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('lymphoma_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// Error Interceptor for auto-logout
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('lymphoma_token');
      localStorage.removeItem('lymphoma_user');
      window.dispatchEvent(new Event('auth-expired'));
    }
    return Promise.reject(error);
  }
);

// 1. System & Health
export const getHealth = async () => {
  const res = await axios.get(`${API_BASE}/system/health`);
  return res.data;
};

export const getModelInfo = async () => {
  const res = await axios.get(`${API_BASE}/metrics/classes`);
  return res.data;
};

// 2. Authentication
export const registerUser = async (userData) => {
  const res = await axios.post(`${API_BASE}/auth/register`, userData);
  return res.data;
};

export const loginUser = async (credentials) => {
  const res = await axios.post(`${API_BASE}/auth/login`, credentials);
  return res.data;
};

export const getCurrentUser = async () => {
  const res = await axios.get(`${API_BASE}/auth/me`, { headers: getAuthHeaders() });
  return res.data;
};

// 3. Slide Analysis & Screening
export const validateImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await axios.post(`${API_BASE}/predict/validate`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return res.data;
};

export const predictAndExplain = async (file, threshold = null) => {
  const formData = new FormData();
  formData.append('file', file);
  if (threshold !== null) {
    formData.append('threshold', threshold);
  }
  const res = await axios.post(`${API_BASE}/predict/`, formData, {
    headers: { ...getAuthHeaders(), 'Content-Type': 'multipart/form-data' }
  });
  return res.data;
};

export const predictBatch = async (files, threshold = null) => {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  if (threshold !== null) {
    formData.append('threshold', threshold);
  }
  const res = await axios.post(`${API_BASE}/predict/batch`, formData, {
    headers: { ...getAuthHeaders(), 'Content-Type': 'multipart/form-data' }
  });
  return res.data;
};

export const submitFeedback = async (feedbackData) => {
  const res = await axios.post(`${API_BASE}/predict/feedback`, feedbackData, {
    headers: getAuthHeaders()
  });
  return res.data;
};

// 4. Benchmarks & Metrics
export const getBenchmarks = async () => {
  const res = await axios.get(`${API_BASE}/metrics/benchmarks`);
  return res.data;
};

export const getAblation = async () => {
  const res = await axios.get(`${API_BASE}/metrics/ablation`);
  return res.data;
};

export const getThresholdAnalysis = async () => {
  const res = await axios.get(`${API_BASE}/metrics/thresholds`);
  return res.data;
};

export const getTrainingHistories = async () => {
  const res = await axios.get(`${API_BASE}/metrics/histories`);
  return res.data;
};

// 5. Pre-Clinical History
export const getHistory = async (params = {}) => {
  const res = await axios.get(`${API_BASE}/history/`, {
    params,
    headers: getAuthHeaders()
  });
  return res.data;
};

export const deleteCase = async (caseId) => {
  const res = await axios.delete(`${API_BASE}/history/${caseId}`, {
    headers: getAuthHeaders()
  });
  return res.data;
};

export const clearHistory = async () => {
  const res = await axios.post(`${API_BASE}/history/clear-all`, {}, {
    headers: getAuthHeaders()
  });
  return res.data;
};

// 6. System Configuration
export const getThreshold = async () => {
  const res = await axios.get(`${API_BASE}/config/threshold`);
  return res.data;
};

export const updateThreshold = async (threshold) => {
  const res = await axios.post(`${API_BASE}/config/threshold`, { threshold }, {
    headers: getAuthHeaders()
  });
  return res.data;
};

// 7. Chat Assistant
export const sendMessageToChat = async (message) => {
  const res = await axios.post(`${API_BASE}/chat/`, { message }, {
    headers: getAuthHeaders()
  });
  return res.data;
};

export const api = {
  getHealth,
  getModelInfo,
  registerUser,
  loginUser,
  getCurrentUser,
  validateImage,
  predictAndExplain,
  predictSingle: predictAndExplain,
  predictBatch,
  submitFeedback,
  getBenchmarks,
  getAblation,
  getThresholdAnalysis,
  getClassMetadata: getModelInfo,
  getTrainingHistories,
  getHistory,
  deleteCase,
  clearHistory,
  getThreshold,
  updateThreshold,
  sendMessageToChat
};
"""

with open(api_path, "w", encoding="utf-8") as f:
    f.write(api_content)

print("Updated frontend/src/services/api.js successfully.")
