import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import UserDashboard from './pages/UserDashboard';
import AdminDashboard from './pages/AdminDashboard';
import Analysis from './pages/Analysis';
import ModelPerformance from './pages/ModelPerformance';
import History from './pages/History';
import Chatbot from './pages/Chatbot';
import About from './pages/About';
import Profile from './pages/Profile';
import { getHealth, getModelInfo, getCurrentUser } from './services/api';

export default function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const stored = localStorage.getItem('lymphoma_user');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const [activeTab, setActiveTab] = useState(() => {
    const savedUser = localStorage.getItem('lymphoma_user');
    if (savedUser) {
      try {
        const u = JSON.parse(savedUser);
        return u.role === 'ADMIN' ? 'admin-dashboard' : 'user-dashboard';
      } catch {
        return 'home';
      }
    }
    return 'home';
  });

  const [systemStatus, setSystemStatus] = useState('connecting');
  const [modelInfo, setModelInfo] = useState(null);

  const checkStatus = async () => {
    try {
      const health = await getHealth();
      setSystemStatus(health.status);
      const info = await getModelInfo();
      setModelInfo(info);
    } catch (err) {
      setSystemStatus('offline');
    }
  };

  const syncCurrentUser = async () => {
    const token = localStorage.getItem('lymphoma_token');
    if (token) {
      try {
        const user = await getCurrentUser();
        setCurrentUser(user);
        localStorage.setItem('lymphoma_user', JSON.stringify(user));
      } catch {
        handleLogout();
      }
    }
  };

  useEffect(() => {
    checkStatus();
    syncCurrentUser();

    const interval = setInterval(checkStatus, 20000);
    const handleAuthExpired = () => handleLogout();
    window.addEventListener('auth-expired', handleAuthExpired);

    return () => {
      clearInterval(interval);
      window.removeEventListener('auth-expired', handleAuthExpired);
    };
  }, []);

  const handleLoginSuccess = (user, token) => {
    localStorage.setItem('lymphoma_token', token);
    localStorage.setItem('lymphoma_user', JSON.stringify(user));
    setCurrentUser(user);

    if (user.role === 'ADMIN') {
      setActiveTab('admin-dashboard');
    } else {
      setActiveTab('user-dashboard');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('lymphoma_token');
    localStorage.removeItem('lymphoma_user');
    setCurrentUser(null);
    setActiveTab('home');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col selection:bg-sky-500 selection:text-white">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        systemStatus={systemStatus}
        currentUser={currentUser}
        onLogout={handleLogout}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Visitor / Public Pages */}
        {activeTab === 'home' && <Home setActiveTab={setActiveTab} />}
        {activeTab === 'performance' && <ModelPerformance />}
        {activeTab === 'about' && <About />}

        {/* Auth Pages */}
        {activeTab === 'login' && (
          <Login onLoginSuccess={handleLoginSuccess} setActiveTab={setActiveTab} />
        )}
        {activeTab === 'register' && (
          <Register onRegisterSuccess={handleLoginSuccess} setActiveTab={setActiveTab} />
        )}

        {/* User Workspace */}
        {activeTab === 'user-dashboard' && (
          <UserDashboard user={currentUser} setActiveTab={setActiveTab} />
        )}

        {/* Admin Console */}
        {activeTab === 'admin-dashboard' && (
          currentUser?.role === 'ADMIN' ? (
            <AdminDashboard adminUser={currentUser} setActiveTab={setActiveTab} />
          ) : (
            <div className="p-8 bg-white border border-slate-200 rounded-3xl text-center space-y-3">
              <h2 className="text-lg font-bold text-rose-700">Access Restricted</h2>
              <p className="text-xs text-slate-500">Administrative privileges are required to access this portal.</p>
              <button
                onClick={() => setActiveTab('home')}
                className="px-4 py-2 bg-sky-600 text-white rounded-xl text-xs font-bold cursor-pointer"
              >
                Return to Overview
              </button>
            </div>
          )
        )}

        {/* Diagnostic Studio */}
        {activeTab === 'analysis' && (
          <Analysis onPredictionSuccess={checkStatus} user={currentUser} />
        )}

        {/* Pre-Clinical History */}
        {activeTab === 'history' && (
          <History user={currentUser} />
        )}

        {/* Gemini AI Chatbot */}
        {activeTab === 'chat' && (
          <Chatbot user={currentUser} />
        )}

        {/* Profile Details */}
        {activeTab === 'profile' && (
          currentUser ? (
            <Profile user={currentUser} onLogout={handleLogout} />
          ) : (
            <Login onLoginSuccess={handleLoginSuccess} setActiveTab={setActiveTab} />
          )
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-6 text-xs text-slate-500 text-center">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="font-mono">
            &copy; 2026 Attention-Augmented Residual Lymphoma Classification &bull; Major Project
          </p>
          <div className="flex items-center space-x-3 text-slate-500 font-medium">
            <span>FastAPI</span> &bull;
            <span>PyTorch</span> &bull;
            <span>Gemini AI</span> &bull;
            <span>React</span> &bull;
            <span>CBAM</span> &bull;
            <span>Grad-CAM++</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
