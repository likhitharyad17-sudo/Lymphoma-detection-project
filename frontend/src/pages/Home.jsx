import React from 'react';
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
            onClick={() => setActiveTab('chat')}
            className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-white hover:bg-slate-50 text-slate-700 font-semibold px-6 py-3 rounded-xl border border-slate-200 shadow-xs transition-all text-sm cursor-pointer"
          >
            <Sparkles className="w-4 h-4 text-sky-600" />
            <span>Gemini AI Assistant</span>
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
