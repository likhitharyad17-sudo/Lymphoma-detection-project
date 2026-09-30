import os

project_root = r"D:\Lymphoma Detection Project"
analysis_path = os.path.join(project_root, "frontend", "src", "pages", "Analysis.jsx")

analysis_jsx = """import React, { useState } from 'react';
import { 
  Upload, Microscope, Activity, Eye, CheckCircle2, AlertTriangle, 
  RefreshCw, Send, Sparkles, FileText, ShieldCheck, Sliders, XCircle 
} from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import { validateImage, predictAndExplain, submitFeedback } from '../services/api';
import MedicalDisclaimer from '../components/MedicalDisclaimer';

export default function Analysis({ onPredictionSuccess }) {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [threshold, setThreshold] = useState(0.80);
  const [loading, setLoading] = useState(false);
  const [validationState, setValidationState] = useState('idle'); // 'idle' | 'checking' | 'valid' | 'invalid'
  const [result, setResult] = useState(null);
  const [viewMode, setViewMode] = useState('overlay'); // 'overlay' | 'heatmap' | 'original'
  const [error, setError] = useState(null);

  // Pathologist Feedback Form
  const [reviewStatus, setReviewStatus] = useState('Verified Correct');
  const [reviewerNotes, setReviewerNotes] = useState('');
  const [reviewerName, setReviewerName] = useState('Pathology Fellow');
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      processSelectedFile(selectedFile);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      processSelectedFile(droppedFile);
    }
  };

  const processSelectedFile = (selectedFile) => {
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResult(null);
    setError(null);
    setValidationState('idle');
    setFeedbackSubmitted(false);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Step 1: Validation Gating Check
      setValidationState('checking');
      const valResponse = await validateImage(file);

      if (!valResponse.is_valid) {
        setValidationState('invalid');
        setError(valResponse.message || 'Invalid image: Please upload a valid histological slide.');
        setLoading(false);
        return;
      }

      // Step 2: Run Two-Stage Screening Model
      setValidationState('valid');
      const data = await predictAndExplain(file, threshold);
      setResult(data);
      if (onPredictionSuccess) onPredictionSuccess();
    } catch (err) {
      console.error(err);
      setValidationState('invalid');
      const msg = err.response?.data?.detail || err.message || 'Image could not be analyzed.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    if (!result?.id && !result?.case_id) return;
    setFeedbackLoading(true);
    try {
      await submitFeedback({
        prediction_id: result.id || 1,
        review_status: reviewStatus,
        notes: reviewerNotes,
        reviewed_by: reviewerName,
      });
      setFeedbackSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setFeedbackLoading(false);
    }
  };

  // Format probabilities for Recharts
  const probsObj = result?.probabilities || result?.top_probabilities || {};
  const chartData = Object.entries(probsObj).map(([name, prob]) => ({
    name,
    probability: Number((prob * 100).toFixed(2)),
    isWinner: name === result?.predicted_subtype,
  }));

  return (
    <div className="space-y-6 animate-fadeIn max-w-7xl mx-auto py-2">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 flex items-center space-x-2.5">
          <Activity className="w-6 h-6 text-sky-600" />
          <span>Histopathology Slide Diagnostic Studio</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Upload a microscopic lymphoid tissue biopsy to perform real-time screening and generate attention-weighted Grad-CAM++ region attribution heatmaps.
        </p>
      </div>

      <MedicalDisclaimer compact />

      {/* Threshold Control Bar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-sky-50 text-sky-600 border border-sky-100">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <div className="text-sm font-bold text-slate-900 flex items-center gap-2">
              Lymphoma Detection Confidence Threshold
              <span className="text-xs font-mono px-2 py-0.5 bg-sky-100 text-sky-800 rounded-full font-bold">
                {(threshold * 100).toFixed(0)}%
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Predictions with maximum probability &lt; {(threshold * 100).toFixed(0)}% are safely rejected as "No Lymphoma Detected".
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-64">
          <span className="text-xs font-mono text-slate-400 font-bold">50%</span>
          <input
            type="range"
            min="0.50"
            max="0.95"
            step="0.05"
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full accent-sky-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
          />
          <span className="text-xs font-mono text-slate-400 font-bold">95%</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Upload & Specimen Loader */}
        <div className="lg:col-span-5 space-y-5">
          <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-4 shadow-xs">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-slate-900">
                Upload a lymphoma test-slide image
              </h2>
              <span className="text-[11px] font-medium text-slate-400">TIFF, PNG, JPG</span>
            </div>

            {/* Drop Zone */}
            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
                previewUrl
                  ? 'border-sky-400 bg-sky-50/40'
                  : 'border-slate-300 hover:border-sky-400 hover:bg-slate-50'
              }`}
            >
              <input
                type="file"
                accept="image/*,.tif,.tiff"
                onChange={handleFileChange}
                className="hidden"
                id="slide-upload"
              />
              <label htmlFor="slide-upload" className="cursor-pointer space-y-3 block">
                {previewUrl ? (
                  <div className="space-y-3">
                    <div className="relative rounded-lg overflow-hidden max-h-56 border border-slate-200 shadow-xs mx-auto">
                      <img src={previewUrl} alt="Slide Preview" className="w-full h-full object-cover" />
                    </div>
                    <div className="text-xs font-mono text-slate-600 truncate max-w-xs mx-auto">
                      {file?.name}
                    </div>
                    <span className="text-xs text-sky-600 font-bold hover:underline inline-block">
                      Click to choose another slide
                    </span>
                  </div>
                ) : (
                  <div className="space-y-2 py-4">
                    <div className="w-12 h-12 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center mx-auto border border-sky-100">
                      <Upload className="w-6 h-6" />
                    </div>
                    <p className="text-sm font-bold text-slate-800">Choose or Drag Histopathology Image</p>
                    <p className="text-xs text-slate-500">Supports standard H&E stained biopsy slides</p>
                  </div>
                )}
              </label>
            </div>

            {/* Validation State Badge */}
            {validationState === 'checking' && (
              <div className="p-3 bg-sky-50 border border-sky-200 rounded-xl text-xs text-sky-800 flex items-center space-x-2">
                <RefreshCw className="w-4 h-4 animate-spin text-sky-600" />
                <span>Validating slide visual gating & cellular contrast...</span>
              </div>
            )}

            {validationState === 'invalid' && error && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-center space-x-2">
                <XCircle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={!file || loading}
              className={`w-full py-3.5 rounded-xl font-bold text-sm flex items-center justify-center space-x-2 transition-all shadow-xs cursor-pointer ${
                !file || loading
                  ? 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200'
                  : 'bg-sky-600 hover:bg-sky-500 text-white shadow-sky-500/20 hover:scale-[1.01]'
              }`}
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Extracting Residual & CBAM Features...</span>
                </>
              ) : (
                <>
                  <Activity className="w-4 h-4" />
                  <span>Execute Diagnostic Analysis</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Diagnostic Results & Explainability */}
        <div className="lg:col-span-7 space-y-5">
          {result ? (
            <div className="space-y-5">
              {/* Positive Outcome Card */}
              {result.outcome === 'LYMPHOMA_DETECTED' && (
                <div className="bg-white border border-slate-200 rounded-2xl p-6 space-y-5 shadow-xs">
                  <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100">
                    <div>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1.5 w-fit">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        Lymphoma Detected
                      </span>
                      <h2 className="text-xl sm:text-2xl font-black text-slate-900 mt-1.5">
                        {result.predicted_subtype_full || result.predicted_subtype}
                      </h2>
                    </div>
                    <div className="text-right">
                      <div className="text-[11px] text-slate-400 font-bold uppercase">Confidence Score</div>
                      <div className="text-2xl sm:text-3xl font-black text-emerald-600 font-mono">
                        {result.confidence_percentage}
                      </div>
                    </div>
                  </div>

                  {/* Multi-view Visualizer */}
                  {result.heatmap_url && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                          Visual Explainability (Grad-CAM++)
                        </span>
                        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
                          {['overlay', 'original'].map((mode) => (
                            <button
                              key={mode}
                              onClick={() => setViewMode(mode)}
                              className={`px-3 py-1 rounded-md font-bold uppercase text-[10px] transition-all cursor-pointer ${
                                viewMode === mode
                                  ? 'bg-white text-sky-700 shadow-xs'
                                  : 'text-slate-500 hover:text-slate-900'
                              }`}
                            >
                              {mode === 'overlay' ? 'Attention Overlay' : 'Original Slide'}
                            </button>
                          ))}
                        </div>
                      </div>

                      <div className="rounded-xl overflow-hidden border border-slate-200 aspect-video bg-slate-900 max-h-72 flex items-center justify-center">
                        <img
                          src={viewMode === 'overlay' ? result.heatmap_url : result.original_url}
                          alt="Visual Result"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </div>
                  )}

                  {/* Softmax Probability Distribution Chart */}
                  <div className="space-y-2">
                    <div className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                      Class Probability Distribution
                    </div>
                    <div className="h-40 w-full pt-2">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={chartData} layout="vertical" margin={{ top: 0, right: 25, left: 35, bottom: 0 }}>
                          <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fontSize: 10, fill: '#64748b' }} />
                          <YAxis dataKey="name" type="category" tick={{ fontSize: 11, fontWeight: 'bold', fill: '#1e293b' }} />
                          <Tooltip formatter={(value) => [`${value}%`, 'Probability']} />
                          <Bar dataKey="probability" radius={[0, 4, 4, 0]}>
                            {chartData.map((entry, index) => (
                              <Cell
                                key={`cell-${index}`}
                                fill={entry.isWinner ? '#0284c7' : '#94a3b8'}
                              />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Morphology Summary */}
                  {result.morphology_summary && (
                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 leading-relaxed space-y-1">
                      <div className="font-bold text-slate-900">Pathological Hallmark:</div>
                      <p>{result.morphology_summary}</p>
                    </div>
                  )}

                  {/* PDF Download Action */}
                  <a
                    href={`/api/reports/${result.case_id}/pdf`}
                    target="_blank"
                    rel="noreferrer"
                    className="w-full py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center justify-center space-x-2 transition-all shadow-xs cursor-pointer"
                  >
                    <FileText className="w-4 h-4 text-sky-400" />
                    <span>Download Clinical PDF Summary Report ({result.case_id})</span>
                  </a>
                </div>
              )}

              {/* Rejected / No Lymphoma Detected Outcome Card */}
              {result.outcome === 'NO_LYMPHOMA_DETECTED' && (
                <div className="bg-white border border-amber-200 rounded-2xl p-6 space-y-5 shadow-xs">
                  <div className="flex items-center gap-3 pb-3 border-b border-amber-100">
                    <div className="p-2.5 bg-amber-100 text-amber-700 rounded-xl">
                      <AlertTriangle className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="px-2 py-0.5 rounded-full text-xs font-bold uppercase bg-amber-100 text-amber-800">
                        Screening Rejection Guard
                      </span>
                      <h2 className="text-xl font-bold text-slate-900 mt-1">
                        No Lymphoma Detected
                      </h2>
                    </div>
                  </div>

                  <div className="text-xs sm:text-sm text-slate-700 leading-relaxed space-y-2">
                    <p>{result.rejection_reason}</p>
                    <p className="text-xs text-slate-500">
                      The confidence score was below the accepted threshold (<strong>{(threshold * 100).toFixed(0)}%</strong>). The model avoided forcing a subtype classification.
                    </p>
                  </div>
                </div>
              )}

              {/* Pathologist Review & Feedback Form */}
              <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                    Pathologist Diagnostic Verification Form
                  </h3>
                  <span className="text-[11px] text-slate-400">Clinical Audit Logging</span>
                </div>

                {feedbackSubmitted ? (
                  <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 flex items-center space-x-2 font-semibold">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>Diagnostic review and notes logged successfully to clinical database.</span>
                  </div>
                ) : (
                  <form onSubmit={handleFeedbackSubmit} className="space-y-3">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="text-[11px] font-bold text-slate-700 block mb-1">Reviewer Name</label>
                        <input
                          type="text"
                          value={reviewerName}
                          onChange={(e) => setReviewerName(e.target.value)}
                          className="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-slate-50 text-slate-900"
                        />
                      </div>
                      <div>
                        <label className="text-[11px] font-bold text-slate-700 block mb-1">Status</label>
                        <select
                          value={reviewStatus}
                          onChange={(e) => setReviewStatus(e.target.value)}
                          className="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-slate-50 text-slate-900"
                        >
                          <option value="Verified Correct">Verified Correct</option>
                          <option value="Misclassified">Misclassified</option>
                          <option value="Needs Further Testing">Needs Flow Cytometry / IHC</option>
                        </select>
                      </div>
                    </div>

                    <div>
                      <label className="text-[11px] font-bold text-slate-700 block mb-1">Pathologist Observations</label>
                      <textarea
                        rows="2"
                        placeholder="Add morphological or clinical commentary..."
                        value={reviewerNotes}
                        onChange={(e) => setReviewerNotes(e.target.value)}
                        className="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-slate-50 text-slate-900"
                      />
                    </div>

                    <button
                      type="submit"
                      disabled={feedbackLoading}
                      className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-lg shadow-xs flex items-center space-x-1.5 cursor-pointer"
                    >
                      <Send className="w-3.5 h-3.5" />
                      <span>{feedbackLoading ? 'Submitting...' : 'Submit Verification Feedback'}</span>
                    </button>
                  </form>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center space-y-3 shadow-xs min-h-[380px] flex flex-col items-center justify-center">
              <div className="w-14 h-14 rounded-2xl bg-slate-50 text-slate-400 flex items-center justify-center mx-auto border border-slate-200">
                <Microscope className="w-7 h-7" />
              </div>
              <h3 className="text-base font-bold text-slate-800">Awaiting Slide Specimen</h3>
              <p className="text-xs text-slate-500 max-w-sm">
                Upload a microscopic histopathology biopsy slide on the left and click Execute Diagnostic Analysis to view attention heatmaps and 3-class lymphoma probabilities.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""

with open(analysis_path, "w", encoding="utf-8") as f:
    f.write(analysis_jsx)

print("Updated Analysis.jsx successfully.")
