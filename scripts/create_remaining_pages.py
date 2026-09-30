import os

project_root = r"D:\Lymphoma Detection Project"
pages_dir = os.path.join(project_root, "frontend", "src", "pages")
src_dir = os.path.join(project_root, "frontend", "src")

# 1. About.jsx
about_jsx = """import React from 'react';
import { BookOpen, Layers, Microscope, Sparkles, BrainCircuit, Activity } from 'lucide-react';
import MedicalDisclaimer from '../components/MedicalDisclaimer';

export default function About() {
  return (
    <div className="space-y-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Clinical Pathology & Mathematical Theory</h1>
        <p className="text-sm text-slate-400 mt-1">
          Histological hallmarks of malignant lymphomas and mathematical foundations of Attention-Augmented Residual Learning.
        </p>
      </div>

      <MedicalDisclaimer />

      {/* 3 Lymphoma Histology Profiles */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <Microscope className="w-6 h-6 text-sky-400" />
          Histological & Cellular Morphology Profiles
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* CLL */}
          <div className="rounded-3xl bg-slate-800/50 border border-slate-700 p-6 space-y-4 shadow-lg">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-sky-500/20 text-sky-300 rounded-full text-xs font-bold border border-sky-500/40">
                Class 0 • CLL / SLL
              </span>
            </div>
            <h3 className="text-lg font-bold text-white">Chronic Lymphocytic Leukemia</h3>
            <div className="space-y-2 text-xs text-slate-300 leading-relaxed">
              <p><strong>Cellular Composition:</strong> Monotonous proliferation of small, round, mature-appearing B-lymphocytes.</p>
              <p><strong>Nuclear Characteristics:</strong> Dense, heavily clumped "soccer-ball" chromatin with indistinct or absent nucleoli and very scant cytoplasm.</p>
              <p><strong>Tissue Architecture:</strong> Diffuse pattern effacing the normal nodal architecture, with pale pseudofollicles (proliferation centers) containing prolymphocytes.</p>
              <p><strong>Immunophenotype:</strong> CD5+, CD19+, CD20+ (dim), CD23+, Cyclin D1-.</p>
            </div>
          </div>

          {/* FL */}
          <div className="rounded-3xl bg-slate-800/50 border border-slate-700 p-6 space-y-4 shadow-lg">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-indigo-500/20 text-indigo-300 rounded-full text-xs font-bold border border-indigo-500/40">
                Class 1 • FL
              </span>
            </div>
            <h3 className="text-lg font-bold text-white">Follicular Lymphoma</h3>
            <div className="space-y-2 text-xs text-slate-300 leading-relaxed">
              <p><strong>Cellular Composition:</strong> Mixture of centrocytes (small to medium cleaved cells) and centroblasts (large transformed cells).</p>
              <p><strong>Nuclear Characteristics:</strong> Centrocytes feature angular, notched, or deeply cleaved nuclear contours. Centroblasts feature vesicular nuclei with 1-3 peripheral nucleoli.</p>
              <p><strong>Tissue Architecture:</strong> Closely spaced, back-to-back neoplastic follicles lacking normal polarized mantle zones or tingible-body macrophages.</p>
              <p><strong>Immunophenotype:</strong> CD10+, BCL2+ (translocation t(14;18)), CD20+, BCL6+.</p>
            </div>
          </div>

          {/* MCL */}
          <div className="rounded-3xl bg-slate-800/50 border border-slate-700 p-6 space-y-4 shadow-lg">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-xs font-bold border border-purple-500/40">
                Class 2 • MCL
              </span>
            </div>
            <h3 className="text-lg font-bold text-white">Mantle Cell Lymphoma</h3>
            <div className="space-y-2 text-xs text-slate-300 leading-relaxed">
              <p><strong>Cellular Composition:</strong> Monotonous population of small-to-medium lymphocytes resembling mantle zone B-cells.</p>
              <p><strong>Nuclear Characteristics:</strong> Slightly irregular, indented or cleaved nuclear membranes, finely dispersed or moderately clumped chromatin, lacking large centroblasts.</p>
              <p><strong>Tissue Architecture:</strong> Mantle zone, nodular, or diffuse expansion with hyalinized blood vessels and scattered epithelioid histiocytes.</p>
              <p><strong>Immunophenotype:</strong> CD5+, CD20+, Cyclin D1+ (translocation t(11;14) CCND1::IGH), SOX11+, CD23-.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Deep Learning & Attention Mathematical Formulations */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <BrainCircuit className="w-6 h-6 text-indigo-400" />
          Attention-Augmented Architecture Formulation
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* CBAM Channel Attention */}
          <div className="rounded-3xl bg-slate-800/40 border border-slate-700 p-6 space-y-3">
            <h3 className="text-base font-bold text-white">1. Channel Attention Module (CAM)</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Computes inter-channel relationships by combining spatial Global Average Pooling (GAP) and Global Max Pooling (GMP) through a shared multi-layer perceptron (MLP) with reduction ratio \(r=16\):
            </p>
            <div className="p-3 bg-slate-900 rounded-xl font-mono text-xs text-sky-300 border border-slate-800">
              M_c(F) = &sigma;( MLP(AvgPool(F)) + MLP(MaxPool(F)) )<br/>
              = &sigma;( W_1(W_0(F_avg^c)) + W_1(W_0(F_max^c)) )
            </div>
          </div>

          {/* CBAM Spatial Attention */}
          <div className="rounded-3xl bg-slate-800/40 border border-slate-700 p-6 space-y-3">
            <h3 className="text-base font-bold text-white">2. Spatial Attention Module (SAM)</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Computes inter-spatial relationships by applying average and max pooling across channels, followed by a 7x7 convolution to pinpoint diagnostic cellular regions:
            </p>
            <div className="p-3 bg-slate-900 rounded-xl font-mono text-xs text-indigo-300 border border-slate-800">
              M_s(F') = &sigma;( f^&#123;7x7&#125;( [AvgPool(F'); MaxPool(F')] ) )
            </div>
          </div>

          {/* Grad-CAM++ */}
          <div className="rounded-3xl bg-slate-800/40 border border-slate-700 p-6 space-y-3">
            <h3 className="text-base font-bold text-white">3. Grad-CAM++ Explainability</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Calculates higher-order positive gradient weights (\(w_k^c\)) to highlight multiple instances of cleaved nuclei and cellular clusters in histopathological slides:
            </p>
            <div className="p-3 bg-slate-900 rounded-xl font-mono text-xs text-emerald-300 border border-slate-800">
              L_&#123;Grad-CAM++&#125;^c = ReLU(&Sigma;_k w_k^c &middot; A^k)
            </div>
          </div>

          {/* Two-Stage Rejection Logic */}
          <div className="rounded-3xl bg-slate-800/40 border border-slate-700 p-6 space-y-3">
            <h3 className="text-base font-bold text-white">4. Two-Stage Confidence Screening</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Rejection decision boundary based on Maximum Softmax Probability (MSP) against validated threshold \(\tau = 0.80\):
            </p>
            <div className="p-3 bg-slate-900 rounded-xl font-mono text-xs text-amber-300 border border-slate-800">
              Outcome = Lymphoma Detected (if max_i P(y=i|x) &ge; &tau;)<br/>
              Outcome = No Lymphoma Detected (if max_i P(y=i|x) &lt; &tau;)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

# 2. History.jsx
history_jsx = """import React, { useState, useEffect } from 'react';
import { History, Download, Trash2, Search, Filter, RefreshCw, FileText, CheckCircle2, AlertTriangle } from 'lucide-react';
import { api } from '../services/api';

