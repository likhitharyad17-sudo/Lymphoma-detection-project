import os

project_root = r"D:\Lymphoma Detection Project"
files = {}

# 1. Frontend Configuration
files["frontend/package.json"] = """{
  "name": "lymphoma-detection-system",
  "private": true,
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.7.9",
    "clsx": "^2.1.1",
    "lucide-react": "^0.475.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "recharts": "^2.15.1",
    "tailwind-merge": "^3.0.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.18",
    "@types/react-dom": "^18.3.5",
    "@vitejs/plugin-react": "^4.3.4",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.5.1",
    "tailwindcss": "^3.4.17",
    "vite": "^6.1.0"
  }
}
"""

files["frontend/vite.config.js"] = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
"""

files["frontend/tailwind.config.js"] = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          900: '#0c4a6e',
        }
      }
    },
  },
  plugins: [],
}
"""

files["frontend/postcss.config.js"] = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

files["frontend/index.html"] = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230284c7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m8 3 4 8 5-5 5 15H2L8 3z'/></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lymphoma Detection & Classification AI Framework</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-900 text-slate-100 antialiased selection:bg-sky-500 selection:text-white">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

files["frontend/src/index.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

code, pre {
  font-family: 'JetBrains Mono', monospace;
}

/* Custom modern scrollbars */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #0f172a;
}
::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #475569;
}
"""

# API Client Service
files["frontend/src/services/api.js"] = """import axios from 'axios';

const API_BASE = '/api';

export const api = {
  // Screening & Inference
  predictSingle: async (formData) => {
    const res = await axios.post(`${API_BASE}/predict/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  },

  predictBatch: async (formData) => {
    const res = await axios.post(`${API_BASE}/predict/batch`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  },

  // Benchmarks & Metrics
  getBenchmarks: async () => {
    const res = await axios.get(`${API_BASE}/metrics/benchmarks`);
    return res.data;
  },

  getAblation: async () => {
    const res = await axios.get(`${API_BASE}/metrics/ablation`);
    return res.data;
  },

  getThresholdAnalysis: async () => {
    const res = await axios.get(`${API_BASE}/metrics/thresholds`);
    return res.data;
  },

  getClassMetadata: async () => {
    const res = await axios.get(`${API_BASE}/metrics/classes`);
    return res.data;
  },

  getTrainingHistories: async () => {
    const res = await axios.get(`${API_BASE}/metrics/histories`);
    return res.data;
  },

  // Case Audit History
  getHistory: async (params = {}) => {
    const res = await axios.get(`${API_BASE}/history/`, { params });
    return res.data;
  },

  deleteCase: async (caseId) => {
    const res = await axios.delete(`${API_BASE}/history/${caseId}`);
    return res.data;
  },

  clearHistory: async () => {
    const res = await axios.post(`${API_BASE}/history/clear-all`);
    return res.data;
  },

  // Config
  getThreshold: async () => {
    const res = await axios.get(`${API_BASE}/config/threshold`);
    return res.data;
  },

  updateThreshold: async (threshold) => {
    const res = await axios.post(`${API_BASE}/config/threshold`, { threshold });
    return res.data;
  },

  // System Health
  getHealth: async () => {
    const res = await axios.get(`${API_BASE}/system/health`);
    return res.data;
  }
};
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("Frontend config, styles, and api client created successfully.")
