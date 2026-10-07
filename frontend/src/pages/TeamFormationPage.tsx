import React from 'react';
import { useStore } from '../store/useStore';
import { Users, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export const TeamFormationPage: React.FC = () => {
  const { activeWorkflow } = useStore();

  if (!activeWorkflow) {
    return (
      <div className="p-12 text-center space-y-4 max-w-xl mx-auto font-sans">
        <Users className="w-12 h-12 text-lime-600 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">No Active Team Formation</h2>
        <p className="text-xs text-slate-500 font-medium">
          Submit an objective prompt to trigger the ZyraMesh constrained team composer.
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
          <Users className="w-5 h-5 text-lime-600" />
          <span>Constrained Agent Team Selection</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Optimization result matching subtasks against candidate marketplace agents respecting hard SLAs and soft multi-objective trust scores.
        </p>
      </div>

      {/* Meta Banner */}
      <div className="glass-panel p-5 rounded-xl border-lime-200 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Strategy Engine</span>
          <h2 className="text-lg font-extrabold text-lime-800">{activeWorkflow.execution_strategy}</h2>
        </div>

        <div className="flex items-center space-x-8">
          <div>
            <div className="text-xs text-slate-500 font-medium">Team Composition</div>
            <div className="text-lg font-extrabold text-slate-900">{activeWorkflow.tasks.length} Agents</div>
          </div>
          <div>
            <div className="text-xs text-slate-500 font-medium">Workflow State</div>
            <div className="text-lg font-extrabold text-lime-700">{activeWorkflow.status}</div>
          </div>
        </div>
      </div>

      {/* Assigned Team Members Table */}
      <div className="space-y-4">
        {activeWorkflow.tasks.map((t) => (
          <div key={t.task_id} className="glass-panel p-5 rounded-xl border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1 max-w-xl">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-lime-800">Subtask #{t.subtask_index}</span>
                <span className="text-xs text-slate-700 font-semibold">— {t.description}</span>
              </div>
              <div className="flex flex-wrap gap-1 pt-1">
                {t.required_capabilities.map((c) => (
                  <span key={c} className="text-[9px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200 font-semibold">
                    {c}
                  </span>
                ))}
              </div>
            </div>

            <div className="glass-panel p-3 rounded-lg border-lime-300 bg-lime-50/80 flex items-center space-x-3">
              <CheckCircle className="w-5 h-5 text-lime-600" />
              <div>
                <div className="text-xs font-bold text-slate-900">{t.assigned_agent_name || t.assigned_agent_id}</div>
                <div className="text-[10px] text-lime-800 font-semibold">ID: {t.assigned_agent_id}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};


