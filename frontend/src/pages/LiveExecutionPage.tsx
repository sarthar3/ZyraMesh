import React, { useEffect } from 'react';
import { useStore } from '../store/useStore';
import { PlayCircle, ShieldCheck, Clock, Terminal, Activity } from 'lucide-react';
import { Link } from 'react-router-dom';

export const LiveExecutionPage: React.FC = () => {
  const { activeWorkflow, executionLogs, isExecuting, loadWorkflowDetails } = useStore();

  useEffect(() => {
    if (activeWorkflow?.workflow_id) {
      loadWorkflowDetails(activeWorkflow.workflow_id);
    }
  }, []);

  if (!activeWorkflow) {
    return (
      <div className="p-12 text-center space-y-4 max-w-xl mx-auto font-sans">
        <PlayCircle className="w-12 h-12 text-lime-600 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">No Active Live Execution</h2>
        <p className="text-xs text-slate-500 font-medium">
          Submit an objective prompt to view live agent step executions.
        </p>
        <Link to="/submit" className="inline-block px-4 py-2 rounded-lg bg-lime-500 hover:bg-lime-400 text-slate-950 font-bold text-xs shadow-xs">
          Submit Objective →
        </Link>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6 max-w-6xl mx-auto font-sans">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
            <PlayCircle className="w-5 h-5 text-lime-600" />
            <span>Live Agent Workflow Execution</span>
          </h1>
          <p className="text-slate-500 text-xs mt-1">
            Realtime step-by-step execution timeline, tool calls, confidence scores, and verifier agreement.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <span className={`px-3.5 py-1 rounded-full text-xs font-bold border flex items-center space-x-1.5 ${
            isExecuting ? 'bg-rose-100 text-rose-900 border-rose-300 animate-pulse' : 'bg-lime-100 text-lime-950 border-lime-300'
          }`}>
            <Activity className="w-3.5 h-3.5" />
            <span>{isExecuting ? 'EXECUTING LIVE...' : activeWorkflow.status}</span>
          </span>
        </div>
      </div>

      {/* Execution Step Timeline */}
      <div className="space-y-4">
        {executionLogs.length === 0 ? (
          <div className="glass-panel p-8 text-center text-xs text-slate-500 space-y-2">
            <Clock className="w-6 h-6 text-lime-600 mx-auto animate-spin" />
            <div className="font-semibold">Initializing agent runtime and executing subtasks...</div>
          </div>
        ) : (
          executionLogs.map((log, idx) => (
            <div key={log.execution_id} className="glass-panel p-5 rounded-xl border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="w-7 h-7 rounded-lg bg-lime-100 text-lime-900 border border-lime-300 flex items-center justify-center font-bold text-xs">
                    {idx + 1}
                  </span>
                  <div>
                    <h3 className="font-bold text-slate-900 text-sm">Agent: {log.agent_name || log.agent_id}</h3>
                    <div className="text-[10px] text-slate-500 font-medium">Task ID: {log.task_id}</div>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                    Conf: {((log.confidence_score || 0.9) * 100).toFixed(0)}%
                  </span>
                  <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-900 border border-rose-300 font-bold">
                    Uncert: {(log.uncertainty_score || 0.1).toFixed(3)}
                  </span>
                </div>
              </div>

              {/* Output Sandbox View */}
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 font-mono text-xs text-lime-300 space-y-2">
                <div className="text-[10px] text-slate-400 flex items-center space-x-1 font-sans font-bold">
                  <Terminal className="w-3 h-3 text-lime-400" />
                  <span>Agent Output Payload</span>
                </div>
                <div className="whitespace-pre-wrap leading-relaxed text-slate-100 font-mono">
                  {typeof log.output_data?.result === 'string'
                    ? log.output_data.result
                    : JSON.stringify(log.output_data, null, 2)}
                </div>
              </div>

              {/* Tool Traces & Verification Status */}
              <div className="flex flex-wrap items-center justify-between gap-2 pt-1 text-xs">
                <div className="flex items-center space-x-2">
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Tools Invoked:</span>
                  {log.tool_trace.map((t) => (
                    <span key={t.tool} className="text-[9px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-semibold">
                      {t.tool} ({t.status})
                    </span>
                  ))}
                </div>

                {log.verifier_agreement && (
                  <div className="text-[11px] text-lime-800 font-bold flex items-center space-x-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-lime-600" />
                    <span>Dual-Oracle Agreement: {(log.verifier_agreement * 100).toFixed(0)}%</span>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};


