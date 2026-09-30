import React, { useState, useEffect } from 'react';
import { 
  History, Download, Trash2, Search, Filter, RefreshCw, FileText, 
  CheckCircle2, AlertTriangle, Eye, EyeOff, Lock, Globe, Shield, User 
} from 'lucide-react';
import { getHistory, deleteCase, clearHistory, toggleAdminVisibility, toggleUserPrivacy } from '../services/api';

export default function HistoryPage({ user }) {
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [outcomeFilter, setOutcomeFilter] = useState('');
  const [filterMode, setFilterMode] = useState('all');
  const [actionMsg, setActionMsg] = useState(null);

  const isAdmin = user?.role === 'ADMIN';
  const currentUserId = user?.id;

  const showNotification = (msg) => {
    setActionMsg(msg);
    setTimeout(() => setActionMsg(null), 4000);
  };

  const fetchHistory = () => {
    setLoading(true);
    getHistory({ 
      outcome: outcomeFilter || undefined, 
      filter_mode: filterMode,
      limit: 100 
    })
      .then(res => {
        setRecords(res.records || []);
        setTotal(res.total || 0);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory();
  }, [outcomeFilter, filterMode]);

  const handleAdminToggleVisibility = async (caseId, currentHiddenState) => {
    try {
      const res = await toggleAdminVisibility(caseId, !currentHiddenState);
      showNotification(res.message);
      fetchHistory();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update display visibility.");
    }
  };

  const handleUserTogglePrivacy = async (caseId, currentPrivacyState) => {
    try {
      const res = await toggleUserPrivacy(caseId, !currentPrivacyState);
      showNotification(res.message);
      fetchHistory();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update test privacy.");
    }
  };

  const handleDelete = async (caseId) => {
    if (window.confirm(`Are you sure you want to delete record ${caseId}?`)) {
      try {
        await deleteCase(caseId);
        showNotification(`Record ${caseId} deleted successfully.`);
        fetchHistory();
      } catch (err) {
        alert(err.response?.data?.detail || "Failed to delete record.");
      }
    }
  };

  const handleClearAll = async () => {
    if (window.confirm("WARNING: Are you sure you want to permanently clear all history records?")) {
      try {
        await clearHistory();
        showNotification("All history records cleared.");
        fetchHistory();
      } catch (err) {
        alert(err.response?.data?.detail || "Failed to clear records.");
      }
    }
  };

  const filtered = records.filter(r => 
    r.case_id?.toLowerCase().includes(search.toLowerCase()) ||
    r.file_name?.toLowerCase().includes(search.toLowerCase()) ||
    r.predicted_subtype?.toLowerCase().includes(search.toLowerCase()) ||
    r.user_name?.toLowerCase().includes(search.toLowerCase()) ||
    r.user_email?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6 max-w-7xl mx-auto py-2 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Case Audit History & Test Logs</h1>
            {isAdmin ? (
              <span className="text-xs font-bold uppercase px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-800 border border-rose-200">
                Administrator Access
              </span>
            ) : user ? (
              <span className="text-xs font-bold uppercase px-2.5 py-0.5 rounded-full bg-sky-50 text-sky-800 border border-sky-200">
                Researcher View
              </span>
            ) : null}
          </div>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            {isAdmin 
              ? "Full administrator console: inspect, modify display visibility (hide/unhide), and manage all historical records."
              : "Review historical specimen results and accuracy. Manage your own test privacy and records."}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchHistory}
            className="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs border border-slate-200 shadow-xs flex items-center gap-2 cursor-pointer"
          >
            <RefreshCw className="w-3.5 h-3.5 text-sky-600" />
            <span>Refresh</span>
          </button>
          {isAdmin && records.length > 0 && (
            <button
              onClick={handleClearAll}
              className="px-3.5 py-2 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold text-xs border border-rose-200 shadow-xs flex items-center gap-2 cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear All Logs</span>
            </button>
          )}
        </div>
      </div>

      {/* Action Notification */}
      {actionMsg && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{actionMsg}</span>
        </div>
      )}

      {/* Filter Mode Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2 overflow-x-auto">
        <button
          onClick={() => setFilterMode('all')}
          className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
            filterMode === 'all'
              ? 'bg-sky-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
          }`}
        >
          All Visible Tests ({total})
        </button>

        {user && (
          <button
            onClick={() => setFilterMode('my_tests')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
              filterMode === 'my_tests'
                ? 'bg-sky-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            <User className="w-3.5 h-3.5" />
            <span>My Personal Tests</span>
          </button>
        )}

        <button
          onClick={() => setFilterMode('public')}
          className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
            filterMode === 'public'
              ? 'bg-sky-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
          }`}
        >
          <Globe className="w-3.5 h-3.5" />
          <span>Public Community Tests</span>
        </button>

        {isAdmin && (
          <button
            onClick={() => setFilterMode('hidden')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
              filterMode === 'hidden'
                ? 'bg-amber-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            <EyeOff className="w-3.5 h-3.5" />
            <span>Hidden by Admin</span>
          </button>
        )}
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-12 gap-3">
        <div className="sm:col-span-8 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search by Case ID, Filename, Subtype, or Investigator..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-sky-500 shadow-xs"
          />
        </div>

        <div className="sm:col-span-4">
          <select
            value={outcomeFilter}
            onChange={(e) => setOutcomeFilter(e.target.value)}
            className="w-full py-2 px-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-700 focus:outline-none focus:border-sky-500 shadow-xs cursor-pointer"
          >
            <option value="">All Outcomes</option>
            <option value="LYMPHOMA_DETECTED">Lymphoma Detected Only</option>
            <option value="NO_LYMPHOMA_DETECTED">No Lymphoma Detected (Rejected)</option>
            <option value="UNABLE_TO_ANALYZE">Unable to Analyze</option>
          </select>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left text-slate-700">
            <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3.5">Case Reference</th>
                <th className="p-3.5">Investigator</th>
                <th className="p-3.5">Outcome</th>
                <th className="p-3.5">Subtype</th>
                <th className="p-3.5">Confidence</th>
                <th className="p-3.5">Status & Privacy</th>
                <th className="p-3.5 text-right">Actions & Controls</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {filtered.length > 0 ? (
                filtered.map((r) => {
                  const isOwner = user && r.user_id === currentUserId;
                  return (
                    <tr key={r.case_id} className="hover:bg-slate-50 transition-colors">
                      <td className="p-3.5 font-bold text-sky-700">
                        <div>{r.case_id}</div>
                        <div className="text-[10px] text-slate-400 font-normal truncate max-w-[140px]">{r.file_name}</div>
                      </td>
                      <td className="p-3.5 font-sans">
                        <div className="font-bold text-slate-900">{r.user_name || 'Anonymous Guest'}</div>
                        <div className="text-[10px] text-slate-400">{r.user_email || '—'}</div>
                      </td>
                      <td className="p-3.5">
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          r.outcome === 'LYMPHOMA_DETECTED' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                          r.outcome === 'NO_LYMPHOMA_DETECTED' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                          'bg-rose-50 text-rose-700 border border-rose-200'
                        }`}>
                          {r.outcome}
                        </span>
                      </td>
                      <td className="p-3.5 font-sans font-semibold text-slate-900">
                        {r.predicted_subtype || '—'}
                      </td>
                      <td className="p-3.5 text-emerald-700 font-bold">
                        {r.confidence ? `${(r.confidence * 100).toFixed(2)}%` : '—'}
                      </td>
                      <td className="p-3.5 font-sans">
                        <div className="flex flex-col gap-1">
                          {r.is_hidden_by_admin && (
                            <span className="px-2 py-0.5 rounded text-[10px] bg-rose-50 text-rose-700 border border-rose-200 font-bold flex items-center gap-1 w-fit">
                              <EyeOff className="w-3 h-3" />
                              Hidden by Admin
                            </span>
                          )}
                          {r.is_private ? (
                            <span className="px-2 py-0.5 rounded text-[10px] bg-slate-100 text-slate-700 border border-slate-200 font-bold flex items-center gap-1 w-fit">
                              <Lock className="w-3 h-3 text-slate-500" />
                              Private (Only You & Admin)
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded text-[10px] bg-sky-50 text-sky-700 border border-sky-100 font-bold flex items-center gap-1 w-fit">
                              <Globe className="w-3 h-3 text-sky-500" />
                              Public
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="p-3.5 text-right space-x-1.5 font-sans">
                        <a
                          href={`/api/reports/${r.case_id}/pdf`}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-bold"
                          title="Download PDF Summary"
                        >
                          <FileText className="w-3.5 h-3.5 text-sky-600" />
                          <span>PDF</span>
                        </a>

                        {isOwner && (
                          <button
                            onClick={() => handleUserTogglePrivacy(r.case_id, r.is_private)}
                            className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg text-[11px] font-bold border transition-colors cursor-pointer ${
                              r.is_private
                                ? 'bg-sky-50 hover:bg-sky-100 text-sky-700 border-sky-200'
                                : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border-slate-200'
                            }`}
                            title={r.is_private ? "Make Public to Community" : "Make Private (Only You & Admin can see)"}
                          >
                            {r.is_private ? <Globe className="w-3 h-3" /> : <Lock className="w-3 h-3" />}
                            <span>{r.is_private ? "Make Public" : "Keep Private"}</span>
                          </button>
                        )}

                        {isAdmin && (
                          <button
                            onClick={() => handleAdminToggleVisibility(r.case_id, r.is_hidden_by_admin)}
                            className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg text-[11px] font-bold border transition-colors cursor-pointer ${
                              r.is_hidden_by_admin
                                ? 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border-emerald-200'
                                : 'bg-amber-50 hover:bg-amber-100 text-amber-700 border-amber-200'
                            }`}
                            title={r.is_hidden_by_admin ? "Unhide and display to users" : "Hide from users without deleting"}
                          >
                            {r.is_hidden_by_admin ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                            <span>{r.is_hidden_by_admin ? "Unhide" : "Hide from Users"}</span>
                          </button>
                        )}

                        {(isAdmin || isOwner) && (
                          <button
                            onClick={() => handleDelete(r.case_id)}
                            className="inline-flex items-center p-1.5 rounded-lg hover:bg-rose-50 text-slate-400 hover:text-rose-600 cursor-pointer"
                            title="Delete Record"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="7" className="p-12 text-center text-slate-400 font-sans">
                    No clinical audit records found matching the active filter.
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
