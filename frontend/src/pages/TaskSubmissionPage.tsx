import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStore } from '../store/useStore';
import { Send, Sliders, Play, Cpu, CheckCircle } from 'lucide-react';

export const TaskSubmissionPage: React.FC = () => {
  const navigate = useNavigate();
  const { submitObjective, startExecution } = useStore();

  const [objective, setObjective] = useState(
    'Retrieve customer churn dataset, validate schema integrity, execute machine learning predictive analysis, conduct security audit, and produce executive markdown summary report.'
  );
  const [strategy, setStrategy] = useState('ZYRAMESH');
  const [ablations, setAblations] = useState({
    no_tdg: false,
    global_trust_only: false,
    no_uncertainty_penalty: false,
    no_collaboration_memory: false,
    no_guardrails: false,
    no_reorchestration: false,
  });

  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!objective.trim()) return;
    setSubmitting(true);
    try {
      const wf = await submitObjective(objective, strategy, ablations);
      await startExecution(wf.workflow_id);
      navigate('/execution');
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-8 space-y-6 max-w-4xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <Send className="w-5 h-5 text-lime-600" />
          <span>Submit Objective Prompt</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Decompose complex objectives into a Task Dependency Graph (TDG) and orchestrate calibrated agent teams on the ZyraMesh marketplace.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Objective Input */}
        <div className="glass-panel p-6 rounded-xl border-lime-200 space-y-3">
          <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
            Objective Specification
          </label>
          <textarea
            rows={4}
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            className="w-full p-4 rounded-lg bg-slate-50 border border-slate-200 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-lime-500 font-sans leading-relaxed"
            placeholder="Type your multi-step objective prompt here..."
          />
        </div>

        {/* Strategy Selector */}
        <div className="glass-panel p-6 rounded-xl border-lime-200 space-y-4">
          <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-lime-600" />
            <span>Orchestration Strategy & Baseline Selection</span>
          </label>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {[
              { id: 'ZYRAMESH', name: 'ZyraMesh (Proposed)', desc: 'Dual-Graph + Trust Calibration + Uncertainty Gate' },
              { id: 'DYNAMIC_BASELINE', name: 'Dynamic Baseline', desc: 'Greedy match without collaboration memory' },
              { id: 'REPUTATION_ONLY', name: 'Reputation Only', desc: 'Global trust mean routing' },
              { id: 'CAPABILITY_ONLY', name: 'Capability Only', desc: 'Tag matching ignoring trust variance' },
              { id: 'FIXED_MULTI_AGENT', name: 'Fixed Multi-Agent', desc: 'Static pipeline assignment' },
              { id: 'SINGLE_GENERALIST', name: 'Single Generalist', desc: 'Monolithic single LLM baseline' },
            ].map((st) => (
              <div
                key={st.id}
                onClick={() => setStrategy(st.id)}
                className={`p-4 rounded-xl cursor-pointer border transition-all space-y-1 ${
                  strategy === st.id
                    ? 'bg-lime-100/90 border-lime-400 text-lime-950 shadow-xs font-semibold'
                    : 'bg-slate-50 border-slate-200 hover:border-lime-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-900">{st.name}</span>
                  {strategy === st.id && <CheckCircle className="w-4 h-4 text-lime-600" />}
                </div>
                <p className="text-[11px] text-slate-500 font-normal">{st.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Ablation Toggles */}
        <div className="glass-panel-rose p-6 rounded-xl space-y-4">
          <label className="text-xs font-bold text-rose-800 uppercase tracking-wider flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-rose-600" />
            <span>Ablation Mode Controls (Experimental Switches)</span>
          </label>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {[
              { key: 'no_tdg', label: 'No TDG (Linearize graph into sequence)' },
              { key: 'global_trust_only', label: 'Global Trust Only (Ignore capability variance)' },
              { key: 'no_uncertainty_penalty', label: 'No Uncertainty Penalty (Ignore entropy gate)' },
              { key: 'no_collaboration_memory', label: 'No Collaboration Memory (Ignore handoff history)' },
              { key: 'no_guardrails', label: 'No Guardrails (Disable security verification)' },
              { key: 'no_reorchestration', label: 'No Re-Orchestration (Fail on step error)' },
            ].map((ab) => (
              <label
                key={ab.key}
                className="flex items-center space-x-3 p-3 rounded-lg bg-white border border-rose-200 cursor-pointer hover:bg-rose-50/50 transition-all text-xs text-slate-700 font-medium"
              >
                <input
                  type="checkbox"
                  checked={(ablations as any)[ab.key]}
                  onChange={(e) => setAblations({ ...ablations, [ab.key]: e.target.checked })}
                  className="rounded border-rose-300 text-rose-600 focus:ring-rose-500 w-4 h-4"
                />
                <span>{ab.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={submitting}
          className="w-full py-3.5 rounded-xl bg-lime-500 hover:bg-lime-400 text-slate-950 font-bold text-sm shadow-xs transition-all flex items-center justify-center space-x-2 disabled:opacity-50 cursor-pointer"
        >
          <Play className="w-4 h-4 fill-current" />
          <span>{submitting ? 'Decomposing Objective & Forming Team...' : 'Form Team & Execute ZyraMesh Workflow'}</span>
        </button>
      </form>
    </div>
  );
};


