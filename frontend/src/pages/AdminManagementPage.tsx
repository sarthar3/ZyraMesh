import React, { useState } from 'react';
import { useStore } from '../store/useStore';
import { Settings, Plus, CheckCircle2 } from 'lucide-react';

export const AdminManagementPage: React.FC = () => {
  const { fetchAgents } = useStore();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [modelBackend, setModelBackend] = useState('ollama/qwen2.5:1.5b-instruct');
  const [capabilities, setCapabilities] = useState('data_analysis, machine_learning');
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !description) return;
    setSubmitting(true);
    try {
      const capList = capabilities.split(',').map((c) => c.trim());
      await fetch('/api/v1/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          description,
          model_backend: modelBackend,
          capabilities: capList,
          tools: [{ name: 'custom_tool', type: 'utility' }],
          cost_per_1k_tokens: 0.001,
          avg_latency_ms: 150,
          availability_status: 'AVAILABLE',
          permissions: ['standard'],
          provenance: { developer: 'Admin Console' }
        })
      });
      await fetchAgents();
      setSuccessMsg(`Successfully registered agent '${name}' into marketplace!`);
      setName('');
      setDescription('');
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-8 space-y-6 max-w-4xl mx-auto font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 flex items-center space-x-2">
          <Settings className="w-5 h-5 text-lime-600" />
          <span>Admin & Marketplace Agent Registry</span>
        </h1>
        <p className="text-slate-500 text-xs mt-1">
          Register new specialized AI agents, manage capability tags, update availability, and configure provider adapters.
        </p>
      </div>

      {successMsg && (
        <div className="p-4 rounded-lg bg-lime-100 border border-lime-300 text-lime-950 text-xs flex items-center space-x-2 font-bold">
          <CheckCircle2 className="w-4 h-4 text-lime-600" />
          <span>{successMsg}</span>
        </div>
      )}

      <form onSubmit={handleRegister} className="glass-panel p-6 rounded-xl border-lime-200 space-y-4">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center space-x-2">
          <Plus className="w-4 h-4 text-lime-600" />
          <span>Register New Marketplace Agent</span>
        </h3>

        <div className="space-y-3 text-xs">
          <div>
            <label className="text-slate-600 font-semibold block mb-1">Agent Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Code Optimizer Agent"
              className="w-full p-3 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-lime-500 font-sans"
            />
          </div>

          <div>
            <label className="text-slate-600 font-semibold block mb-1">Description</label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Brief description of capability and scope..."
              className="w-full p-3 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-lime-500 font-sans leading-relaxed"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="text-slate-600 font-semibold block mb-1">Model Backend</label>
              <select
                value={modelBackend}
                onChange={(e) => setModelBackend(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 focus:outline-none focus:border-lime-500 font-sans"
              >
                <option value="ollama/qwen2.5:1.5b-instruct" className="bg-white">Ollama (qwen2.5:1.5b-instruct)</option>
                <option value="gemini/gemini-1.5-flash" className="bg-white">Gemini (gemini-1.5-flash)</option>
                <option value="mock/deterministic" className="bg-white">Mock Deterministic Adapter</option>
              </select>
            </div>

            <div>
              <label className="text-slate-600 font-semibold block mb-1">Capabilities (Comma-separated)</label>
              <input
                type="text"
                value={capabilities}
                onChange={(e) => setCapabilities(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-lime-500 font-sans"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="px-6 py-2.5 rounded-lg bg-lime-500 hover:bg-lime-400 text-slate-950 font-bold text-xs shadow-xs transition-all flex items-center space-x-2 disabled:opacity-50 cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>{submitting ? 'Registering Agent...' : 'Register Agent Profile'}</span>
        </button>
      </form>
    </div>
  );
};


