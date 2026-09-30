import React, { useState } from 'react';
import { LogIn, Lock, Mail, AlertCircle, Shield, ArrowRight } from 'lucide-react';
import { loginUser } from '../services/api';

export default function Login({ onLoginSuccess, setActiveTab }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await loginUser({ email, password });
      onLoginSuccess(data.user, data.access_token);
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  const handleAdminQuickFill = () => {
    setEmail('admin@lymphoma.ai');
    setPassword('Admin@123');
  };

  return (
    <div className="max-w-md mx-auto py-8 animate-fadeIn">
      <div className="bg-white border border-slate-200 rounded-3xl p-8 shadow-xs space-y-6">
        <div className="text-center space-y-1">
          <div className="w-12 h-12 bg-sky-50 text-sky-600 rounded-2xl flex items-center justify-center mx-auto border border-sky-100">
            <LogIn className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight pt-2">Sign in to LymphomaAI</h2>
          <p className="text-xs text-slate-500">Enter your credentials to access the digital pathology studio.</p>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                required
                placeholder="pathologist@hospital.org"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-xs transition-all cursor-pointer"
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs space-y-2">
          <div className="font-bold text-slate-800 flex items-center gap-1.5">
            <Shield className="w-3.5 h-3.5 text-sky-600" />
            <span>Administrator Credentials</span>
          </div>
          <p className="text-[11px] text-slate-500 font-normal">
            To evaluate full administrative features (hide/unhide results, delete any record, configure threshold), click below:
          </p>
          <button
            type="button"
            onClick={handleAdminQuickFill}
            className="w-full py-1.5 px-3 bg-white hover:bg-slate-100 text-sky-700 font-bold text-[11px] rounded-lg border border-slate-200 transition-colors cursor-pointer text-center"
          >
            Fill Admin Credentials (admin@lymphoma.ai)
          </button>
        </div>

        <div className="pt-2 text-center text-xs text-slate-500 border-t border-slate-100">
          Don't have an account?{' '}
          <button
            onClick={() => setActiveTab('register')}
            className="text-sky-600 font-bold hover:underline cursor-pointer"
          >
            Create an Account
          </button>
        </div>
      </div>
    </div>
  );
}
