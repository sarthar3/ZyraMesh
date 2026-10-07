import React, { useEffect } from 'react';
import { useStore } from '../store/useStore';
import { Network, GitGraph, ShieldAlert, BarChart3, ArrowRight, Activity, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export const HomePage: React.FC = () => {
  const { agents, fetchAgents, fetchTrustLeaderboard } = useStore();

  useEffect(() => {
    fetchAgents();
    fetchTrustLeaderboard();
  }, []);

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-sans">
      {/* Hero Header featuring the logo */}
      <div className="glass-panel p-8 rounded-2xl border border-lime-200 bg-gradient-to-r from-white via-lime-50/40 to-white relative overflow-hidden accent-line-lime shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-4 max-w-3xl">
            <div className="flex items-center space-x-3">
              <img src="/zyra-logo.png" alt="Zyra Mesh" className="w-12 h-12 object-contain rounded-xl border border-lime-200 shadow-xs bg-black p-0.5" />
              <div>
                <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900">
                  ZYRAMESH
                </h1>
                <p className="text-xs text-lime-800 font-bold uppercase tracking-wider">
                  Trust-Calibrated Dual-Graph Agent Team Formation
                </p>
              </div>
            </div>

            <p className="text-slate-600 text-xs sm:text-sm leading-relaxed">
              An open multi-agent marketplace and runtime framework featuring uncertainty-gated dynamic re-orchestration, Bayesian capability trust calibration, and empirical baseline benchmarks.
            </p>

            <div className="flex items-center space-x-4 pt-2">
              <Link
                to="/submit"
                className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-lg bg-lime-500 hover:bg-lime-400 text-slate-950 font-bold text-xs shadow-xs transition-all"
              >
                <span>Submit Objective</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/evaluation"
                className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-lg glass-panel text-slate-700 font-semibold text-xs hover:border-lime-400 hover:text-slate-950 transition-all"
              >
                <BarChart3 className="w-4 h-4 text-lime-600" />
                <span>View Evaluation Metrics</span>
              </Link>
            </div>
          </div>

          <div className="hidden lg:flex flex-col items-center justify-center p-6 bg-slate-900 rounded-2xl border border-slate-800 shadow-md">
            <img src="/zyra-logo.png" alt="Zyra Mesh Emblem" className="w-36 h-36 object-contain drop-shadow-lg" />
            <span className="text-[11px] text-lime-400 font-bold mt-2 tracking-wider uppercase">Dual-Graph Engine</span>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="glass-panel p-5 rounded-xl border-lime-200 flex items-center space-x-4">
          <div className="p-3 rounded-lg bg-lime-100 text-lime-800 border border-lime-300">
            <Network className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-extrabold text-slate-900">{agents.length}</div>
            <div className="text-xs text-slate-500 font-medium">Registered Agents</div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-xl border-lime-200 flex items-center space-x-4">
          <div className="p-3 rounded-lg bg-lime-100 text-lime-800 border border-lime-300">
            <GitGraph className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-extrabold text-slate-900">Dual-Graph</div>
            <div className="text-xs text-slate-500 font-medium">TDG + ACTG Topology</div>
          </div>
        </div>

        <div className="glass-panel-rose p-5 rounded-xl flex items-center space-x-4">
          <div className="p-3 rounded-lg bg-rose-100 text-rose-800 border border-rose-200">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-extrabold text-slate-900">0.40</div>
            <div className="text-xs text-slate-500 font-medium">Uncertainty Gate Threshold</div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-xl border-lime-200 flex items-center space-x-4">
          <div className="p-3 rounded-lg bg-lime-100 text-lime-800 border border-lime-300">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-extrabold text-slate-900">6 Baselines</div>
            <div className="text-xs text-slate-500 font-medium">Ablation Suite</div>
          </div>
        </div>
      </div>

      {/* Top Calibrated Agents Preview */}
      <div className="glass-panel p-6 rounded-xl border-lime-200 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-lime-600" />
            <span>Marketplace Calibrated Agent Registry</span>
          </h2>
          <Link to="/marketplace" className="text-xs text-lime-700 hover:text-lime-900 font-bold hover:underline">
            View Full Registry →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {agents.slice(0, 4).map((agent) => (
            <div key={agent.agent_id} className="glass-panel p-4 rounded-lg border-slate-200 hover:border-lime-400 transition-all space-y-2 glass-panel-hover">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900 truncate">{agent.name}</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                  {(agent.trust_mean * 100).toFixed(0)}% Trust
                </span>
              </div>
              <p className="text-[11px] text-slate-600 line-clamp-2">{agent.description}</p>
              <div className="flex flex-wrap gap-1 pt-1">
                {agent.capabilities.map((cap) => (
                  <span key={cap} className="text-[9px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-semibold">
                    {cap}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};


