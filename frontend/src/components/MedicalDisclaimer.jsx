import React from 'react';
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
