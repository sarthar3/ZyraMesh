import React, { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';
import { Store, Cpu, DollarSign, Clock, Wrench, Search } from 'lucide-react';
import { Link } from 'react-router-dom';

export const MarketplacePage: React.FC = () => {
  const { agents, fetchAgents } = useStore();
  const [search, setSearch] = useState('');
  const [selectedCap, setSelectedCap] = useState<string>('ALL');

  useEffect(() => {
    fetchAgents();
  }, []);

  const filteredAgents = agents.filter((a) => {
    const matchesSearch = a.name.toLowerCase().includes(search.toLowerCase()) || a.description.toLowerCase().includes(search.toLowerCase());
    const matchesCap = selectedCap === 'ALL' || a.capabilities.includes(selectedCap);
    return matchesSearch && matchesCap;
  });

  const allCapabilities = Array.from(new Set(agents.flatMap((a) => a.capabilities)));

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto font-sans">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
            <Store className="w-5 h-5 text-lime-600" />
            <span>Agent Marketplace Registry</span>
          </h1>
          <p className="text-slate-500 text-xs mt-1">
            Registered AI agents with capability distributions, tool specifications, SLAs, and Bayesian trust metrics.
          </p>
        </div>

        {/* Filter controls */}
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search agent or tool..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-4 py-1.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-lime-500 w-56 font-sans shadow-xs"
            />
          </div>

          <select
            value={selectedCap}
            onChange={(e) => setSelectedCap(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-800 focus:outline-none focus:border-lime-500 font-sans shadow-xs"
          >
            <option value="ALL">All Capabilities</option>
            {allCapabilities.map((cap) => (
              <option key={cap} value={cap} className="bg-white">{cap}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredAgents.map((agent) => (
          <div key={agent.agent_id} className="glass-panel p-5 rounded-xl border-slate-200 glass-panel-hover flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-bold text-slate-900 text-sm">{agent.name}</h3>
                  <div className="text-[11px] text-lime-700 font-semibold flex items-center space-x-1 mt-0.5">
                    <Cpu className="w-3 h-3 text-lime-600" />
                    <span>{agent.model_backend}</span>
                  </div>
                </div>
                <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                  {(agent.trust_mean * 100).toFixed(0)}% Trust
                </span>
              </div>

              <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">{agent.description}</p>

              {/* Specs pill row */}
              <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                <div className="flex items-center space-x-1.5 text-slate-600 font-semibold">
                  <Clock className="w-3.5 h-3.5 text-lime-600" />
                  <span>{agent.avg_latency_ms} ms SLA</span>
                </div>
                <div className="flex items-center space-x-1.5 text-slate-600 font-semibold">
                  <DollarSign className="w-3.5 h-3.5 text-lime-600" />
                  <span>${agent.cost_per_1k_tokens} / 1k</span>
                </div>
              </div>

              {/* Capabilities */}
              <div className="space-y-1">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Capabilities</span>
                <div className="flex flex-wrap gap-1">
                  {agent.capabilities.map((cap) => (
                    <span key={cap} className="text-[9px] px-2 py-0.5 rounded bg-lime-50 text-lime-800 border border-lime-200 font-semibold">
                      {cap}
                    </span>
                  ))}
                </div>
              </div>

              {/* Tools */}
              {agent.tools.length > 0 && (
                <div className="space-y-1">
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Tools</span>
                  <div className="flex flex-wrap gap-1">
                    {agent.tools.map((t) => (
                      <span key={t.name} className="text-[9px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 flex items-center space-x-1 font-medium">
                        <Wrench className="w-2.5 h-2.5 text-rose-500" />
                        <span>{t.name}</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <Link
              to={`/marketplace/${agent.agent_id}`}
              className="block w-full py-2 text-center text-xs font-bold rounded-lg bg-lime-100 hover:bg-lime-500 hover:text-slate-950 text-lime-950 border border-lime-300 transition-all shadow-xs"
            >
              View Full Profile & Trust Matrix →
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};