export default function HistoryPage() {
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [outcomeFilter, setOutcomeFilter] = useState('');

  const fetchHistory = () => {
    setLoading(true);
    api.getHistory({ outcome: outcomeFilter || undefined, limit: 100 })
      .then(res => {
        setRecords(res.records || []);
        setTotal(res.total || 0);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory();
  }, [outcomeFilter]);

  const handleDelete = async (caseId) => {
    if (window.confirm(`Delete record ${caseId}?`)) {
      await api.deleteCase(caseId);
      fetchHistory();
    }
  };

  const handleClearAll = async () => {
    if (window.confirm("Are you sure you want to clear all history records?")) {
      await api.clearHistory();
      fetchHistory();
    }
  };

  const filtered = records.filter(r => 
    r.case_id?.toLowerCase().includes(search.toLowerCase()) ||
    r.file_name?.toLowerCase().includes(search.toLowerCase()) ||
    r.predicted_subtype?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Case Audit History & Logs</h1>
          <p className="text-sm text-slate-400 mt-1">
            Complete database of clinical screening cases, confidence records, and generated PDF reports.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchHistory}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs border border-slate-700 flex items-center gap-2"
          >
            <RefreshCw className="w-3.5 h-3.5 text-sky-400" />
            Refresh
          </button>
          {records.length > 0 && (
            <button
              onClick={handleClearAll}
              className="px-4 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 font-bold text-xs border border-red-500/30 flex items-center gap-2"
            >
              <Trash2 className="w-3.5 h-3.5" />
              Clear All Logs
            </button>
          )}
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-12 gap-4">
        <div className="sm:col-span-8 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search by Case ID, Filename, or Subtype..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-white placeholder-slate-400 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div className="sm:col-span-4">
          <select
            value={outcomeFilter}
            onChange={(e) => setOutcomeFilter(e.target.value)}
            className="w-full py-2 px-3 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-sky-500"
          >
            <option value="">All Outcomes</option>
            <option value="LYMPHOMA_DETECTED">Lymphoma Detected Only</option>
            <option value="NO_LYMPHOMA_DETECTED">No Lymphoma Detected (Rejected)</option>
            <option value="UNABLE_TO_ANALYZE">Unable to Analyze</option>
          </select>
        </div>
      </div>

      {/* History Table */}
      <div className="rounded-3xl bg-slate-800/50 border border-slate-700/80 overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left text-slate-300">
            <thead className="bg-slate-900 text-slate-400 uppercase font-semibold">
              <tr>
                <th className="p-3.5">Case Reference</th>
                <th className="p-3.5">Timestamp</th>
                <th className="p-3.5">Slide Image</th>
                <th className="p-3.5">Outcome</th>
                <th className="p-3.5">Subtype</th>
                <th className="p-3.5">Confidence</th>
                <th className="p-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/60 font-mono">
              {filtered.length > 0 ? (
                filtered.map((r) => (
                  <tr key={r.case_id} className="hover:bg-slate-700/30 transition-colors">
                    <td className="p-3.5 font-bold text-sky-400">{r.case_id}</td>
                    <td className="p-3.5 text-slate-400 font-sans">{new Date(r.created_at).toLocaleString()}</td>
                    <td className="p-3.5 truncate max-w-xs">{r.file_name}</td>
                    <td className="p-3.5">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        r.outcome === 'LYMPHOMA_DETECTED' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' :
                        r.outcome === 'NO_LYMPHOMA_DETECTED' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' :
                        'bg-red-500/20 text-red-300 border border-red-500/40'
                      }`}>
                        {r.outcome}
                      </span>
                    </td>
                    <td className="p-3.5 font-sans font-semibold text-white">
                      {r.predicted_subtype || '—'}
                    </td>
                    <td className="p-3.5 text-emerald-400 font-bold">
                      {r.confidence ? `${(r.confidence * 100).toFixed(2)}%` : '—'}
                    </td>
                    <td className="p-3.5 text-right space-x-2">
                      <a
                        href={`/api/reports/${r.case_id}/pdf`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 text-[11px] font-sans font-bold"
                      >
                        <FileText className="w-3.5 h-3.5 text-sky-400" />
                        PDF
                      </a>
                      <button
                        onClick={() => handleDelete(r.case_id)}
                        className="inline-flex items-center p-1 rounded-lg hover:bg-red-500/20 text-slate-400 hover:text-red-400"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="p-12 text-center text-slate-500 font-sans">
                    No clinical audit records found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
"""

# 3. AdminDashboard.jsx
admin_jsx = """import React, { useState, useEffect } from 'react';
import { Settings, Cpu, HardDrive, Sliders, ShieldCheck, RefreshCw, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export default function AdminDashboard() {
  const [health, setHealth] = useState(null);
  const [threshold, setThreshold] = useState(0.80);
  const [savedMsg, setSavedMsg] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStatus = () => {
    setLoading(true);
    Promise.all([api.getHealth(), api.getThreshold()])
      .then(([h, t]) => {
        setHealth(h);
        setThreshold(t.current_threshold);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleUpdateThreshold = async () => {
    try {
      const res = await api.updateThreshold(threshold);
      setSavedMsg(res.message);
      setTimeout(() => setSavedMsg(null), 4000);
    } catch (err) {
      alert('Failed to update threshold');
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">System & Model Configuration</h1>
        <p className="text-sm text-slate-400 mt-1">
          Real-time hardware monitoring and rejection parameter calibration.
        </p>
      </div>

      {/* Hardware Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-3xl bg-slate-800/50 border border-slate-700 p-6 space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/30">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400">Accelerator Device</div>
              <div className="text-base font-bold text-white">
                {health?.hardware?.gpu_name || 'CPU Mode'}
              </div>
            </div>
          </div>
          <div className="text-xs text-slate-400 font-mono">
            VRAM: {health?.hardware?.gpu_memory_gb || 0} GB • CUDA Active: {health?.hardware?.cuda_available ? 'Yes' : 'No'}
          </div>
        </div>

        <div className="rounded-3xl bg-slate-800/50 border border-slate-700 p-6 space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
              <HardDrive className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400">System Resources</div>
              <div className="text-base font-bold text-white">
                {health?.hardware?.cpu_cores} CPU Cores • {health?.hardware?.ram_gb} GB RAM
              </div>
            </div>
          </div>
          <div className="text-xs text-slate-400 font-mono">
            API Version: {health?.version} • Status: {health?.status}
          </div>
        </div>

        <div className="rounded-3xl bg-slate-800/50 border border-slate-700 p-6 space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400">Target Pathology Classes</div>
              <div className="text-base font-bold text-white">CLL • FL • MCL</div>
            </div>
          </div>
          <div className="text-xs text-slate-400 font-mono">
            Zero legacy leukemia terms • 3 Malignant Subtypes
          </div>
        </div>
      </div>

      {/* Threshold Calibration Card */}
      <div className="rounded-3xl bg-slate-800/60 border border-slate-700/80 p-8 space-y-6 shadow-xl max-w-3xl">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-sky-500/10 text-sky-400 rounded-2xl border border-sky-500/30">
            <Sliders className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">Live Confidence Rejection Threshold Tuning</h3>
            <p className="text-xs text-slate-400">
              Dynamically calibrate the system's sensitivity to reject out-of-distribution or ambiguous histological images.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-bold text-slate-200">Current Threshold:</span>
            <span className="text-2xl font-extrabold text-sky-400 font-mono">
              {(threshold * 100).toFixed(0)}%
            </span>
          </div>

          <input
            type="range"
            min="0.50"
            max="0.95"
            step="0.05"
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full accent-sky-500 h-2.5 bg-slate-700 rounded-lg cursor-pointer"
          />

          <div className="flex justify-between text-xs text-slate-500 font-mono">
            <span>50% (High Sensitivity)</span>
            <span>80% (Recommended Balance)</span>
            <span>95% (High Specificity)</span>
          </div>
        </div>

        <div className="flex items-center gap-4 pt-2">
          <button
            onClick={handleUpdateThreshold}
            className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-bold text-xs shadow-lg shadow-sky-500/25 transition-all"
          >
            Apply & Save Threshold
          </button>

          {savedMsg && (
            <div className="text-xs text-emerald-400 flex items-center gap-1.5 font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              {savedMsg}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""

# 4. App.jsx
app_jsx = """import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Analysis from './pages/Analysis';
import ModelPerformance from './pages/ModelPerformance';
import About from './pages/About';
import HistoryPage from './pages/History';
import AdminDashboard from './pages/AdminDashboard';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col text-slate-100">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1">
        {activeTab === 'home' && <Home setActiveTab={setActiveTab} />}
        {activeTab === 'analysis' && <Analysis />}
        {activeTab === 'performance' && <ModelPerformance />}
        {activeTab === 'about' && <About />}
        {activeTab === 'history' && <HistoryPage />}
        {activeTab === 'admin' && <AdminDashboard />}
      </main>

      <footer className="border-t border-slate-800 bg-slate-950/60 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 space-y-1">
          <p>Attention Augmented Residual Deep Learning Framework for Lymphoma Detection</p>
          <p>Academic Phase-II Digital Pathology Project • 3-Class Malignant Lymphoma Classification (CLL, FL, MCL)</p>
        </div>
      </footer>
    </div>
  );
}
"""

# 5. main.jsx
main_jsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
"""

with open(os.path.join(pages_dir, "About.jsx"), "w", encoding="utf-8") as f:
    f.write(about_jsx)

with open(os.path.join(pages_dir, "History.jsx"), "w", encoding="utf-8") as f:
    f.write(history_jsx)

with open(os.path.join(pages_dir, "AdminDashboard.jsx"), "w", encoding="utf-8") as f:
    f.write(admin_jsx)

with open(os.path.join(src_dir, "App.jsx"), "w", encoding="utf-8") as f:
    f.write(app_jsx)

with open(os.path.join(src_dir, "main.jsx"), "w", encoding="utf-8") as f:
    f.write(main_jsx)

print("Created About.jsx, History.jsx, AdminDashboard.jsx, App.jsx, and main.jsx successfully.")
