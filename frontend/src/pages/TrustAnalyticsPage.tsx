import React, { useEffect } from 'react';
import { useStore } from '../store/useStore';
import { BarChart3 } from 'lucide-react';

export const TrustAnalyticsPage: React.FC = () => {
  const { leaderboard, fetchTrustLeaderboard } = useStore();

  useEffect(() => {
    fetchTrustLeaderboard();
  }, []);

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <BarChart3 className="w-5 h-5 text-lime-600" />
          <span>Trust Analytics & Calibration Leaderboard</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Evidence-based Bayesian trust updating tracking capability-specific mean \(\mu\) and uncertainty \(\sigma^2\).
        </p>
      </div>

      <div className="glass-panel rounded-xl border-slate-200 overflow-hidden shadow-xs">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
              <th className="p-4">Rank & Agent Name</th>
              <th className="p-4">Calibrated Trust (\(\mu\))</th>
              <th className="p-4">Uncertainty (\(\sigma^2\))</th>
              <th className="p-4">Historical Success Rate</th>
              <th className="p-4">Total Executions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 text-xs font-medium">
            {leaderboard.map((item, idx) => (
              <tr key={item.agent_id} className="hover:bg-lime-50/50 transition-colors">
                <td className="p-4 font-bold text-slate-900 flex items-center space-x-3">
                  <span className="w-6 h-6 rounded-full bg-lime-100 text-lime-950 border border-lime-300 flex items-center justify-center text-[11px] font-extrabold">
                    #{idx + 1}
                  </span>
                  <div>
                    <div className="font-bold text-slate-900">{item.name}</div>
                    <div className="text-[10px] text-slate-400 font-medium">{item.agent_id}</div>
                  </div>
                </td>
                <td className="p-4 font-extrabold text-lime-700">
                  {(item.trust_mean * 100).toFixed(1)}%
                </td>
                <td className="p-4 font-extrabold text-rose-600">
                  {item.trust_uncertainty.toFixed(3)}
                </td>
                <td className="p-4 font-bold text-slate-800">
                  {(item.success_rate * 100).toFixed(1)}%
                </td>
                <td className="p-4 text-slate-600 font-semibold">
                  {item.total_executions} runs
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};


