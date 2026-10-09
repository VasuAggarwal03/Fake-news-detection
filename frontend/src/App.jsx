import React, { useState } from 'react';
import { 
  Activity, 
  BarChart3, 
  AlertTriangle, 
  FileSearch, 
  ShieldCheck,
  Send,
  Trash2,
  CheckCircle2,
  XCircle,
  Database,
  Cpu,
  BrainCircuit
} from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('Analyze');
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!title.trim() && !text.trim()) {
      setError('Please enter a headline or article text to analyze.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, text }),
      });

      if (!response.ok) {
        throw new Error('Failed to connect to the prediction API. Ensure the backend is running.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setTitle('');
    setText('');
    setResult(null);
    setError(null);
  };

  const tabs = [
    { name: 'Analyze', icon: FileSearch },
    { name: 'Model Analytics', icon: BarChart3 },
    { name: 'Error Analysis', icon: AlertTriangle },
    { name: 'How It Works', icon: Activity },
    { name: 'Responsible AI', icon: ShieldCheck },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30">
      
      {/* Top Navbar */}
      <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center shadow-[0_0_15px_rgba(79,70,229,0.5)]">
              <ShieldCheck size={18} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-slate-100 leading-tight">NewsGuard AI</h1>
              <p className="text-[10px] uppercase tracking-widest text-indigo-400 font-semibold">AI-Powered Detection</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            Backend Online
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8 relative">
        
        {/* Background Gradients */}
        <div className="absolute top-0 -left-40 w-96 h-96 bg-indigo-600/20 rounded-full blur-[100px] pointer-events-none"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-violet-600/10 rounded-full blur-[100px] pointer-events-none"></div>

        {/* Sidebar Navigation */}
        <nav className="lg:col-span-3 space-y-1 relative z-10">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.name;
            return (
              <button
                key={tab.name}
                onClick={() => setActiveTab(tab.name)}
                className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                  isActive 
                    ? 'bg-white/10 text-white shadow-[inset_0_1px_1px_rgba(255,255,255,0.1)] border border-white/5' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`}
              >
                <Icon size={18} className={isActive ? 'text-indigo-400' : 'text-slate-500'} />
                {tab.name}
              </button>
            )
          })}
        </nav>

        {/* Main Content Area */}
        <main className="lg:col-span-9 relative z-10 space-y-6">
          
          {/* ---- ANALYZE TAB ---- */}
          {activeTab === 'Analyze' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              
              {/* Hero */}
              <div className="p-8 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-white/5 shadow-xl relative overflow-hidden">
                <div className="absolute right-0 top-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-[80px]"></div>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 mb-4">
                  <Database size={12} /> Local ML Classification
                </span>
                <h2 className="text-3xl font-bold text-white mb-2">Detect misinformation before it spreads.</h2>
                <p className="text-slate-400 max-w-2xl text-sm leading-relaxed">
                  Enter an article headline and text below. Our locally hosted Support Vector Machine uses TF-IDF vectorization to identify deep linguistic patterns indicative of fake news, providing instant analytical classification.
                </p>
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                
                {/* Input Card */}
                <div className="bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-lg flex flex-col h-full">
                  <h3 className="text-sm font-semibold text-white flex items-center gap-2 mb-4">
                    <FileSearch size={16} className="text-indigo-400" /> Source Material
                  </h3>
                  
                  <div className="space-y-4 flex-grow flex flex-col">
                    <div>
                      <input
                        type="text"
                        placeholder="Article Headline..."
                        className="w-full bg-slate-950/50 border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                      />
                    </div>
                    <div className="flex-grow flex flex-col relative">
                      <textarea
                        placeholder="Paste full article text here..."
                        className="w-full h-48 md:h-full bg-slate-950/50 border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all resize-none"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                      />
                      <span className="absolute bottom-3 right-4 text-xs text-slate-600 font-mono">
                        {text.length} chars
                      </span>
                    </div>
                  </div>

                  <div className="flex gap-3 mt-4 pt-4 border-t border-white/5">
                    <button
                      onClick={handleClear}
                      disabled={loading || (!title && !text)}
                      className="px-4 py-2.5 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent hover:border-white/10 transition-all disabled:opacity-50 flex items-center gap-2"
                    >
                      <Trash2 size={16} /> Clear
                    </button>
                    <button
                      onClick={handleAnalyze}
                      disabled={loading || (!title.trim() && !text.trim())}
                      className="flex-1 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl text-sm py-2.5 px-4 shadow-[0_0_15px_rgba(79,70,229,0.3)] hover:shadow-[0_0_25px_rgba(79,70,229,0.5)] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {loading ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Processing...
                        </>
                      ) : (
                        <>
                          <Send size={16} /> Analyze Content
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* Results Card */}
                <div className="bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-lg flex flex-col h-full relative overflow-hidden">
                  <h3 className="text-sm font-semibold text-white flex items-center gap-2 mb-4">
                    <BrainCircuit size={16} className="text-indigo-400" /> Model Output
                  </h3>

                  {/* Empty State */}
                  {!result && !error && !loading && (
                    <div className="flex-grow flex flex-col items-center justify-center text-center px-6">
                      <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4 border border-white/5">
                        <Activity className="text-slate-500" size={24} />
                      </div>
                      <p className="text-sm text-slate-400">Awaiting input.</p>
                      <p className="text-xs text-slate-500 mt-1">Submit an article to generate an AI classification report.</p>
                    </div>
                  )}

                  {/* Loading State */}
                  {loading && (
                    <div className="flex-grow flex flex-col items-center justify-center">
                      <div className="relative">
                        <div className="w-16 h-16 rounded-full border-4 border-indigo-500/20"></div>
                        <div className="w-16 h-16 rounded-full border-4 border-indigo-500 border-t-transparent animate-spin absolute top-0 left-0"></div>
                      </div>
                      <p className="text-sm text-indigo-400 mt-4 animate-pulse font-medium">Extracting TF-IDF Features...</p>
                    </div>
                  )}

                  {/* Error State */}
                  {error && (
                    <div className="flex-grow flex flex-col justify-center bg-red-500/10 border border-red-500/20 rounded-xl p-6">
                      <AlertTriangle className="text-red-400 mb-3" size={24} />
                      <h4 className="text-sm font-semibold text-red-300 mb-1">Analysis Failed</h4>
                      <p className="text-xs text-red-400/80 leading-relaxed">{error}</p>
                    </div>
                  )}

                  {/* Success State */}
                  {result && !loading && (
                    <div className="flex flex-col h-full animate-in zoom-in-95 duration-300">
                      
                      <div className={`flex-grow flex items-center justify-center flex-col p-8 rounded-xl border relative overflow-hidden mb-6 ${
                        result.prediction === 'REAL' 
                          ? 'bg-emerald-500/10 border-emerald-500/30' 
                          : 'bg-rose-500/10 border-rose-500/30'
                      }`}>
                        {/* Glow effect behind prediction */}
                        <div className={`absolute w-32 h-32 rounded-full blur-[50px] ${result.prediction === 'REAL' ? 'bg-emerald-500/20' : 'bg-rose-500/20'}`}></div>
                        
                        <p className={`text-[10px] font-bold uppercase tracking-widest mb-2 z-10 ${
                          result.prediction === 'REAL' ? 'text-emerald-400' : 'text-rose-400'
                        }`}>
                          Prediction
                        </p>
                        <h3 className={`text-4xl md:text-5xl font-black z-10 tracking-tight flex items-center gap-3 ${
                          result.prediction === 'REAL' ? 'text-emerald-300' : 'text-rose-300'
                        }`}>
                          {result.prediction === 'REAL' ? <CheckCircle2 size={32} /> : <XCircle size={32} />}
                          {result.prediction === 'REAL' ? 'LIKELY REAL' : 'LIKELY FAKE'}
                        </h3>
                      </div>

                      <div className="grid grid-cols-2 gap-3 mb-6">
                        <div className="bg-black/20 border border-white/5 rounded-lg p-3">
                          <p className="text-xs text-slate-500 mb-1">Model</p>
                          <p className="text-sm font-semibold text-slate-200">{result.model}</p>
                        </div>
                        <div className="bg-black/20 border border-white/5 rounded-lg p-3">
                          <p className="text-xs text-slate-500 mb-1">Decision Score</p>
                          <p className="text-sm font-mono text-indigo-300">{result.decision_score.toFixed(4)}</p>
                        </div>
                      </div>

                      <div className="mt-auto border-t border-white/10 pt-4 flex items-start gap-3">
                        <ShieldCheck className="text-slate-500 shrink-0 mt-0.5" size={14} />
                        <p className="text-[11px] text-slate-500 leading-relaxed">
                          This result is an AI-based classification and does not independently verify factual truth. Please cross-reference claims with reliable sources.
                        </p>
                      </div>

                    </div>
                  )}
                </div>
              </div>
            </div>
          )}


          {/* ---- MODEL ANALYTICS TAB ---- */}
          {activeTab === 'Model Analytics' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl">
                <h2 className="text-xl font-bold text-white mb-2">Production Metrics</h2>
                <p className="text-sm text-slate-400 mb-6">Evaluated on 8,812 held-out test articles.</p>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  {[
                    { label: 'Accuracy', value: '99.77%' },
                    { label: 'Precision', value: '99.77%' },
                    { label: 'Recall', value: '99.78%' },
                    { label: 'F1 Score', value: '99.77%' },
                  ].map(stat => (
                    <div key={stat.label} className="bg-black/20 border border-indigo-500/20 rounded-xl p-5 text-center shadow-[inset_0_1px_0_rgba(255,255,255,0.05)]">
                      <p className="text-3xl font-black text-indigo-400 mb-1">{stat.value}</p>
                      <p className="text-xs font-medium uppercase tracking-wider text-slate-500">{stat.label}</p>
                    </div>
                  ))}
                </div>

                <h3 className="text-sm font-semibold text-white mb-4">Algorithm Comparison (Macro Averages)</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm text-left border-collapse">
                    <thead className="text-xs text-slate-400 uppercase bg-white/5 border-b border-white/10">
                      <tr>
                        <th className="px-6 py-4 font-medium">Model</th>
                        <th className="px-6 py-4 font-medium text-right">Accuracy</th>
                        <th className="px-6 py-4 font-medium text-right">Precision</th>
                        <th className="px-6 py-4 font-medium text-right">Recall</th>
                        <th className="px-6 py-4 font-medium text-right">F1 Score</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                      <tr className="hover:bg-white/[0.02] transition-colors">
                        <td className="px-6 py-4 text-slate-300">Logistic Regression</td>
                        <td className="px-6 py-4 text-slate-400 text-right font-mono">99.39%</td>
                        <td className="px-6 py-4 text-slate-400 text-right font-mono">99.38%</td>
                        <td className="px-6 py-4 text-slate-400 text-right font-mono">99.39%</td>
                        <td className="px-6 py-4 text-slate-400 text-right font-mono">99.39%</td>
                      </tr>
                      <tr className="bg-indigo-500/5 hover:bg-indigo-500/10 transition-colors">
                        <td className="px-6 py-4 text-indigo-300 font-medium flex items-center gap-2">
                          <CheckCircle2 size={14} className="text-indigo-400" /> Linear SVM (Deployed)
                        </td>
                        <td className="px-6 py-4 text-indigo-300 text-right font-mono font-bold">99.77%</td>
                        <td className="px-6 py-4 text-indigo-300 text-right font-mono font-bold">99.77%</td>
                        <td className="px-6 py-4 text-indigo-300 text-right font-mono font-bold">99.78%</td>
                        <td className="px-6 py-4 text-indigo-300 text-right font-mono font-bold">99.77%</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* ---- ERROR ANALYSIS TAB ---- */}
          {activeTab === 'Error Analysis' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl">
                <h2 className="text-xl font-bold text-white mb-6">Test Set Error Distribution</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="bg-black/20 border border-white/5 rounded-xl p-5">
                    <p className="text-sm text-slate-400 mb-2">False Positives</p>
                    <p className="text-3xl font-bold text-white mb-2">13</p>
                    <p className="text-xs text-slate-500">Real articles predicted as Fake.</p>
                  </div>
                  <div className="bg-black/20 border border-white/5 rounded-xl p-5">
                    <p className="text-sm text-slate-400 mb-2">False Negatives</p>
                    <p className="text-3xl font-bold text-white mb-2">7</p>
                    <p className="text-xs text-slate-500">Fake articles predicted as Real.</p>
                  </div>
                  <div className="bg-rose-500/10 border border-rose-500/20 rounded-xl p-5">
                    <p className="text-sm text-rose-400 mb-2">Total Errors</p>
                    <p className="text-3xl font-bold text-rose-300 mb-2">20</p>
                    <p className="text-xs text-rose-400/70">Out of 8,812 total test articles.</p>
                  </div>
                </div>

                <div className="bg-white/5 rounded-lg p-5 border border-white/5 text-sm text-slate-300 leading-relaxed">
                  <h3 className="font-semibold text-white mb-2">Error Insight</h3>
                  <p className="mb-2">
                    False Positives typically occur when a highly opinionated or dramatic real news article (e.g., specific political commentary) utilizes syntax heavily associated with unreliable sources.
                  </p>
                  <p>
                    False Negatives occur when fabricated articles adopt an extremely formal, objective tone and directly cite real-world entities, allowing them to bypass the TF-IDF vocabulary triggers.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* ---- HOW IT WORKS TAB ---- */}
          {activeTab === 'How It Works' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="p-8 bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl flex flex-col items-center">
                <h2 className="text-xl font-bold text-white mb-8">Classification Pipeline</h2>
                
                <div className="w-full max-w-md space-y-2">
                  {[
                    { title: 'Raw Input', desc: 'Headline + Article Text', icon: FileSearch },
                    { title: 'NLP Preprocessing', desc: 'Lowercase, Strip HTML, Normalization', icon: Cpu },
                    { title: 'TF-IDF Vectorization', desc: '50,000 Unigrams & Bigrams Matrix', icon: Database },
                    { title: 'Linear SVM Model', desc: 'Margin-maximizing hyperplane classification', icon: BrainCircuit },
                    { title: 'Final Output', desc: 'FAKE or REAL prediction', icon: Activity }
                  ].map((step, idx, arr) => (
                    <div key={idx} className="flex flex-col items-center">
                      <div className="w-full bg-black/40 border border-white/10 rounded-xl p-4 flex items-center gap-4 relative z-10 shadow-lg">
                        <div className="w-10 h-10 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center shrink-0">
                          <step.icon size={18} className="text-indigo-400" />
                        </div>
                        <div>
                          <h4 className="text-sm font-bold text-slate-200">{step.title}</h4>
                          <p className="text-xs text-slate-500">{step.desc}</p>
                        </div>
                      </div>
                      {idx < arr.length - 1 && (
                        <div className="h-6 w-[1px] bg-gradient-to-b from-indigo-500/50 to-transparent my-1"></div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ---- RESPONSIBLE AI TAB ---- */}
          {activeTab === 'Responsible AI' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="p-8 bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-2xl">
                <ShieldCheck size={40} className="text-indigo-400 mb-6" />
                <h2 className="text-2xl font-bold text-white mb-4">Responsible AI Usage</h2>
                <div className="space-y-4 text-sm text-slate-400 leading-relaxed max-w-3xl">
                  <p>
                    <strong className="text-slate-200">Statistical Learning:</strong> The NewsGuard AI model is fundamentally a statistical engine. It learns linguistic patterns, n-gram frequencies, and stylistic tells from the provided training dataset. 
                  </p>
                  <p>
                    <strong className="text-slate-200">Not an Oracle:</strong> It does <span className="text-rose-400 font-semibold">not</span> independently verify factual claims against external databases, search the internet, or understand semantic truth.
                  </p>
                  <p>
                    <strong className="text-slate-200">Inevitable Errors:</strong> As shown in our Error Analysis, predictions can contain false positives (real news flagged as fake) and false negatives (fake news evading detection).
                  </p>
                  <p>
                    <strong className="text-slate-200">Dataset Bias:</strong> The model's behavior is entirely bound by the biases inherent in the Kaggle Fake and Real News dataset. Changes in real-world news styles over time (data drift) will require periodic retraining.
                  </p>
                  <div className="mt-8 p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-lg text-indigo-300">
                    <strong>Final Verification:</strong> Important claims should always be verified through lateral reading and reliable, authoritative sources. AI is an assistant, not a replacement for critical thinking.
                  </div>
                </div>
              </div>
            </div>
          )}
          
        </main>
      </div>
    </div>
  );
}

export default App;
