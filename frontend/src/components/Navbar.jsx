import React from 'react';
import { 
  Activity, Microscope, BarChart3, History, Info, Cpu, 
  MessageSquare, ShieldAlert, LogIn, UserPlus, User, LogOut, LayoutDashboard 
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, systemStatus, currentUser, onLogout }) {
  const isAdmin = currentUser?.role === 'ADMIN';
  const isLoggedIn = !!currentUser;

  let navItems = [];

  if (!isLoggedIn) {
    navItems = [
      { id: 'home', label: 'Overview', icon: Microscope },
      { id: 'analysis', label: 'Slide Analysis', icon: Activity },
      { id: 'performance', label: 'Model Benchmarks', icon: BarChart3 },
      { id: 'chat', label: 'AI Assistant', icon: MessageSquare },
    ];
  } else if (isAdmin) {
    navItems = [
      { id: 'admin-dashboard', label: 'Admin Console', icon: ShieldAlert },
      { id: 'chat', label: 'AI Assistant', icon: MessageSquare },
      { id: 'analysis', label: 'Lymphoma Prediction', icon: Activity },
      { id: 'history', label: 'History Management', icon: History },
      { id: 'performance', label: 'Model Benchmarks', icon: BarChart3 },
    ];
  } else {
    navItems = [
      { id: 'user-dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { id: 'chat', label: 'AI Assistant', icon: MessageSquare },
      { id: 'analysis', label: 'Lymphoma Prediction', icon: Activity },
      { id: 'history', label: 'Prediction History', icon: History },
      { id: 'performance', label: 'Model Benchmarks', icon: BarChart3 },
    ];
  }

  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-50 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div
            className="flex items-center space-x-3 cursor-pointer select-none"
            onClick={() => setActiveTab(isLoggedIn ? (isAdmin ? 'admin-dashboard' : 'user-dashboard') : 'home')}
          >
            <div className="w-9 h-9 rounded-xl bg-sky-600 flex items-center justify-center text-white shadow-xs">
              <Microscope className="w-5 h-5" />
            </div>
            <div>
              <span className="font-extrabold text-slate-900 text-lg tracking-tight">
                Lymphoma<span className="text-sky-600">AI</span>
              </span>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">Attention-Augmented Deep Learning</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-semibold transition-all cursor-pointer ${
                    isActive
                      ? 'bg-sky-50 text-sky-700 font-bold border border-sky-200/80 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-sky-600' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Action / Auth Area */}
          <div className="flex items-center space-x-3">
            {isLoggedIn ? (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setActiveTab('profile')}
                  className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === 'profile'
                      ? 'bg-sky-50 border-sky-200 text-sky-700'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <User className="w-3.5 h-3.5 text-slate-500" />
                  <span className="max-w-[110px] truncate">{currentUser.full_name?.split(' ')[0]}</span>
                  <span className={`text-[10px] px-1.5 py-0.2 rounded font-bold uppercase ${
                    isAdmin ? 'bg-rose-100 text-rose-800' : 'bg-sky-100 text-sky-800'
                  }`}>
                    {currentUser.role}
                  </span>
                </button>

                <button
                  onClick={onLogout}
                  title="Sign Out"
                  className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-colors cursor-pointer"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setActiveTab('login')}
                  className="flex items-center space-x-1.5 px-3.5 py-2 text-xs font-bold text-slate-700 hover:text-slate-900 hover:bg-slate-50 rounded-xl transition-colors cursor-pointer"
                >
                  <LogIn className="w-3.5 h-3.5 text-slate-500" />
                  <span>Login</span>
                </button>

                <button
                  onClick={() => setActiveTab('register')}
                  className="flex items-center space-x-1.5 px-4 py-2 text-xs font-bold text-white bg-sky-600 hover:bg-sky-500 rounded-xl shadow-xs transition-all hover:scale-[1.02] cursor-pointer"
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  <span>Create Account</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Bar */}
      <div className="md:hidden flex overflow-x-auto px-2 py-1.5 border-t border-slate-100 space-x-1 bg-slate-50">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium whitespace-nowrap ${
                isActive ? 'bg-white text-sky-700 shadow-xs font-semibold' : 'text-slate-600'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
