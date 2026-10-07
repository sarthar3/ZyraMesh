import React from 'react';
import { useStore } from '../store/useStore';
import { RefreshCw, ArrowRight, UserCheck } from 'lucide-react';

export const ReOrchestrationPage: React.FC = () => {
  const { executionLogs } = useStore();
  const reRoutedLogs = executionLogs.filter((l) => l.status === 'RE_ROUTED');

  return (
    <div className="p-8 space-y-6 max-w-6xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <RefreshCw className="w-5 h-5 text-rose-600" />
          <span>Dynamic Re-Orchestration Engine</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Dynamic subtask re-routing triggered when step verification fails or an agent encounters execution risk threshold breaches.
        </p>
      </div>

      <div className="space-y-4">
        {reRoutedLogs.length === 0 ? (
          <div className="glass-panel p-8 text-center text-xs text-slate-500 space-y-2">
            <UserCheck className="w-8 h-8 text-lime-600 mx-auto" />
            <div className="font-bold text-slate-900 text-sm">No Re-Routing Triggers Required</div>
            <div className="font-medium text-slate-600">All agent executions in the current workflow passed verification and uncertainty checks on the first attempt.</div>
          </div>
        ) : (
          reRoutedLogs.map((log) => (
            <div key={log.execution_id} className="glass-panel-rose p-5 rounded-xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs text-rose-900 font-extrabold">DYNAMIC RE-ROUTING EVENT</span>
                <span className="text-[10px] text-slate-500 font-medium">Task ID: {log.task_id}</span>
              </div>
              <div className="flex items-center space-x-4 text-xs">
                <div className="p-3 rounded-lg bg-white border border-rose-200">
                  <div className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Original Agent</div>
                  <div className="font-bold text-slate-900">{log.agent_id}</div>
                </div>
                <ArrowRight className="w-5 h-5 text-rose-600" />
                <div className="p-3 rounded-lg bg-lime-100 border border-lime-300">
                  <div className="text-[10px] text-lime-900 font-bold uppercase tracking-wider">Replacement Calibrated Agent</div>
                  <div className="font-bold text-slate-900">Re-routed via ACTG trust composition</div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};


