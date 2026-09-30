import os

project_root = r"D:\Lymphoma Detection Project"
pages_dir = os.path.join(project_root, "frontend", "src", "pages")

analysis_jsx = """import React, { useState, useRef } from 'react';
import { 
  UploadCloud, FileImage, CheckCircle2, AlertTriangle, XCircle, 
  Layers, Download, RefreshCw, Sliders, Eye, FileText, ChevronRight 
} from 'lucide-react';
import { api } from '../services/api';
import MedicalDisclaimer from '../components/MedicalDisclaimer';

export default function Analysis() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [threshold, setThreshold] = useState(0.80);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [tabMode, setTabMode] = useState('single');
  
  const [batchFiles, setBatchFiles] = useState([]);
  const [batchResult, setBatchResult] = useState(null);
  const [batchLoading, setBatchLoading] = useState(false);

  const fileInputRef = useRef(null);
  const batchInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('threshold', threshold);

    try {
      const data = await api.predictSingle(formData);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Inference failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBatchAnalyze = async () => {
    if (batchFiles.length === 0) return;
    setBatchLoading(true);
    setBatchResult(null);

    const formData = new FormData();
    for (let i = 0; i < batchFiles.length; i++) {
      formData.append('files', batchFiles[i]);
    }
    formData.append('threshold', threshold);

    try {
      const data = await api.predictBatch(formData);
      setBatchResult(data);
    } catch (err) {
      setError('Batch inference failed.');
    } finally {
      setBatchLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Histopathology Screening Hub</h1>
          <p className="text-sm text-slate-400 mt-1">
            Two-stage automated screening and 3-class lymphoma classification with Grad-CAM++ explainability.
          </p>
        </div>

        <div className="flex items-center gap-1 bg-slate-800/80 p-1 rounded-xl border border-slate-700">
          <button
            onClick={() => setTabMode('single')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
              tabMode === 'single' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            Single Slide Analysis
          </button>
          <button
            onClick={() => setTabMode('batch')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
              tabMode === 'batch' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            Batch Screening
          </button>
        </div>
      </div>

      <MedicalDisclaimer compact />

      {/* Threshold Control Bar */}
      <div className="rounded-2xl bg-slate-800/60 border border-slate-700/80 p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/30">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <div className="text-sm font-bold text-white flex items-center gap-2">
              Lymphoma Detection Confidence Threshold
              <span className="text-xs font-mono px-2 py-0.5 bg-sky-500/20 text-sky-300 rounded-full">
                {(threshold * 100).toFixed(0)}%
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Predictions with maximum probability &lt; {(threshold * 100).toFixed(0)}% are rejected as "No Lymphoma Detected" to avoid out-of-distribution errors.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-64">
          <span className="text-xs font-mono text-slate-400">50%</span>
          <input
            type="range"
            min="0.50"
            max="0.95"
            step="0.05"
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full accent-sky-500 h-2 bg-slate-700 rounded-lg cursor-pointer"
          />
          <span className="text-xs font-mono text-slate-400">95%</span>
        </div>
      </div>

      {tabMode === 'single' ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Upload */}
          <div className="lg:col-span-5 space-y-6">
            <div 
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-3xl p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center min-h-[300px] ${
                previewUrl 
                  ? 'border-sky-500/50 bg-sky-950/10' 
                  : 'border-slate-700 hover:border-sky-500/50 bg-slate-800/40 hover:bg-slate-800/60'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*,.tif,.tiff"
                onChange={handleFileChange}
                className="hidden"
              />

              {previewUrl ? (
                <div className="space-y-4 w-full">
                  <div className="relative rounded-2xl overflow-hidden max-h-60 border border-slate-700 mx-auto shadow-md">
                    <img 
                      src={previewUrl} 
                      alt="Slide Preview" 
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="text-xs text-slate-300 font-mono truncate max-w-xs mx-auto">
                    {selectedFile?.name}
                  </div>
                  <span className="text-xs text-sky-400 font-semibold hover:underline">
                    Click to choose a different slide
                  </span>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="w-14 h-14 rounded-2xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 mx-auto">
                    <UploadCloud className="w-7 h-7" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-white">Upload Histopathology Slide</p>
                    <p className="text-xs text-slate-400 mt-1">Drag and drop TIFF, PNG, or JPG image</p>
                  </div>
                  <span className="inline-block text-xs font-semibold px-3 py-1 bg-slate-700/60 text-slate-300 rounded-full">
                    Recommended: 224x224 to 1388x1040 H&E Stained
                  </span>
                </div>
              )}
            </div>

            <button
              onClick={handleAnalyze}
              disabled={!selectedFile || loading}
              className={`w-full py-4 rounded-2xl font-bold text-sm flex items-center justify-center gap-2 transition-all shadow-xl ${
                !selectedFile || loading
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                  : 'bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white shadow-sky-500/25'
              }`}
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Analyzing Residual & Attention Features...
                </>
              ) : (
                <>
                  <Layers className="w-4 h-4" />
                  Run Screening & Classification
                </>
              )}
            </button>

            {error && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex items-center gap-2">
                <XCircle className="w-4 h-4 text-red-400 shrink-0" />
                <span>{error}</span>
              </div>
            )}
          </div>

          {/* Right Column: Prediction Results */}
          <div className="lg:col-span-7">
            {result ? (
              <div className="space-y-6">
                {/* Result Card: Positive State */}
                {result.outcome === 'LYMPHOMA_DETECTED' && (
                  <div className="rounded-3xl bg-slate-800/60 border border-emerald-500/40 p-6 sm:p-8 space-y-6 shadow-xl">
                    <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-700/60">
                      <div>
                        <span className="px-3 py-1 rounded-full text-xs font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center gap-1.5 w-fit">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                          Lymphoma Detected
                        </span>
                        <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">
                          {result.predicted_subtype_full}
                        </h2>
                      </div>
                      <div className="text-right">
                        <div className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Model Confidence</div>
                        <div className="text-3xl font-extrabold text-emerald-400 font-mono">
                          {result.confidence_percentage}
                        </div>
                      </div>
                    </div>

                    {/* Class Probability Distribution */}
                    <div className="space-y-3">
                      <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                        Three-Class Softmax Probabilities
                      </div>
                      {result.probabilities && Object.entries(result.probabilities).map(([cls, prob]) => (
                        <div key={cls} className="space-y-1">
                          <div className="flex justify-between text-xs font-mono">
                            <span className="font-bold text-slate-200">{cls}</span>
                            <span className="text-slate-400">{(prob * 100).toFixed(2)}%</span>
                          </div>
                          <div className="w-full h-2.5 bg-slate-700/60 rounded-full overflow-hidden">
                            <div 
                              className={`h-full rounded-full transition-all duration-500 ${
                                cls === result.predicted_subtype ? 'bg-emerald-400' : 'bg-sky-600/70'
                              }`}
                              style={{ width: `${prob * 100}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Grad-CAM++ Attention Heatmap Overlay */}
                    {result.heatmap_url && (
                      <div className="space-y-3 pt-2">
                        <div className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center justify-between">
                          <span>Visual Explainability (Grad-CAM++ Attention)</span>
                          <span className="text-[11px] text-sky-400 font-normal">Layer4 CBAM Attention</span>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="space-y-1.5 text-center">
                            <div className="rounded-2xl overflow-hidden border border-slate-700 aspect-video bg-slate-900">
                              <img src={result.original_url} alt="Original" className="w-full h-full object-cover" />
                            </div>
                            <span className="text-[11px] text-slate-400">Original Slide</span>
                          </div>
                          <div className="space-y-1.5 text-center">
                            <div className="rounded-2xl overflow-hidden border border-emerald-500/40 aspect-video bg-slate-900">
                              <img src={result.heatmap_url} alt="Grad-CAM++" className="w-full h-full object-cover" />
                            </div>
                            <span className="text-[11px] text-emerald-300 font-semibold">Cellular Focus Map</span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Morphology Summary */}
                    {result.morphology_summary && (
                      <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-700/60 text-xs text-slate-300 leading-relaxed">
                        <div className="font-bold text-slate-200 mb-1">Pathological Hallmark Characteristics:</div>
                        {result.morphology_summary}
                      </div>
                    )}

                    {/* PDF Export Button */}
                    <div className="pt-2">
                      <a
                        href={`/api/reports/${result.case_id}/pdf`}
                        target="_blank"
                        rel="noreferrer"
                        className="w-full py-3 rounded-xl bg-slate-700 hover:bg-slate-600 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all"
                      >
                        <FileText className="w-4 h-4 text-sky-400" />
                        Download Clinical PDF Summary Report ({result.case_id})
                      </a>
                    </div>
                  </div>
                )}

                {/* Result Card: Rejection State */}
                {result.outcome === 'NO_LYMPHOMA_DETECTED' && (
                  <div className="rounded-3xl bg-slate-800/60 border border-amber-500/40 p-6 sm:p-8 space-y-6 shadow-xl">
                    <div className="flex items-center gap-3 pb-4 border-b border-slate-700/60">
                      <div className="p-3 bg-amber-500/20 text-amber-400 rounded-2xl border border-amber-500/40">
                        <AlertTriangle className="w-8 h-8" />
                      </div>
                      <div>
                        <span className="px-3 py-1 rounded-full text-xs font-bold uppercase bg-amber-500/20 text-amber-300 border border-amber-500/40">
                          Rejection Notice
                        </span>
                        <h2 className="text-2xl font-extrabold text-white mt-1">
                          No Lymphoma Detected
                        </h2>
                      </div>
                    </div>

                    <div className="space-y-3 text-sm text-amber-200/90 leading-relaxed">
                      <p>
                        {result.rejection_reason}
                      </p>
                      <p className="text-xs text-slate-400">
                        The framework's rejection guard refused to force a subtype classification because the maximum softmax probability failed to meet the required threshold (<strong>{(threshold*100).toFixed(0)}%</strong>).
                      </p>
                    </div>

                    {result.probabilities && (
                      <div className="space-y-2 pt-2 border-t border-slate-700/60">
                        <div className="text-xs font-bold text-slate-300 uppercase">Sub-Threshold Probabilities:</div>
                        <div className="grid grid-cols-3 gap-2 text-xs font-mono">
                          <div className="p-2 bg-slate-900 rounded-lg border border-slate-700 text-center">
                            CLL: {(result.probabilities.CLL * 100).toFixed(1)}%
                          </div>
                          <div className="p-2 bg-slate-900 rounded-lg border border-slate-700 text-center">
                            FL: {(result.probabilities.FL * 100).toFixed(1)}%
                          </div>
                          <div className="p-2 bg-slate-900 rounded-lg border border-slate-700 text-center">
                            MCL: {(result.probabilities.MCL * 100).toFixed(1)}%
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Result Card: Unable to Analyze State */}
                {result.outcome === 'UNABLE_TO_ANALYZE' && (
                  <div className="rounded-3xl bg-slate-800/60 border border-red-500/40 p-6 sm:p-8 space-y-4 shadow-xl">
                    <div className="flex items-center gap-3">
                      <div className="p-3 bg-red-500/20 text-red-400 rounded-2xl border border-red-500/40">
                        <XCircle className="w-8 h-8" />
                      </div>
                      <div>
                        <h2 className="text-2xl font-extrabold text-white">Unable to Analyze Image</h2>
                        <p className="text-xs text-red-300 mt-1">{result.rejection_reason}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="h-full rounded-3xl bg-slate-800/30 border border-slate-700/60 p-12 flex flex-col items-center justify-center text-center space-y-4 text-slate-400">
                <div className="w-16 h-16 rounded-3xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-500">
                  <Layers className="w-8 h-8" />
                </div>
                <div className="max-w-sm space-y-1">
                  <h3 className="text-base font-bold text-slate-200">Awaiting Slide Upload</h3>
                  <p className="text-xs text-slate-400">
                    Upload a histopathology slide on the left and click Run Screening to visualize attention activation maps and subtype classification.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="rounded-3xl bg-slate-800/40 border border-slate-700 p-8 text-center space-y-4">
            <input
              ref={batchInputRef}
              type="file"
              multiple
              accept="image/*,.tif,.tiff"
              onChange={(e) => setBatchFiles(Array.from(e.target.files))}
              className="hidden"
            />
            <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mx-auto">
              <FileImage className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Batch Histopathology Screening</h3>
              <p className="text-xs text-slate-400 mt-1">Select multiple slides for high-throughput screening</p>
            </div>
            <button
              onClick={() => batchInputRef.current?.click()}
              className="px-6 py-2.5 rounded-xl bg-slate-700 hover:bg-slate-600 text-white font-bold text-xs"
            >
              Select Images ({batchFiles.length} selected)
            </button>

            {batchFiles.length > 0 && (
              <div className="pt-2">
                <button
                  onClick={handleBatchAnalyze}
                  disabled={batchLoading}
                  className="px-8 py-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-bold text-xs shadow-lg shadow-sky-500/25"
                >
                  {batchLoading ? 'Processing Batch...' : `Run Analysis on ${batchFiles.length} Slides`}
                </button>
              </div>
            )}
          </div>

          {batchResult && (
            <div className="rounded-3xl bg-slate-800/60 border border-slate-700 p-6 space-y-4">
              <div className="grid grid-cols-4 gap-4 text-center">
                <div className="p-3 bg-slate-900 rounded-xl border border-slate-700">
                  <div className="text-xs text-slate-400">Total Processed</div>
                  <div className="text-xl font-bold text-white">{batchResult.total_processed}</div>
                </div>
                <div className="p-3 bg-slate-900 rounded-xl border border-emerald-500/30">
                  <div className="text-xs text-emerald-400">Lymphoma Detected</div>
                  <div className="text-xl font-bold text-emerald-300">{batchResult.lymphoma_detected_count}</div>
                </div>
                <div className="p-3 bg-slate-900 rounded-xl border border-amber-500/30">
                  <div className="text-xs text-amber-400">Rejected (No Lymphoma)</div>
                  <div className="text-xl font-bold text-amber-300">{batchResult.rejected_count}</div>
                </div>
                <div className="p-3 bg-slate-900 rounded-xl border border-red-500/30">
                  <div className="text-xs text-red-400">Invalid / Corrupt</div>
                  <div className="text-xl font-bold text-red-300">{batchResult.invalid_count}</div>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left text-slate-300">
                  <thead className="bg-slate-900 text-slate-400 uppercase font-semibold">
                    <tr>
                      <th className="p-3">Case ID</th>
                      <th className="p-3">Filename</th>
                      <th className="p-3">Outcome</th>
                      <th className="p-3">Predicted Subtype</th>
                      <th className="p-3">Confidence</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700/60 font-mono">
                    {batchResult.results.map((r) => (
                      <tr key={r.case_id} className="hover:bg-slate-700/30">
                        <td className="p-3 font-bold text-sky-400">{r.case_id}</td>
                        <td className="p-3">{r.file_name}</td>
                        <td className="p-3">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            r.outcome === 'LYMPHOMA_DETECTED' ? 'bg-emerald-500/20 text-emerald-300' :
                            r.outcome === 'NO_LYMPHOMA_DETECTED' ? 'bg-amber-500/20 text-amber-300' : 'bg-red-500/20 text-red-300'
                          }`}>
                            {r.outcome}
                          </span>
                        </td>
                        <td className="p-3 font-sans font-semibold">{r.predicted_subtype || 'N/A'}</td>
                        <td className="p-3">{r.confidence_percentage || 'N/A'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
"""

with open(os.path.join(pages_dir, "Analysis.jsx"), "w", encoding="utf-8") as f:
    f.write(analysis_jsx)
print("Wrote Analysis.jsx")
