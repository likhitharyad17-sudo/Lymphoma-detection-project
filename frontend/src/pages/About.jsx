import React from 'react';
import { BookOpen, Layers, Microscope, Sparkles, BrainCircuit, Activity } from 'lucide-react';
import MedicalDisclaimer from '../components/MedicalDisclaimer';

export default function About() {
  return (
    <div className="space-y-10 max-w-6xl mx-auto py-2 animate-fadeIn">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Clinical Pathology & Mathematical Theory</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Histological hallmarks of target lymphomas and mathematical formulation of Attention-Augmented Residual Learning.
        </p>
      </div>

      <MedicalDisclaimer />

      {/* 3 Lymphoma Histology Profiles */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <Microscope className="w-5 h-5 text-sky-600" />
          <span>Histological & Cellular Morphology Profiles</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* CLL */}
          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
            <span className="px-2.5 py-0.5 bg-sky-50 text-sky-700 rounded-full text-xs font-bold border border-sky-200">
              Class 0 • CLL / SLL
            </span>
            <h3 className="text-base font-bold text-slate-900">Chronic Lymphocytic Leukemia</h3>
            <div className="space-y-2 text-xs text-slate-600 leading-relaxed font-normal">
              <p><strong>Cellular Composition:</strong> Monotonous proliferation of small, round, mature-appearing B-lymphocytes.</p>
              <p><strong>Nuclear Characteristics:</strong> Dense, heavily clumped "soccer-ball" chromatin with indistinct or absent nucleoli and very scant cytoplasm.</p>
              <p><strong>Tissue Architecture:</strong> Diffuse pattern effacing nodal architecture with pale pseudofollicles (proliferation centers).</p>
              <p><strong>Immunophenotype:</strong> CD5+, CD19+, CD20+ (dim), CD23+, Cyclin D1-.</p>
            </div>
          </div>

          {/* FL */}
          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
            <span className="px-2.5 py-0.5 bg-indigo-50 text-indigo-700 rounded-full text-xs font-bold border border-indigo-200">
              Class 1 • FL
            </span>
            <h3 className="text-base font-bold text-slate-900">Follicular Lymphoma</h3>
            <div className="space-y-2 text-xs text-slate-600 leading-relaxed font-normal">
              <p><strong>Cellular Composition:</strong> Mixture of cleaved centrocytes and transformed centroblasts.</p>
              <p><strong>Nuclear Characteristics:</strong> Centrocytes feature angular, notched, or deeply cleaved nuclear contours. Centroblasts feature vesicular nuclei with peripheral nucleoli.</p>
              <p><strong>Tissue Architecture:</strong> Closely packed, back-to-back neoplastic follicles lacking normal polarized mantle zones.</p>
              <p><strong>Immunophenotype:</strong> CD10+, BCL2+ (translocation t(14;18)), CD20+, BCL6+.</p>
            </div>
          </div>

          {/* MCL */}
          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
            <span className="px-2.5 py-0.5 bg-purple-50 text-purple-700 rounded-full text-xs font-bold border border-purple-200">
              Class 2 • MCL
            </span>
            <h3 className="text-base font-bold text-slate-900">Mantle Cell Lymphoma</h3>
            <div className="space-y-2 text-xs text-slate-600 leading-relaxed font-normal">
              <p><strong>Cellular Composition:</strong> Monotonous population of small-to-medium lymphocytes resembling mantle zone B-cells.</p>
              <p><strong>Nuclear Characteristics:</strong> Irregular, indented nuclear membranes with condensed chromatin (lacks transformed centroblasts).</p>
              <p><strong>Tissue Architecture:</strong> Mantle zone, nodular, or diffuse expansion with hyalinized blood vessels.</p>
              <p><strong>Immunophenotype:</strong> CD5+, CD20+, Cyclin D1+ (translocation t(11;14) CCND1::IGH), SOX11+, CD23-.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Mathematical Formulations */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <BrainCircuit className="w-5 h-5 text-indigo-600" />
          <span>Attention Mechanism Mathematical Formulations</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-2 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900">1. Channel Attention Module (CAM)</h3>
            <p className="text-xs text-slate-600 leading-relaxed font-normal">
              Combines Global Average Pooling (GAP) and Global Max Pooling (GMP) through a shared MLP with reduction ratio r=16:
            </p>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-sky-800">
              M_c(F) = &sigma;( MLP(AvgPool(F)) + MLP(MaxPool(F)) )
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-2 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900">2. Spatial Attention Module (SAM)</h3>
            <p className="text-xs text-slate-600 leading-relaxed font-normal">
              Applies a 7x7 spatial convolution across inter-channel pooled feature maps:
            </p>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-indigo-800">
              M_s(F') = &sigma;( f^(7x7)( [AvgPool(F'); MaxPool(F')] ) )
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-2 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900">3. Grad-CAM++ Explainability</h3>
            <p className="text-xs text-slate-600 leading-relaxed font-normal">
              Computes higher-order partial derivative weights to map cellular clusters:
            </p>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-emerald-800">
              L_(Grad-CAM++)^c = ReLU( &Sigma;_k w_k^c &middot; A^k )
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-2 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900">4. Two-Stage Confidence Screening</h3>
            <p className="text-xs text-slate-600 leading-relaxed font-normal">
              Confidence threshold decision rule guarding against out-of-distribution slides:
            </p>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-amber-800">
              Outcome = Lymphoma Detected (if max P &ge; 0.80)<br/>
              Outcome = No Lymphoma Detected (if max P &lt; 0.80)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
