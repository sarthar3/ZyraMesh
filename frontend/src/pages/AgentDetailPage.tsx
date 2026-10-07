import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../services/api';
import type { Agent } from '../types';
import { ShieldCheck, Cpu, DollarSign, Clock, ArrowLeft, Activity, UserCheck } from 'lucide-react';

export const AgentDetailPage: React.FC = () => {
  const { agentId } = useParams<{ agentId: string }>();
  const [agent, setAgent] = useState<Agent | null>(null);

  useEffect(() => {
    if (agentId) {
      api.getAgentDetails(agentId).then(setAgent).catch(console.error);
    }
  }, [agentId]);

  if (!agent) {
    return (
      <div className="p-8 text-center text-slate-500 font-sans text-xs">
        Loading agent profile details...
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6 max-w-5xl mx-auto font-sans">
      <Link to="/marketplace" className="inline-flex items-center space-x-2 text-xs text-lime-700 hover:text-lime-900 font-bold hover:underline">
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Agent Marketplace Registry</span>
      </Link>

      {/* Header Profile Card */}
      <div className="glass-panel p-6 rounded-xl border-lime-200 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-extrabold text-slate-900">{agent.name}</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 border border-lime-300 font-bold">
                {agent.status}
              </span>
            </div>
            <div className="text-xs text-lime-700 font-bold flex items-center space-x-1 mt-1">
              <Cpu className="w-3.5 h-3.5" />
              <span>Backend Provider: {agent.model_backend}</span>
            </div>
          </div>

          <div className="flex items-center space-x-6">
            <div className="text-right">
              <div className="text-2xl font-extrabold text-lime-700">{(agent.trust_mean * 100).toFixed(1)}%</div>
              <div className="text-[10px] text-slate-500 font-medium">Trust Mean (\(\mu\))</div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-extrabold text-rose-600">{agent.trust_uncertainty.toFixed(3)}</div>
              <div className="text-[10px] text-slate-500 font-medium">Uncertainty (\(\sigma^2\))</div>
            </div>
          </div>
        </div>

        <p className="text-slate-600 text-xs leading-relaxed font-medium">{agent.description}</p>
      </div>

      {/* Specs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="glass-panel p-5 rounded-xl border-lime-200 space-y-2">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center space-x-2">
            <Clock className="w-4 h-4 text-lime-600" />
            <span>Performance SLA</span>
          </div>
          <div className="text-xl font-extrabold text-slate-900">{agent.avg_latency_ms} ms</div>
          <div className="text-[11px] text-slate-500 font-medium">Average step turnaround</div>
        </div>

        <div className="glass-panel p-5 rounded-xl border-lime-200 space-y-2">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center space-x-2">
            <DollarSign className="w-4 h-4 text-lime-600" />
            <span>Token Cost</span>
          </div>
          <div className="text-xl font-extrabold text-slate-900">${agent.cost_per_1k_tokens} / 1k</div>
          <div className="text-[11px] text-slate-500 font-medium">Input/Output token pricing</div>
        </div>

        <div className="glass-panel-rose p-5 rounded-xl space-y-2">
          <div className="text-xs font-bold text-rose-800 uppercase tracking-wider flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-rose-600" />
            <span>Security Tier</span>
          </div>
          <div className="text-sm font-bold text-slate-900 truncate">{agent.permissions.join(', ')}</div>
          <div className="text-[11px] text-slate-500 font-medium">Granted sandbox permissions</div>
        </div>
      </div>

      {/* Capability-Specific Trust Breakdown */}
      <div className="glass-panel p-6 rounded-xl border-lime-200 space-y-4">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center space-x-2">
          <Activity className="w-4 h-4 text-lime-600" />
          <span>Capability-Specific Bayesian Trust Distributions</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(agent.capability_specific_trust || {}).map(([cap, trust]) => (
            <div key={cap} className="glass-panel p-4 rounded-lg border-slate-200 space-y-2">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-slate-800">{cap}</span>
                <span className="text-lime-700">{(trust.mean * 100).toFixed(1)}% (\(\sigma^2\)={trust.var.toFixed(3)})</span>
              </div>
              <div className="w-full h-2.5 rounded-full bg-slate-100 overflow-hidden border border-slate-200">
                <div className="h-full bg-lime-500" style={{ width: `${trust.mean * 100}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Collaboration History Matrix */}
      <div className="glass-panel p-6 rounded-xl border-lime-200 space-y-3">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center space-x-2">
          <UserCheck className="w-4 h-4 text-lime-600" />
          <span>Historical Agent Handoff Compatibility</span>
        </h3>

        {Object.keys(agent.collaboration_history || {}).length === 0 ? (
          <p className="text-xs text-slate-500 font-medium">No historical handoff observations recorded yet for this agent.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {Object.entries(agent.collaboration_history).map(([partnerId, hist]) => (
              <div key={partnerId} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs">
                <span className="font-semibold text-slate-800">Partner: {partnerId}</span>
                <div className="text-right">
                  <span className="text-lime-700 font-extrabold">{(hist.success_rate * 100).toFixed(0)}%</span>
                  <span className="text-[10px] text-slate-500 block">({hist.count} runs)</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};


