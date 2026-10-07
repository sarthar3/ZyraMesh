import React, { useEffect } from 'react';
import { useStore } from '../store/useStore';
import { GitGraph, ArrowRight } from 'lucide-react';

export const ACTGPage: React.FC = () => {
  const { agents, fetchAgents } = useStore();

  useEffect(() => {
    fetchAgents();
  }, []);

  const capabilityNodes = Array.from(new Set(agents.flatMap((a) => a.capabilities)));

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <GitGraph className="w-5 h-5 text-lime-600" />
          <span>Agent Capability-Trust Graph (ACTG)</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Heterogeneous Network Topology connecting Agent nodes, Capability tags, and Pairwise Collaboration history edges.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Capability Nodes Column */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Capability Hub Nodes</h3>
          <div className="space-y-2">
            {capabilityNodes.map((cap) => (
              <div key={cap} className="glass-panel p-3 rounded-lg border-slate-200 flex items-center justify-between text-xs">
                <span className="font-bold text-slate-900">{cap}</span>
                <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                  {agents.filter((a) => a.capabilities.includes(cap)).length} Agents
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Agent Nodes & Calibrated Trust Column */}
        <div className="lg:col-span-2 space-y-3">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Marketplace Agent Graph Nodes</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((agent) => (
              <div key={agent.agent_id} className="glass-panel p-4 rounded-xl border-slate-200 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 text-xs">{agent.name}</span>
                  <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                    {(agent.trust_mean * 100).toFixed(0)}% Trust
                  </span>
                </div>

                <div className="text-[11px] text-slate-600 space-y-1 font-medium">
                  <div>Model: <span className="text-slate-900 font-bold">{agent.model_backend}</span></div>
                  <div>Variance: <span className="text-rose-600 font-bold">{agent.trust_uncertainty.toFixed(3)}</span></div>
                </div>

                {/* Graph Edges to Capabilities */}
                <div className="flex flex-wrap gap-1 pt-1">
                  {agent.capabilities.map((c) => (
                    <span key={c} className="text-[9px] px-1.5 py-0.5 rounded bg-lime-50 text-lime-800 border border-lime-200 flex items-center space-x-1 font-semibold">
                      <ArrowRight className="w-2.5 h-2.5 text-lime-600" />
                      <span>{c}</span>
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};


