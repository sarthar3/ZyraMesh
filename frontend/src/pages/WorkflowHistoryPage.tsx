import React from 'react';
import { useStore } from '../store/useStore';
import { History, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const WorkflowHistoryPage: React.FC = () => {
  const { activeWorkflow } = useStore();

  return (
    <div className="p-8 space-y-6 max-w-6xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <History className="w-5 h-5 text-lime-600" />
          <span>Workflow Execution History & Audits</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Historical record of submitted natural language objectives, execution strategies, and auditable event traces.
        </p>
      </div>

      <div className="space-y-4">
        {!activeWorkflow ? (
          <div className="glass-panel p-8 text-center text-xs text-slate-500 font-medium">
            No active or historical workflows recorded yet in session.
          </div>
        ) : (
          <div className="glass-panel p-5 rounded-xl border-slate-200 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-extrabold text-xs text-lime-800">{activeWorkflow.workflow_id}</span>
              <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                {activeWorkflow.status}
              </span>
            </div>
            <p className="text-xs text-slate-900 font-semibold">"{activeWorkflow.raw_user_objective}"</p>
            <div className="flex items-center justify-between text-[11px] text-slate-500 border-t border-slate-200 pt-3 font-medium">
              <div>Strategy Engine: <span className="font-bold text-slate-900">{activeWorkflow.execution_strategy}</span></div>
              <div>Created: <span className="font-medium text-slate-700">{new Date(activeWorkflow.created_at).toLocaleString()}</span></div>
              <Link to="/execution" className="text-lime-700 hover:text-lime-900 font-bold hover:underline flex items-center space-x-1">
                <span>View Full Execution Trace</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};


