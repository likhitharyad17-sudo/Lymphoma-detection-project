import React, { useState, useEffect } from 'react';
import { 
  Settings, Cpu, HardDrive, Sliders, ShieldCheck, RefreshCw, 
  CheckCircle2, Users, UserCheck, UserX, Clock, Trash2, 
  Search, Filter, AlertTriangle, ShieldAlert, Power, Activity
} from 'lucide-react';
import { 
  getHealth, getThreshold, updateThreshold, 
  getAdminUsers, updateUserStatus, deleteUser 
} from '../services/api';

export default function AdminDashboard({ adminUser, setActiveTab }) {
  // System & Model state
  const [health, setHealth] = useState(null);
  const [threshold, setThreshold] = useState(0.80);
  const [savedMsg, setSavedMsg] = useState(null);
  const [loading, setLoading] = useState(true);

  // User Management state
  const [usersData, setUsersData] = useState({
    total: 0,
    active_count: 0,
    inactive_count: 0,
    disabled_count: 0,
    users: []
  });
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [actionMsg, setActionMsg] = useState(null);
  const [actionErr, setActionErr] = useState(null);
  const [deleteModalUser, setDeleteModalUser] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const fetchStatus = () => {
    setLoading(true);
    Promise.all([getHealth(), getThreshold()])
      .then(([h, t]) => {
        setHealth(h);
        setThreshold(t.current_threshold);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  const fetchUsersList = async () => {
    setLoadingUsers(true);
    try {
      const params = {};
      if (searchTerm.trim()) params.search = searchTerm.trim();
      if (roleFilter !== 'ALL') params.role = roleFilter;
      if (statusFilter !== 'ALL') params.status = statusFilter;

      const data = await getAdminUsers(params);
      setUsersData(data);
    } catch (err) {
      console.error('Failed to load users:', err);
    } finally {
      setLoadingUsers(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    fetchUsersList();
  }, []);

  const handleUpdateThreshold = async () => {
    try {
      const res = await updateThreshold(threshold);
      setSavedMsg(res.message);
      setTimeout(() => setSavedMsg(null), 4000);
    } catch (err) {
      alert('Failed to update threshold');
    }
  };

  const handleToggleStatus = async (user) => {
    const newStatus = user.status === 'DISABLED' ? 'ACTIVE' : 'DISABLED';
    try {
      await updateUserStatus(user.id, newStatus);
      setActionMsg(`User account '${user.email}' is now ${newStatus}.`);
      setTimeout(() => setActionMsg(null), 4000);
      fetchUsersList();
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Failed to update user status';
      setActionErr(errMsg);
      setTimeout(() => setActionErr(null), 4000);
    }
  };

  const handleConfirmDelete = async () => {
    if (!deleteModalUser) return;
    setDeleting(true);
    try {
      await deleteUser(deleteModalUser.id);
      setActionMsg(`User '${deleteModalUser.email}' was permanently deleted.`);
      setTimeout(() => setActionMsg(null), 4000);
      setDeleteModalUser(null);
      fetchUsersList();
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Failed to delete user';
      setActionErr(errMsg);
      setTimeout(() => setActionErr(null), 4000);
    } finally {
      setDeleting(false);
    }
  };

  const formatTimeAgo = (days) => {
    if (days === 0) return 'Active today';
    if (days === 1) return 'Yesterday';
    if (days < 30) return `${days} days ago`;
    return `${days} days inactive`;
  };

  return (
    <div className="space-y-10 max-w-6xl mx-auto py-2 animate-fadeIn">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
          <ShieldAlert className="w-7 h-7 text-sky-600" />
          <span>Clinical & System Admin Console</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Hardware monitoring, threshold calibration, and user account lifecycle management.
        </p>
      </div>

      {/* Notifications */}
      {actionMsg && (
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs sm:text-sm font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{actionMsg}</span>
        </div>
      )}
      {actionErr && (
        <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs sm:text-sm font-semibold flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{actionErr}</span>
        </div>
      )}

      {/* 1. Hardware Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-sky-50 text-sky-600 border border-sky-100">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Accelerator Device</div>
              <div className="text-sm font-bold text-slate-900 truncate max-w-[180px]">
                {health?.hardware?.gpu_name || 'NVIDIA RTX 4050'}
              </div>
            </div>
          </div>
          <div className="text-xs text-slate-500 font-mono">
            VRAM: {health?.hardware?.gpu_memory_gb || 6.44} GB • CUDA: Active
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-purple-50 text-purple-600 border border-purple-100">
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Active Model Version</div>
              <div className="text-sm font-bold text-slate-900">model_v2_15000</div>
            </div>
          </div>
          <div className="text-xs text-slate-500 font-mono">
            CBAM Attention ResNet-50
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-indigo-50 text-indigo-600 border border-indigo-100">
              <HardDrive className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Primary Dataset Size</div>
              <div className="text-sm font-bold text-slate-900">15,000 Images</div>
            </div>
          </div>
          <div className="text-xs text-slate-500 font-mono">
            5,000 CLL • 5,000 FL • 5,000 MCL
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-100">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Classification Scope</div>
              <div className="text-sm font-bold text-slate-900">CLL • FL • MCL</div>
            </div>
          </div>
          <div className="text-xs text-slate-500 font-mono">
            Two-Stage Screening Active
          </div>
        </div>
      </div>

      {/* 2. Threshold Calibration Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 space-y-5 shadow-xs max-w-2xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-sky-50 text-sky-600 rounded-xl border border-sky-100">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Live Confidence Rejection Threshold Tuning</h3>
            <p className="text-xs text-slate-500">
              Calibrate sensitivity to reject low-confidence or ambiguous histological specimens.
            </p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700">Active Threshold:</span>
            <span className="text-2xl font-black text-sky-600 font-mono">
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
            className="w-full accent-sky-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
          />

          <div className="flex justify-between text-xs text-slate-400 font-mono font-medium">
            <span>50% (High Recall)</span>
            <span>80% (Recommended)</span>
            <span>95% (High Specificity)</span>
          </div>
        </div>

        <div className="flex items-center gap-3 pt-2">
          <button
            onClick={handleUpdateThreshold}
            className="px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-xs transition-all cursor-pointer"
          >
            Apply & Save Threshold
          </button>

          {savedMsg && (
            <div className="text-xs text-emerald-700 flex items-center gap-1.5 font-bold">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>{savedMsg}</span>
            </div>
          )}
        </div>
      </div>

      {/* 3. USER MANAGEMENT CONSOLE */}
      <div className="space-y-6 pt-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Users className="w-5 h-5 text-indigo-600" />
              <span>User Account & Access Management</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Monitor active sessions, inspect user activity, disable accounts, and safely delete inactive accounts.
            </p>
          </div>

          <button
            onClick={fetchUsersList}
            disabled={loadingUsers}
            className="flex items-center space-x-1.5 px-3.5 py-2 text-xs font-bold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-xl shadow-xs transition-all cursor-pointer w-fit"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${loadingUsers ? 'animate-spin' : ''}`} />
            <span>Refresh User Directory</span>
          </button>
        </div>

        {/* User Metric Summary */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500">Total Users</span>
              <Users className="w-4 h-4 text-slate-400" />
            </div>
            <div className="text-2xl font-black text-slate-900 font-mono mt-2">
              {usersData.total}
            </div>
          </div>

          <div className="bg-white border border-emerald-200/80 rounded-2xl p-4 shadow-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-emerald-700">Active Accounts</span>
              <UserCheck className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-2xl font-black text-emerald-700 font-mono mt-2">
              {usersData.active_count}
            </div>
          </div>

          <div className="bg-white border border-amber-200/80 rounded-2xl p-4 shadow-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-amber-700">Inactive (&gt;30d)</span>
              <Clock className="w-4 h-4 text-amber-600" />
            </div>
            <div className="text-2xl font-black text-amber-700 font-mono mt-2">
              {usersData.inactive_count}
            </div>
          </div>

          <div className="bg-white border border-rose-200/80 rounded-2xl p-4 shadow-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-rose-700">Disabled</span>
              <UserX className="w-4 h-4 text-rose-600" />
            </div>
            <div className="text-2xl font-black text-rose-700 font-mono mt-2">
              {usersData.disabled_count}
            </div>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Search by name or email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') fetchUsersList(); }}
              className="w-full pl-9 pr-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-sky-500"
            />
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto">
            <select
              value={roleFilter}
              onChange={(e) => { setRoleFilter(e.target.value); }}
              className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 focus:outline-none cursor-pointer"
            >
              <option value="ALL">All Roles</option>
              <option value="USER">Standard Users</option>
              <option value="ADMIN">Administrators</option>
            </select>

            <select
              value={statusFilter}
              onChange={(e) => { setStatusFilter(e.target.value); }}
              className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 focus:outline-none cursor-pointer"
            >
              <option value="ALL">All Statuses</option>
              <option value="ACTIVE">Active Only</option>
              <option value="INACTIVE">Inactive (&gt;30d)</option>
              <option value="DISABLED">Disabled</option>
            </select>

            <button
              onClick={fetchUsersList}
              className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold rounded-xl transition-all shadow-xs cursor-pointer"
            >
              Filter
            </button>
          </div>
        </div>

        {/* Users Table */}
        <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-bold uppercase tracking-wider">
                <tr>
                  <th className="px-5 py-3.5">User Identity</th>
                  <th className="px-4 py-3.5">Role</th>
                  <th className="px-4 py-3.5">Status</th>
                  <th className="px-4 py-3.5">Activity</th>
                  <th className="px-4 py-3.5 text-center">Predictions</th>
                  <th className="px-4 py-3.5">Registered</th>
                  <th className="px-5 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {usersData.users.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-10 text-center text-slate-400">
                      No matching user accounts found.
                    </td>
                  </tr>
                ) : (
                  usersData.users.map((u) => {
                    const isSelf = u.id === adminUser?.id;
                    const initial = u.full_name?.charAt(0)?.toUpperCase() || 'U';
                    return (
                      <tr key={u.id} className="hover:bg-slate-50/80 transition-colors">
                        {/* User Identity */}
                        <td className="px-5 py-3.5">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 text-white font-bold flex items-center justify-center text-xs shadow-xs shrink-0">
                              {initial}
                            </div>
                            <div>
                              <div className="font-bold text-slate-900 flex items-center gap-1.5">
                                <span>{u.full_name}</span>
                                {isSelf && (
                                  <span className="text-[10px] px-1.5 py-0.2 rounded bg-sky-100 text-sky-800 font-bold">You</span>
                                )}
                              </div>
                              <div className="text-slate-400 font-mono text-[11px]">{u.email}</div>
                            </div>
                          </div>
                        </td>

                        {/* Role */}
                        <td className="px-4 py-3.5">
                          <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                            u.role === 'ADMIN'
                              ? 'bg-rose-50 text-rose-700 border border-rose-200'
                              : 'bg-sky-50 text-sky-700 border border-sky-200'
                          }`}>
                            {u.role}
                          </span>
                        </td>

                        {/* Status */}
                        <td className="px-4 py-3.5">
                          {u.status === 'ACTIVE' && (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                              ACTIVE
                            </span>
                          )}
                          {u.status === 'INACTIVE' && (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">
                              <Clock className="w-3 h-3 text-amber-600" />
                              INACTIVE (&gt;30d)
                            </span>
                          )}
                          {u.status === 'DISABLED' && (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                              <UserX className="w-3 h-3 text-rose-600" />
                              DISABLED
                            </span>
                          )}
                        </td>

                        {/* Activity */}
                        <td className="px-4 py-3.5 text-slate-600 font-medium">
                          {u.days_inactive !== null && u.days_inactive !== undefined
                            ? formatTimeAgo(u.days_inactive)
                            : 'No logins'}
                        </td>

                        {/* Prediction count */}
                        <td className="px-4 py-3.5 text-center font-mono font-bold text-slate-700">
                          {u.prediction_count || 0}
                        </td>

                        {/* Registered */}
                        <td className="px-4 py-3.5 text-slate-500 font-mono text-[11px]">
                          {u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'}
                        </td>

                        {/* Actions */}
                        <td className="px-5 py-3.5 text-right">
                          <div className="flex items-center justify-end space-x-2">
                            {/* Toggle Disable/Enable */}
                            <button
                              onClick={() => handleToggleStatus(u)}
                              disabled={isSelf}
                              title={isSelf ? "Cannot disable your own administrator account" : (u.status === 'DISABLED' ? 'Enable Account' : 'Disable Account')}
                              className={`p-1.5 rounded-lg border transition-all cursor-pointer ${
                                isSelf
                                  ? 'opacity-30 cursor-not-allowed bg-slate-50 text-slate-400 border-slate-200'
                                  : u.status === 'DISABLED'
                                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100'
                                  : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-amber-50 hover:text-amber-700 hover:border-amber-200'
                              }`}
                            >
                              <Power className="w-3.5 h-3.5" />
                            </button>

                            {/* Delete User */}
                            <button
                              onClick={() => setDeleteModalUser(u)}
                              disabled={isSelf}
                              title={isSelf ? "Cannot delete your own administrator account" : "Permanently Delete User"}
                              className={`p-1.5 rounded-lg border transition-all cursor-pointer ${
                                isSelf
                                  ? 'opacity-30 cursor-not-allowed bg-slate-50 text-slate-400 border-slate-200'
                                  : 'bg-slate-50 text-slate-400 border-slate-200 hover:bg-rose-50 hover:text-rose-600 hover:border-rose-200'
                              }`}
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Safe Delete Confirmation Modal */}
      {deleteModalUser && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-white rounded-3xl p-6 sm:p-7 max-w-md w-full shadow-2xl border border-slate-200 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center border border-rose-100">
              <Trash2 className="w-6 h-6" />
            </div>

            <div className="space-y-1">
              <h3 className="text-lg font-bold text-slate-900">
                Confirm User Account Deletion
              </h3>
              <p className="text-xs text-slate-500 leading-relaxed">
                Are you sure you want to permanently delete user account <strong className="text-slate-800">{deleteModalUser.email}</strong>?
              </p>
            </div>

            <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800 space-y-1">
              <p className="font-bold flex items-center gap-1">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                Administrative Safety Notice:
              </p>
              <p className="text-[11px] leading-relaxed">
                This will revoke user credentials and permanently delete the account. Associated pre-clinical specimen prediction logs will be preserved in the audit archive.
              </p>
            </div>

            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={() => setDeleteModalUser(null)}
                disabled={deleting}
                className="px-4 py-2.5 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDelete}
                disabled={deleting}
                className="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold shadow-xs transition-all cursor-pointer flex items-center gap-1.5"
              >
                {deleting ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    <span>Deleting...</span>
                  </>
                ) : (
                  <>
                    <Trash2 className="w-3.5 h-3.5" />
                    <span>Confirm Delete</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

