import React, { useState, useRef, useEffect } from 'react';
import { 
  MessageSquare, Send, Sparkles, Bot, User, RefreshCw, Zap, 
  Copy, Check, Globe, ExternalLink, Trash2, Code2, Cpu, 
  Compass, Calculator, Microscope, BookOpen, Shield
} from 'lucide-react';
import { sendMessageToChat } from '../services/api';

export default function Chatbot({ user }) {
  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      text: "Hello! I’m your Medical & General AI Assistant. Ask me about health, medicine, diseases, science, or general questions.",
      sources: [],
      search_performed: false
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState(null);
  const [activeCategory, setActiveCategory] = useState('all');
  const messagesEndRef = useRef(null);

  const categories = [
    { id: 'all', label: 'All Topics', icon: Compass },
    { id: 'health', label: 'Health & Medicine', icon: Shield },
    { id: 'pathology', label: 'Pathology & Oncology', icon: Microscope },
    { id: 'science', label: 'Biology & Science', icon: Sparkles },
    { id: 'research', label: 'Latest Research', icon: Globe },
    { id: 'general', label: 'General Knowledge', icon: BookOpen },
  ];

  const categoryPrompts = {
    all: [
      "What causes anemia?",
      "What are the common symptoms of diabetes?",
      "What is the difference between Hodgkin and Non-Hodgkin Lymphoma?",
      "What is photosynthesis?"
    ],
    health: [
      "What are the primary risk factors for cardiovascular disease?",
      "How do antibiotics eliminate bacterial pathogens?",
      "What are the clinical diagnostic criteria for hypertension?",
      "Explain the key differences between viral and bacterial infections."
    ],
    pathology: [
      "What are the histopathological hallmarks of CLL, FL, and MCL?",
      "What is the role of the BCL2 gene in Follicular Lymphoma?",
      "How does Mantle Cell Lymphoma present under microscopic evaluation?",
      "What is the purpose of an immunohistochemistry (IHC) panel in lymphoma diagnosis?"
    ],
    science: [
      "Explain cellular respiration and how ATP is generated.",
      "How does the human immune system generate antibodies?",
      "What is the structure of DNA and how does replication occur?",
      "Explain the fundamental difference between mitosis and meiosis."
    ],
    research: [
      "Search the web for recent clinical advances in CAR-T cell therapy.",
      "What are current targeted therapies for Mantle Cell Lymphoma?",
      "What are the latest findings in digital pathology AI validation?"
    ],
    general: [
      "What is the history behind the discovery of penicillin?",
      "Explain how vaccines stimulate long-term immunological memory.",
      "What is the difference between arteries and veins in human circulation?"
    ]
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMsg = { sender: 'user', text: query };
    setMessages(prev => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setLoading(true);

    try {
      // Build history payload for multi-turn context
      const historyPayload = messages.map(m => ({
        role: m.sender === 'user' ? 'user' : 'model',
        text: m.text
      }));

      const res = await sendMessageToChat(query, historyPayload);
      setMessages(prev => [
        ...prev,
        {
          sender: 'assistant',
          text: res.reply,
          sources: res.sources || [],
          search_performed: res.search_performed || false
        }
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          sender: 'assistant',
          text: "I encountered an error processing your request. Please check your connection or try again.",
          sources: [],
          search_performed: false
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        sender: 'assistant',
        text: "Conversation cleared. I am your **Medical & General AI Assistant**, ready to help with health, clinical medicine, pathology, oncology, biological sciences, or general questions.",
        sources: [],
        search_performed: false
      }
    ]);
  };

  const handleCopy = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto py-2 animate-fadeIn">
      {/* Top Header */}
      <div className="bg-white border border-slate-200 rounded-3xl p-6 sm:p-7 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-xs">
                <Bot className="w-5 h-5" />
              </div>
              <span>Medical & General AI Assistant</span>
            </h1>
            <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
              <Globe className="w-3 h-3 text-emerald-600" />
              Web Grounding Active
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 font-normal">
            Intelligent assistant for healthcare, oncology, histopathology, biological sciences, research, and general knowledge.
          </p>
        </div>

        <button
          onClick={handleClearChat}
          className="flex items-center space-x-1.5 px-3.5 py-2 text-xs font-semibold text-slate-600 hover:text-rose-600 bg-slate-50 hover:bg-rose-50 border border-slate-200 hover:border-rose-200 rounded-xl transition-all cursor-pointer"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>New Conversation</span>
        </button>
      </div>

      {/* Domain Category Selector */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
        {categories.map(cat => {
          const Icon = cat.icon;
          const isActive = activeCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                isActive
                  ? 'bg-sky-600 text-white shadow-xs'
                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{cat.label}</span>
            </button>
          );
        })}
      </div>

      {/* Suggested Quick Prompts */}
      <div className="flex flex-wrap gap-2">
        {categoryPrompts[activeCategory].map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q)}
            className="text-xs bg-white hover:bg-sky-50 text-slate-700 hover:text-sky-800 px-3.5 py-1.5 rounded-full border border-slate-200 transition-all cursor-pointer shadow-xs font-medium text-left"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Chat Messages Container */}
      <div className="bg-white border border-slate-200 rounded-3xl p-5 sm:p-7 shadow-xs min-h-[480px] max-h-[620px] overflow-y-auto space-y-5">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex items-start gap-3.5 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {m.sender === 'assistant' && (
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 text-white flex items-center justify-center shadow-xs shrink-0 mt-0.5">
                <Bot className="w-4 h-4" />
              </div>
            )}
            
            <div className={`space-y-2 max-w-2xl ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`p-4 sm:p-5 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-wrap ${
                m.sender === 'user'
                  ? 'bg-sky-600 text-white shadow-xs rounded-tr-none font-medium'
                  : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-none font-normal'
              }`}>
                {m.text}

                {/* Grounding Source Citations */}
                {m.sender === 'assistant' && m.sources && m.sources.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-slate-200 space-y-2">
                    <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                      <Globe className="w-3.5 h-3.5 text-sky-600" />
                      <span>Web Grounding Sources & References:</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {m.sources.map((s, sIdx) => (
                        <a
                          key={sIdx}
                          href={s.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center justify-between p-2 rounded-xl bg-white border border-slate-200 hover:border-sky-300 hover:bg-sky-50 text-[11px] text-slate-700 hover:text-sky-800 transition-all group"
                        >
                          <span className="truncate max-w-[200px] font-medium">{s.title || s.url}</span>
                          <ExternalLink className="w-3 h-3 text-slate-400 group-hover:text-sky-600 shrink-0 ml-1.5" />
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {m.sender === 'assistant' && (
                <div className="flex items-center justify-between px-1">
                  {m.search_performed && (
                    <span className="text-[10px] text-emerald-600 font-semibold flex items-center gap-1">
                      <Globe className="w-3 h-3" /> Grounded with Web Search
                    </span>
                  )}
                  <button
                    onClick={() => handleCopy(m.text, idx)}
                    className="text-[10px] text-slate-400 hover:text-slate-600 flex items-center gap-1 cursor-pointer px-1.5 py-0.5 rounded hover:bg-slate-100 ml-auto"
                  >
                    {copiedIdx === idx ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedIdx === idx ? "Copied" : "Copy"}</span>
                  </button>
                </div>
              )}
            </div>

            {m.sender === 'user' && (
              <div className="w-8 h-8 rounded-xl bg-slate-200 text-slate-700 flex items-center justify-center shadow-xs shrink-0 mt-0.5 font-bold text-xs">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2.5 text-xs text-slate-500 italic p-3.5 bg-slate-50 rounded-2xl border border-slate-200 w-fit">
            <RefreshCw className="w-4 h-4 animate-spin text-sky-600" />
            <span>AI assistant is synthesizing medical & scientific response...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="space-y-2">
        <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-2xl p-1.5 shadow-xs focus-within:border-sky-500 focus-within:ring-2 focus-within:ring-sky-100 transition-all">
          <input
            type="text"
            placeholder="Ask a medical or general question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 px-3.5 py-2.5 text-xs sm:text-sm text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className={`px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-1.5 text-white transition-all cursor-pointer shadow-xs ${
              !input.trim() || loading ? 'bg-slate-300 cursor-not-allowed' : 'bg-sky-600 hover:bg-sky-500'
            }`}
          >
            <Send className="w-4 h-4" />
            <span>Send</span>
          </button>
        </div>

        <div className="flex items-center justify-between px-2 text-[11px] text-slate-400">
          <span className="flex items-center gap-1">
            <Shield className="w-3 h-3 text-slate-400" />
            Medical & General AI Assistant provides educational and research assistance. Biopsy slide classification is performed by the Attention ResNet-50 CBAM model.
          </span>
          <span className="hidden sm:inline font-mono text-[10px]">Powered by Google Gemini API</span>
        </div>
      </form>
    </div>
  );
}

