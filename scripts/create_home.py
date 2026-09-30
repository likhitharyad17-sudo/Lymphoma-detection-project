import os

project_root = r"D:\Lymphoma Detection Project"
pages_dir = os.path.join(project_root, "frontend", "src", "pages")
os.makedirs(pages_dir, exist_ok=True)

home_jsx = """import React from 'react';
import { 
  Layers, Activity, Sparkles, ArrowRight, 
  CheckCircle2, AlertTriangle, Cpu, Microscope, FileText, BarChart3 
} from 'lucide-react';
import MedicalDisclaimer from '../components/MedicalDisclaimer';

export default function Home({ setActiveTab }) {
  return (
    <div className="space-y-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <MedicalDisclaimer />

      {/* Hero Section */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950/80 border border-slate-700/80 p-8 sm:p-12 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/3 -mb-12 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-300 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5 text-sky-400" />
            Academic Major Project • Phase-II Rebuild
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Attention Augmented Residual Deep Learning Framework for <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-indigo-300 to-sky-200">Lymphoma Detection</span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed font-normal">
            A specialized computer-aided digital pathology system engineered with <strong>Convolutional Block Attention Modules (CBAM)</strong> and <strong>Two-Stage Screening Logic</strong>. Designed specifically for the 3 malignant lymphoma categories: <strong>CLL</strong>, <strong>FL</strong>, and <strong>MCL</strong>.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              onClick={() => setActiveTab('analysis')}
              className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-sky-500/25 transition-all transform hover:-translate-y-0.5"
            >
              <Layers className="w-4 h-4" />
              Launch Screening Hub
              <ArrowRight className="w-4 h-4 ml-1" />
            </button>

            <button
              onClick={() => setActiveTab('performance')}
              className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-800/90 hover:bg-slate-700/90 border border-slate-700 text-slate-200 font-bold text-sm transition-all"
            >
              <BarChart3 className="w-4 h-4 text-sky-400" />
              View Benchmark Results
            </button>
          </div>
        </div>
      </div>

      {/* Two-Stage Logic Highlight Card */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="rounded-2xl bg-slate-800/50 border border-emerald-500/30 p-6 space-y-4 shadow-lg hover:border-emerald-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="px-3 py-1 rounded-full text-xs font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              Outcome 1 • Accepted
            </span>
            <span className="text-xs text-slate-400 font-mono">Confidence &ge; Threshold</span>
          </div>
          <h3 className="text-xl font-bold text-white">Lymphoma Detected</h3>
          <p className="text-sm text-slate-300 leading-relaxed">
            When microscopic cellular features pass the model's calibrated confidence criteria (&ge; 80%), the system predicts the precise lymphoma subtype (<strong>CLL</strong>, <strong>FL</strong>, or <strong>MCL</strong>), provides exact probability distributions, and overlays a <strong>Grad-CAM++</strong> attention heatmap.
          </p>
        </div>

        <div className="rounded-2xl bg-slate-800/50 border border-amber-500/30 p-6 space-y-4 shadow-lg hover:border-amber-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="px-3 py-1 rounded-full text-xs font-bold uppercase bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
              Outcome 2 • Rejection
            </span>
            <span className="text-xs text-slate-400 font-mono">Confidence &lt; Threshold</span>
          </div>
          <h3 className="text-xl font-bold text-white">No Lymphoma Detected / Rejected</h3>
          <p className="text-sm text-slate-300 leading-relaxed">
            Unlike simplistic argmax classifiers that hallucinate predictions on unrelated slides, our framework guards against false positives by safely returning <strong>"No Lymphoma Detected"</strong> when confidence is insufficient, avoiding forced diagnoses.
          </p>
        </div>
      </div>

      {/* Target Malignant Lymphoma Classes */}
      <div className="space-y-6">
        <div className="text-center space-y-2 max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-white">Three Target Lymphoma Subtypes</h2>
          <p className="text-sm text-slate-400">
            Microscopic histopathological classification from high-resolution TIFF tissue biopsies.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="rounded-2xl bg-slate-800/40 border border-slate-700/60 p-6 space-y-3">
            <div className="w-10 h-10 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 font-bold">
              CLL
            </div>
            <h4 className="text-base font-bold text-white">Chronic Lymphocytic Leukemia</h4>
            <p className="text-xs text-slate-300 leading-relaxed">
              Also termed Small Lymphocytic Lymphoma (SLL). Diffuse proliferation of monotonous small round lymphocytes with dense clumped chromatin.
            </p>
          </div>

          <div className="rounded-2xl bg-slate-800/40 border border-slate-700/60 p-6 space-y-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 font-bold">
              FL
            </div>
            <h4 className="text-base font-bold text-white">Follicular Lymphoma</h4>
            <p className="text-xs text-slate-300 leading-relaxed">
              Prominent nodular architecture composed of a mixture of cleaved centrocytes and larger transformed centroblasts.
            </p>
          </div>

          <div className="rounded-2xl bg-slate-800/40 border border-slate-700/60 p-6 space-y-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 font-bold">
              MCL
            </div>
            <h4 className="text-base font-bold text-white">Mantle Cell Lymphoma</h4>
            <p className="text-xs text-slate-300 leading-relaxed">
              Monotonous lymphoid proliferation with irregular indented nuclear contours and mantle zone expansion.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

with open(os.path.join(pages_dir, "Home.jsx"), "w", encoding="utf-8") as f:
    f.write(home_jsx)
print("Wrote Home.jsx")
