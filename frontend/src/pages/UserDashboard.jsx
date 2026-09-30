import React from 'react';
import { Activity, History, MessageSquare, BarChart3, ArrowRight, UserCheck, Microscope, Sparkles, BookOpen, ShieldCheck } from 'lucide-react';

export default function UserDashboard({ user, setActiveTab }) {
  const cards = [
    {
      id: 'analysis',
      title: 'Slide Diagnostic Studio',
      subtitle: 'Upload histopathological slides, execute validation gating, and view Grad-CAM++ attention heatmaps.',
      icon: Activity,
      color: 'bg-sky-50 text-sky-600 border-sky-100',
      action: 'Launch Diagnostic Studio',
    },
    {
      id: 'history',
      title: 'Clinical History Logs',
      subtitle: 'Review historical specimen screening records, 3-class probabilities, and pathologist review notes.',
      icon: History,
      color: 'bg-indigo-50 text-indigo-600 border-indigo-100',
      action: 'View Historical Records',
    },
    {
      id: 'chat',
      title: 'Medical & General AI Assistant',
      subtitle: 'Ask questions regarding medical science, pathology, oncology, biology, research, or general knowledge.',
      icon: MessageSquare,
      color: 'bg-emerald-50 text-emerald-600 border-emerald-100',
      action: 'Open AI Assistant',
    },
    {
      id: 'performance',
      title: 'Model Benchmarks',
      subtitle: 'Explore real empirical evaluation metrics, 15k test benchmarks, confusion matrix, and training convergence curves.',
      icon: BarChart3,
      color: 'bg-amber-50 text-amber-600 border-amber-100',
      action: 'View Model Benchmarks',
    },
  ];

  return (
    <div className="space-y-8 animate-fadeIn max-w-6xl mx-auto py-2">
      {/* Welcome Header */}
      <div className="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider bg-sky-50 text-sky-700 border border-sky-200 px-2.5 py-0.5 rounded-full">
              {user?.role || 'Standard User'}
            </span>
            <span className="text-xs text-slate-400 font-mono">ID #{user?.id}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            Welcome, {user?.full_name || 'Researcher'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 font-normal">
            Your personalized workspace for deep learning histopathological analysis and digital pathology assistance.
          </p>
        </div>

        <button
          onClick={() => setActiveTab('analysis')}
          className="flex items-center space-x-2 bg-sky-600 hover:bg-sky-500 text-white font-bold px-5 py-2.5 rounded-xl shadow-xs transition-all hover:scale-[1.02] text-xs sm:text-sm cursor-pointer shrink-0"
        >
          <Microscope className="w-4 h-4" />
          <span>New Slide Analysis</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Feature Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {cards.map((c) => {
          const Icon = c.icon;
          return (
            <div
              key={c.id}
              onClick={() => setActiveTab(c.id)}
              className="bg-white border border-slate-200 hover:border-sky-300 rounded-2xl p-6 shadow-xs hover:shadow-md transition-all cursor-pointer space-y-4 group flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className={`w-11 h-11 rounded-xl border flex items-center justify-center ${c.color} transition-transform group-hover:scale-110`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <ArrowRight className="w-4 h-4 text-slate-300 group-hover:text-sky-600 transition-colors" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900 group-hover:text-sky-700 transition-colors">
                    {c.title}
                  </h3>
                  <p className="text-xs text-slate-500 leading-relaxed mt-1 font-normal">
                    {c.subtitle}
                  </p>
                </div>
              </div>

              <div className="pt-2 text-xs font-bold text-sky-600 flex items-center space-x-1">
                <span>{c.action}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
