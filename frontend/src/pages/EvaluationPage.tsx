import React, { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';
import { api } from '../services/api';
import { TestTube2, Play } from 'lucide-react';

export const EvaluationPage: React.FC = () => {
  const { evaluationMetrics, fetchMetrics } = useStore();
  const [running, setRunning] = useState(false);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const handleRunBenchmark = async () => {
    setRunning(true);
    try {
      await api.runBenchmark(10);
      await fetchMetrics();
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto font-sans">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
            <TestTube2 className="w-5 h-5 text-lime-600" />
            <span>Research Evaluation & Benchmarking Suite</span>
          </h1>
          <p className="text-slate-500 text-xs mt-1">
            Empirical comparative analysis across 6 baseline execution strategies and ablation modes.
          </p>
        </div>

        <button
          onClick={handleRunBenchmark}
          disabled={running}
          className="px-5 py-2.5 rounded-lg bg-lime-500 hover:bg-lime-400 text-slate-950 font-bold text-xs shadow-xs transition-all flex items-center space-x-2 disabled:opacity-50 cursor-pointer"
        >
          <Play className="w-4 h-4 fill-current" />
          <span>{running ? 'Executing Benchmark Suite...' : 'Run Empirical Experiments'}</span>
        </button>
      </div>

      {/* Comparative Metrics Table */}
      <div className="glass-panel rounded-xl border-slate-200 overflow-hidden space-y-4 shadow-xs">
        <div className="p-5 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <h3 className="font-bold text-slate-900 text-sm">Empirical Baseline Comparison Matrix</h3>
          <span className="text-[10px] text-slate-500 font-bold">Sample Size N = 10 per strategy</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                <th className="p-4">Strategy</th>
                <th className="p-4 text-lime-800">Success Rate (%)</th>
                <th className="p-4 text-rose-700">Failure Propagation (%)</th>
                <th className="p-4 text-rose-700">ECE (Calibration Error)</th>
                <th className="p-4 text-lime-800">Avg Latency (ms)</th>
                <th className="p-4 text-slate-700">Total Cost ($)</th>
                <th className="p-4 text-slate-500">Re-Routing Success</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 text-xs font-semibold">
              {evaluationMetrics.slice(0, 6).map((m) => {
                const isZyra = m.strategy === 'ZYRAMESH';
                return (
                  <tr key={m.metric_id} className={isZyra ? 'bg-lime-50/80 border-l-4 border-l-lime-500' : 'hover:bg-slate-50'}>
                    <td className="p-4 font-extrabold text-slate-900 flex items-center space-x-2">
                      <span>{m.strategy}</span>
                      {isZyra && <span className="text-[9px] px-2 py-0.5 rounded-full bg-lime-500 text-slate-950 font-bold uppercase tracking-wider">PROPOSED</span>}
                    </td>
                    <td className="p-4 text-lime-800 font-extrabold">
                      {(m.workflow_success_rate * 100).toFixed(1)}%
                    </td>
                    <td className="p-4 text-rose-600">
                      {(m.failure_propagation_rate * 100).toFixed(1)}%
                    </td>
                    <td className="p-4 text-rose-600">
                      {m.expected_calibration_error.toFixed(3)}
                    </td>
                    <td className="p-4 text-lime-800">
                      {m.avg_latency_ms.toFixed(0)} ms
                    </td>
                    <td className="p-4 text-slate-800">
                      ${m.total_cost.toFixed(4)}
                    </td>
                    <td className="p-4 text-slate-600">
                      {(m.rerouting_success_rate * 100).toFixed(0)}%
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};


