import os

project_root = r"D:\Lymphoma Detection Project"
files = {}

# 1. Medical Disclaimer Component
files["frontend/src/components/MedicalDisclaimer.jsx"] = """import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

export default function MedicalDisclaimer({ compact = false }) {
  if (compact) {
    return (
      <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg px-3 py-2 text-xs text-amber-300 flex items-center gap-2">
        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
        <span>
          <strong>Academic Research Prototype:</strong> This AI system is intended for computer-aided screening and research purposes only. Not a clinical diagnosis.
        </span>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-r from-amber-950/40 via-amber-900/20 to-amber-950/40 border border-amber-500/30 rounded-xl p-4 text-amber-200 text-sm shadow-lg backdrop-blur-sm">
      <div className="flex items-start gap-3">
        <div className="p-2 bg-amber-500/20 rounded-lg text-amber-400 shrink-0 mt-0.5">
          <AlertTriangle className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <div className="font-bold text-amber-300 text-base flex items-center gap-2">
            Clinical Decision Support & Research Notice
            <span className="text-xs font-normal px-2 py-0.5 bg-amber-500/20 rounded-full border border-amber-500/40 text-amber-200">
              Two-Stage Screening Guard
            </span>
          </div>
          <p className="text-xs text-amber-200/90 leading-relaxed">
            This deep learning framework operates under an active confidence thresholding mechanism. If an image features insufficient evidence or is outside the learned lymphoma distribution, the prediction is rejected as <strong>"No Lymphoma Detected"</strong> rather than forcing an inaccurate subtype.
            A negative screening result does not prove the absence of disease and must never replace board-certified histological and immunohistochemical review.
          </p>
        </div>
      </div>
    </div>
  );
}
"""

# 2. Navbar Component
files["frontend/src/components/Navbar.jsx"] = """import React, { useState, useEffect } from 'react';
import { 
  Activity, Microscopic, BarChart3, BookOpen, History, 
  Settings, CheckCircle2, AlertCircle, Cpu, Layers 
} from 'lucide-react';
import { api } from '../services/api';

export default function Navbar({ activeTab, setActiveTab }) {
  const [health, setHealth] = useState({ status: 'checking', cuda: false, gpu: '' });

  useEffect(() => {
    api.getHealth()
      .then(res => {
        setHealth({
          status: res.status,
          cuda: res.hardware?.cuda_available || false,
          gpu: res.hardware?.gpu_name || 'CPU'
        });
      })
      .catch(() => setHealth({ status: 'offline', cuda: false, gpu: '' }));
  }, []);

  const navItems = [
    { id: 'home', label: 'Overview', icon: Activity },
    { id: 'analysis', label: 'Screening Hub', icon: Layers },
    { id: 'performance', label: 'Benchmarks & Evaluation', icon: BarChart3 },
    { id: 'about', label: 'Pathology & Math', icon: BookOpen },
    { id: 'history', label: 'Case Logs', icon: History },
    { id: 'admin', label: 'System Config', icon: Settings },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div 
            onClick={() => setActiveTab('home')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-500 p-0.5 shadow-lg shadow-sky-500/20 group-hover:shadow-sky-500/40 transition-all">
              <div className="w-full h-full bg-slate-900 rounded-[10px] flex items-center justify-center">
                <Layers className="w-5 h-5 text-sky-400 group-hover:scale-110 transition-transform" />
              </div>
            </div>
            <div>
              <div className="font-bold text-base tracking-tight text-white flex items-center gap-2">
                <span>Lymphoma<span className="text-sky-400">AI</span></span>
                <span className="text-[10px] uppercase font-semibold px-2 py-0.5 bg-sky-500/10 text-sky-400 border border-sky-500/30 rounded-full">
                  Attention-ResNet50
                </span>
              </div>
              <div className="text-[11px] text-slate-400 font-medium">
                CLL • FL • MCL Digital Pathology
              </div>
            </div>
          </div>

          {/* Navigation Items */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-semibold transition-all ${
                    isActive 
                      ? 'bg-sky-500 text-white shadow-md shadow-sky-500/25' 
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* System Health Badge */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs font-medium">
              <div className={`w-2 h-2 rounded-full ${health.status === 'online' ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`} />
              <span className="text-slate-300">
                {health.status === 'online' ? (health.cuda ? `GPU: ${health.gpu.replace('Laptop GPU', '')}` : 'CPU Mode') : 'API Offline'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("Navbar and MedicalDisclaimer components created successfully.")
