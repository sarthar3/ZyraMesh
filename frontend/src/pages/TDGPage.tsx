import React from 'react';
import { useStore } from '../store/useStore';
import { Network, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const TDGPage: React.FC = () => {
  const { activeWorkflow } = useStore();

  if (!activeWorkflow) {
    return (
      <div className="p-12 text-center space-y-4 max-w-xl mx-auto font-sans">
        <Network className="w-12 h-12 text-lime-600 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">No Active Task Dependency Graph</h2>
        <p className="text-xs text-slate-500 font-medium">
          Submit an objective prompt to parse subtasks and render the Task Dependency Graph (TDG).
        </p>
        <Link to="/submit" className="inline-block px-4 py-2 rounded-lg bg-lime-500 hover:bg-lime-400 text-slate-950 font-bold text-xs shadow-xs">
          Submit Objective →
        </Link>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6 max-w-6xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <Network className="w-5 h-5 text-lime-600" />
          <span>Task Dependency Graph (TDG)</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          DAG mapping of subtasks, dependency ordering, criticality scores, sensitivity levels, and propagation risk.
        </p>
      </div>

      {/* Objective Banner */}
      <div className="glass-panel p-4 rounded-xl border-lime-200 text-xs text-slate-700 font-medium">
        <span className="font-bold text-lime-800">Objective:</span> "{activeWorkflow.raw_user_objective}"
      </div>

      {/* Subtasks DAG Sequence */}
      <div className="space-y-4">
        {activeWorkflow.tasks.map((t, idx) => (
          <div key={t.task_id} className="relative">
            <div className="glass-panel p-5 rounded-xl border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="w-7 h-7 rounded-lg bg-lime-100 text-lime-900 border border-lime-300 flex items-center justify-center font-bold text-xs">
                    {t.subtask_index}
                  </span>
                  <h3 className="font-bold text-slate-900 text-sm">{t.description}</h3>
                </div>

                <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                  {t.assigned_agent_name || 'Unassigned'}
                </span>
              </div>

              {/* Badges & Scores */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs pt-1">
                <div className="space-y-1">
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Capabilities</span>
                  <div className="flex flex-wrap gap-1">
                    {t.required_capabilities.map((c) => (
                      <span key={c} className="text-[9px] px-2 py-0.5 rounded bg-lime-50 text-lime-800 border border-lime-200 font-semibold">
                        {c}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="glass-panel p-2.5 rounded-lg border-slate-200 flex justify-between items-center">
                  <span className="text-[10px] text-slate-500 font-semibold">Criticality</span>
                  <span className="font-extrabold text-lime-700">{(t.criticality_score * 100).toFixed(0)}%</span>
                </div>

                <div className="glass-panel p-2.5 rounded-lg border-slate-200 flex justify-between items-center">
                  <span className="text-[10px] text-slate-500 font-semibold">Sensitivity</span>
                  <span className="font-extrabold text-rose-600">{(t.sensitivity_score * 100).toFixed(0)}%</span>
                </div>

                <div className="glass-panel-rose p-2.5 rounded-lg flex justify-between items-center">
                  <span className="text-[10px] text-rose-800 font-semibold">Propagation Risk</span>
                  <span className="font-extrabold text-rose-600">{(t.propagation_risk * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>

            {/* Dependency Arrow */}
            {idx < activeWorkflow.tasks.length - 1 && (
              <div className="flex justify-center py-2">
                <ArrowRight className="w-4 h-4 text-lime-600 rotate-90" />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};


