import os

project_root = r"D:\Lymphoma Detection Project"
src_dir = os.path.join(project_root, "frontend", "src")
pages_dir = os.path.join(src_dir, "pages")
components_dir = os.path.join(src_dir, "components")
os.makedirs(pages_dir, exist_ok=True)
os.makedirs(components_dir, exist_ok=True)

files = {}

# 1. index.css (Clean light theme)
files["frontend/src/index.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-50 text-slate-900 min-h-screen antialiased;
    font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  }
}

/* Subtle clean scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f8fafc;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.2s ease-out forwards;
}
"""

# 2. components/MedicalDisclaimer.jsx
files["frontend/src/components/MedicalDisclaimer.jsx"] = """import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

export default function MedicalDisclaimer({ compact = false }) {
  if (compact) {
    return (
      <div className="bg-amber-50 border border-amber-200 rounded-xl px-3.5 py-2 text-xs text-amber-800 flex items-center gap-2 shadow-xs">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
        <span>
          <strong>Academic Research Prototype:</strong> This AI system is designed for computer-aided screening and research purposes only. Not a clinical diagnosis.
        </span>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-r from-amber-50 via-amber-50/80 to-amber-50 border border-amber-200 rounded-2xl p-4 sm:p-5 text-amber-900 text-sm shadow-xs">
      <div className="flex items-start gap-3.5">
        <div className="p-2 bg-amber-100 rounded-xl text-amber-700 shrink-0 mt-0.5">
          <AlertTriangle className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <div className="font-bold text-amber-950 text-sm sm:text-base flex items-center gap-2">
            Clinical Decision Support & Screening Notice
            <span className="text-[10px] font-semibold px-2 py-0.5 bg-amber-200/70 text-amber-900 rounded-full border border-amber-300">
              Two-Stage Screening Guard
            </span>
          </div>
          <p className="text-xs text-amber-800/90 leading-relaxed font-normal">
            This framework operates under a calibrated confidence thresholding mechanism. If an uploaded slide does not meet the required confidence criteria, it is rejected as <strong>"No Lymphoma Detected / Not Classified as Lymphoma"</strong> rather than forcing an inaccurate subtype.
            A negative screening result does not prove the absence of disease and must never replace board-certified pathological and immunohistochemical evaluation.
          </p>
        </div>
      </div>
    </div>
  );
}
"""

# 3. components/Navbar.jsx
files["frontend/src/components/Navbar.jsx"] = """import React from 'react';
import { 
  Activity, Microscope, BarChart3, History, Info, Cpu, 
  MessageSquare, ShieldAlert, LogIn, UserPlus, User, LogOut, LayoutDashboard 
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, systemStatus, currentUser, onLogout }) {
  const isAdmin = currentUser?.role === 'ADMIN';
  const isLoggedIn = !!currentUser;

  let navItems = [];

  if (!isLoggedIn) {
    navItems = [
      { id: 'home', label: 'Overview', icon: Microscope },
      { id: 'analysis', label: 'Slide Analysis', icon: Activity },
      { id: 'performance', label: 'Model Benchmarks', icon: BarChart3 },
      { id: 'about', label: 'Methodology & AI', icon: Info },
    ];
  } else if (isAdmin) {
    navItems = [
      { id: 'admin-dashboard', label: 'Admin Console', icon: ShieldAlert },
      { id: 'analysis', label: 'Slide Analysis', icon: Activity },
      { id: 'history', label: 'History Management', icon: History },
      { id: 'chat', label: 'Gemini AI Chat', icon: MessageSquare },
      { id: 'performance', label: 'Benchmarks', icon: BarChart3 },
      { id: 'about', label: 'Methodology', icon: Info },
    ];
  } else {
    navItems = [
      { id: 'user-dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { id: 'analysis', label: 'Slide Analysis', icon: Activity },
      { id: 'history', label: 'Clinical History', icon: History },
      { id: 'chat', label: 'Gemini AI Chat', icon: MessageSquare },
      { id: 'performance', label: 'Benchmarks', icon: BarChart3 },
      { id: 'about', label: 'Methodology', icon: Info },
    ];
  }

  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-50 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div
            className="flex items-center space-x-3 cursor-pointer select-none"
            onClick={() => setActiveTab(isLoggedIn ? (isAdmin ? 'admin-dashboard' : 'user-dashboard') : 'home')}
          >
            <div className="w-9 h-9 rounded-xl bg-sky-600 flex items-center justify-center text-white shadow-xs">
              <Microscope className="w-5 h-5" />
            </div>
            <div>
              <span className="font-extrabold text-slate-900 text-lg tracking-tight">
                Lymphoma<span className="text-sky-600">AI</span>
              </span>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">Attention-Augmented Deep Learning</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-semibold transition-all cursor-pointer ${
                    isActive
                      ? 'bg-sky-50 text-sky-700 font-bold border border-sky-200/80 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-sky-600' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Action / Auth Area */}
          <div className="flex items-center space-x-3">
            {isLoggedIn ? (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setActiveTab('profile')}
                  className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === 'profile'
                      ? 'bg-sky-50 border-sky-200 text-sky-700'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <User className="w-3.5 h-3.5 text-slate-500" />
                  <span className="max-w-[110px] truncate">{currentUser.full_name?.split(' ')[0]}</span>
                  <span className={`text-[10px] px-1.5 py-0.2 rounded font-bold uppercase ${
                    isAdmin ? 'bg-rose-100 text-rose-800' : 'bg-sky-100 text-sky-800'
                  }`}>
                    {currentUser.role}
                  </span>
                </button>

                <button
                  onClick={onLogout}
                  title="Sign Out"
                  className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-colors cursor-pointer"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setActiveTab('login')}
                  className="flex items-center space-x-1.5 px-3.5 py-2 text-xs font-bold text-slate-700 hover:text-slate-900 hover:bg-slate-50 rounded-xl transition-colors cursor-pointer"
                >
                  <LogIn className="w-3.5 h-3.5 text-slate-500" />
                  <span>Login</span>
                </button>

                <button
                  onClick={() => setActiveTab('register')}
                  className="flex items-center space-x-1.5 px-4 py-2 text-xs font-bold text-white bg-sky-600 hover:bg-sky-500 rounded-xl shadow-xs transition-all hover:scale-[1.02] cursor-pointer"
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  <span>Create Account</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Bar */}
      <div className="md:hidden flex overflow-x-auto px-2 py-1.5 border-t border-slate-100 space-x-1 bg-slate-50">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium whitespace-nowrap ${
                isActive ? 'bg-white text-sky-700 shadow-xs font-semibold' : 'text-slate-600'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
"""

# 4. pages/Home.jsx
files["frontend/src/pages/Home.jsx"] = """import React from 'react';
import { Microscope, Activity, Eye, Zap, ArrowRight, BarChart3, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';
import MedicalDisclaimer from '../components/MedicalDisclaimer';

export default function Home({ setActiveTab }) {
  const benefits = [
    {
      title: 'Two-Stage Screening Guard',
      desc: 'Confidence-gated evaluation rejects out-of-distribution slides as "No Lymphoma Detected" instead of forcing inaccurate cancer classifications.',
      icon: ShieldCheck,
    },
    {
      title: 'CBAM Attention Modules',
      desc: 'Dual channel and spatial attention mechanisms recalibrate residual feature maps to focus on diagnostic cellular morphology.',
      icon: Eye,
    },
    {
      title: 'Grad-CAM++ Explainability',
      desc: 'Visual region activation heatmaps provide transparent morphological rationale for every accepted prediction.',
      icon: Microscope,
    },
  ];

  const steps = [
    {
      number: '01',
      title: 'Upload Specimen',
      desc: 'Drag & drop any microscopic histopathology biopsy slide (TIFF, PNG, or JPG).',
    },
    {
      number: '02',
      title: 'AI Feature Extraction',
      desc: 'Residual backbone and Stage 3/4 CBAM attention modules process cellular chromatin texture.',
    },
    {
      number: '03',
      title: 'Inspect & Verify',
      desc: 'Review two-stage screening outcome, 3-class probabilities, and Grad-CAM++ visual overlays.',
    },
  ];

  return (
    <div className="space-y-12 py-4 animate-fadeIn max-w-6xl mx-auto">
      <MedicalDisclaimer />

      {/* 1. Hero Section */}
      <section className="text-center space-y-6 pt-4 pb-2">
        <div className="inline-flex items-center space-x-2 bg-sky-50 border border-sky-100 text-sky-700 text-xs font-semibold px-3.5 py-1 rounded-full shadow-xs">
          <Sparkles className="w-3.5 h-3.5 text-sky-600" />
          <span>AI-Assisted Digital Pathology Screening</span>
        </div>

        <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-tight">
          Attention-Augmented Deep Learning for <span className="text-sky-600">Lymphoma Detection</span>
        </h1>

        <p className="text-slate-600 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
          Automated histopathological slide screening and 3-class lymphoma classification (<strong>CLL</strong>, <strong>FL</strong>, <strong>MCL</strong>) powered by deep residual feature extraction, CBAM attention mechanisms, and Grad-CAM++ visual explainability.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <button
            onClick={() => setActiveTab('analysis')}
            className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold px-6 py-3 rounded-xl shadow-sm transition-all hover:scale-[1.01] active:scale-[0.99] text-sm cursor-pointer"
          >
            <Activity className="w-4 h-4" />
            <span>Launch Slide Analysis</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => setActiveTab('performance')}
            className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-white hover:bg-slate-50 text-slate-700 font-semibold px-6 py-3 rounded-xl border border-slate-200 shadow-xs transition-all text-sm cursor-pointer"
          >
            <BarChart3 className="w-4 h-4 text-sky-600" />
            <span>View Benchmarks</span>
          </button>
        </div>

        {/* Metric Badges */}
        <div className="pt-4 grid grid-cols-2 md:grid-cols-4 gap-3 max-w-3xl mx-auto">
          {[
            { label: 'Test Accuracy', val: '85.96%' },
            { label: 'Ablation Gain', val: '+7.01%' },
            { label: 'Target Classes', val: 'CLL, FL, MCL' },
            { label: 'Inference Latency', val: '~45 ms' },
          ].map((item, idx) => (
            <div key={idx} className="bg-white border border-slate-200 rounded-xl p-3.5 shadow-xs text-center">
              <div className="text-xl font-bold text-slate-900 font-mono">{item.val}</div>
              <div className="text-xs text-slate-500 mt-0.5">{item.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* 2. Two-Stage Screening Logic */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="bg-white border border-emerald-200 rounded-2xl p-6 shadow-xs space-y-3">
          <div className="flex items-center justify-between">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              Outcome 1 • Accepted
            </span>
            <span className="text-xs text-slate-400 font-mono">Confidence &ge; 80%</span>
          </div>
          <h3 className="text-lg font-bold text-slate-900">Lymphoma Detected</h3>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
            When microscopic cellular features pass the model's calibrated confidence criteria, the system classifies into <strong>CLL</strong>, <strong>FL</strong>, or <strong>MCL</strong>, computes full probability distributions, and overlays a Grad-CAM++ attention heatmap.
          </p>
        </div>

        <div className="bg-white border border-amber-200 rounded-2xl p-6 shadow-xs space-y-3">
          <div className="flex items-center justify-between">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase bg-amber-50 text-amber-700 border border-amber-200 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
              Outcome 2 • Rejection Guard
            </span>
            <span className="text-xs text-slate-400 font-mono">Confidence &lt; 80%</span>
          </div>
          <h3 className="text-lg font-bold text-slate-900">No Lymphoma Detected / Rejected</h3>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
            Unlike standard softmax classifiers that force every image into a cancer type, our framework guards against hallucinations by returning <strong>"No Lymphoma Detected"</strong> when confidence is below the accepted screening threshold.
          </p>
        </div>
      </section>

      {/* 3. Key Features */}
      <section className="space-y-6">
        <div className="text-center space-y-1">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Key Architectural Features
          </h2>
          <p className="text-slate-500 text-sm max-w-lg mx-auto">
            Combining robust residual architecture with attention refinement for reliable digital pathology.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {benefits.map((b, idx) => {
            const Icon = b.icon;
            return (
              <div
                key={idx}
                className="bg-white border border-slate-200 hover:border-slate-300 rounded-xl p-6 shadow-xs transition-all space-y-3"
              >
                <div className="w-10 h-10 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center border border-sky-100">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-slate-900">{b.title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed font-normal">{b.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* 4. Workflow Steps */}
      <section className="bg-white border border-slate-200 rounded-2xl p-8 space-y-6 shadow-xs">
        <div className="text-center space-y-1">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Workflow & Decision Pipeline
          </h2>
          <p className="text-slate-500 text-sm">
            Three simple steps from specimen upload to interpretable screening results.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {steps.map((s, idx) => (
            <div key={idx} className="bg-slate-50 border border-slate-200/80 rounded-xl p-5 space-y-2">
              <div className="w-7 h-7 rounded-md bg-sky-600 text-white font-mono font-bold text-xs flex items-center justify-center shadow-xs">
                {s.number}
              </div>
              <h3 className="text-sm font-bold text-slate-900 pt-1">{s.title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed font-normal">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("Created index.css, MedicalDisclaimer, Navbar, and Home.jsx successfully.")
