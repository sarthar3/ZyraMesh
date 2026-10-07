import React from 'react';
import { useStore } from '../store/useStore';
import { ShieldAlert, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const UncertaintyGatePage: React.FC = () => {
  const { executionLogs } = useStore();

  return (
    <div className="p-8 space-y-6 max-w-6xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-rose-600" />
          <span>Uncertainty-Gated Controller</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Monitors execution output entropy, schema validity, epistemic trust variance, and triggers selective oracle verification when risk exceeds threshold (0.40).
        </p>
      </div>

      <div className="space-y-4">
        {executionLogs.length === 0 ? (
          <div className="glass-panel p-8 text-center text-xs text-slate-500 font-medium">
            No active execution logs present. Run a workflow to view uncertainty gate evaluations.
          </div>
        ) : (
          executionLogs.map((log) => {
            const uncert = log.uncertainty_score || 0.15;
            const triggered = uncert >= 0.40;
            return (
              <div key={log.execution_id} className={`p-5 rounded-xl space-y-3 ${triggered ? 'glass-panel-rose' : 'glass-panel'}`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg border ${triggered ? 'bg-rose-100 text-rose-700 border-rose-200' : 'bg-lime-100 text-lime-800 border-lime-300'}`}>
                      {triggered ? <AlertTriangle className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900 text-sm">Subtask: {log.task_id}</h3>
                      <div className="text-[10px] text-slate-500 font-medium">Agent: {log.agent_name || log.agent_id}</div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-lg font-extrabold text-slate-900">{uncert.toFixed(3)}</div>
                    <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-bold ${triggered ? 'bg-rose-100 text-rose-900 border border-rose-300' : 'bg-lime-100 text-lime-900 border border-lime-300'}`}>
                      {triggered ? 'SELECTIVE ORACLE TRIGGERED' : 'LOW UNCERTAINTY (PASSED)'}
                    </span>
                  </div>
                </div>

                {/* Progress bar visualizer */}
                <div className="space-y-1">
                  <div className="flex justify-between text-[10px] text-slate-500 font-semibold">
                    <span>Gate Threshold: 0.400</span>
                    <span>Measured Entropy: {uncert.toFixed(3)}</span>
                  </div>
                  <div className="w-full h-2.5 rounded-full bg-slate-100 overflow-hidden border border-slate-200">
                    <div
                      className={`h-full ${triggered ? 'bg-rose-500' : 'bg-lime-500'}`}
                      style={{ width: `${Math.min(100, uncert * 100)}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};


