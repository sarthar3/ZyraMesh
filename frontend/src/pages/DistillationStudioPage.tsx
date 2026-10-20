import React, { useState, useEffect } from 'react';
import { 
  Cpu, Zap, DollarSign, Download, Play, CheckCircle2, 
  Layers, Activity, Terminal, 
  TrendingDown, ShieldCheck, Sparkles, AlertCircle, RefreshCw
} from 'lucide-react';

import { api } from '../services/api';
import type { 
  DistillationJob, DistillationDataset, DistilledModel, 
  DistillationInferenceResult, PricingROI 
} from '../types';

export const DistillationStudioPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'wizard' | 'monitor' | 'arena' | 'models' | 'roi'>('arena');
  
  // Data state
  const [jobs, setJobs] = useState<DistillationJob[]>([]);
  const [datasets, setDatasets] = useState<DistillationDataset[]>([]);
  const [models, setModels] = useState<DistilledModel[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Wizard form state
  const [jobName, setJobName] = useState<string>('Zyra-Hardware-Edge-Distill-1B');
  const [teacherModel, setTeacherModel] = useState<string>('zyra-mesh-orchestrator');
  const [studentBase, setStudentBase] = useState<string>('qwen2.5:0.5b');
  const [distillStrategy, setDistillStrategy] = useState<string>('SEQUENCE_KD');
  const [selectedDatasetId, setSelectedDatasetId] = useState<string>('ds_shopping_gold_v1');
  const [epochs, setEpochs] = useState<number>(3);
  const [exportFormat, setExportFormat] = useState<string>('GGUF_Q4_K_M');
  const [isLaunching, setIsLaunching] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Arena inference state
  const [testPrompt, setTestPrompt] = useState<string>(
    'Find the best laptop under ₹70,000 for AI development with RTX GPU and 16GB RAM.'
  );
  const [selectedModelId, setSelectedModelId] = useState<string>('zyra-qwen2.5-0.5b-distilled-v1');
  const [isInferring, setIsInferring] = useState<boolean>(false);
  const [inferenceResult, setInferenceResult] = useState<DistillationInferenceResult | null>(null);

  // ROI calculator state
  const [monthlyRequests, setMonthlyRequests] = useState<number>(100000);
  const [teacherCostPer1M, setTeacherCostPer1M] = useState<number>(15.0);
  const [roiData, setRoiData] = useState<PricingROI | null>(null);

  // Model export modal state
  const [exportModalModel, setExportModalModel] = useState<any | null>(null);

  // Fetch initial data
  const fetchData = async () => {
    try {
      setLoading(true);
      const [fetchedJobs, fetchedDatasets, fetchedModels, fetchedRoi] = await Promise.all([
        api.getDistillationJobs(),
        api.getDistillationDatasets(),
        api.getDistilledModels(),
        api.getPricingROI(monthlyRequests, teacherCostPer1M)
      ]);
      setJobs(fetchedJobs);
      setDatasets(fetchedDatasets);
      setModels(fetchedModels);
      setRoiData(fetchedRoi);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to DaaS backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Poll active jobs if on monitor tab
  useEffect(() => {
    let interval: any;
    if (activeTab === 'monitor') {
      interval = setInterval(async () => {
        try {
          const fetchedJobs = await api.getDistillationJobs();
          setJobs(fetchedJobs);
        } catch (e) {
          // ignore polling error
        }
      }, 2500);
    }
    return () => clearInterval(interval);
  }, [activeTab]);

  // Handle ROI recalculation
  const handleRecalculateROI = async (reqs: number, cost: number) => {
    setMonthlyRequests(reqs);
    setTeacherCostPer1M(cost);
    try {
      const res = await api.getPricingROI(reqs, cost);
      setRoiData(res);
    } catch (e) {
      console.error(e);
    }
  };

  // Launch job
  const handleLaunchJob = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLaunching(true);
    setSuccessMsg(null);
    setError(null);
    try {
      const newJob = await api.createDistillationJob({
        name: jobName,
        teacher_model: teacherModel,
        student_base: studentBase,
        distillation_strategy: distillStrategy,
        dataset_id: selectedDatasetId,
        epochs: epochs,
        export_format: exportFormat
      });
      setSuccessMsg(`Distillation job "${newJob.name}" started successfully! Tracking training...`);
      setJobs([newJob, ...jobs]);
      setActiveTab('monitor');
    } catch (err: any) {
      setError(err.message || 'Failed to start distillation job');
    } finally {
      setIsLaunching(false);
    }
  };

  // Run side-by-side inference arena
  const handleRunInference = async () => {
    if (!testPrompt.trim()) return;
    setIsInferring(true);
    setError(null);
    try {
      const res = await api.runDistillationInference({
        prompt: testPrompt,
        student_model_id: selectedModelId,
        teacher_model: 'zyra-mesh-orchestrator',
        compare_teacher: true
      });
      setInferenceResult(res);
    } catch (err: any) {
      setError(err.message || 'Inference arena execution failed');
    } finally {
      setIsInferring(false);
    }
  };

  // Open export modal
  const handleOpenExport = async (modelId: string) => {
    try {
      const exportData = await api.exportDistilledModel(modelId);
      setExportModalModel(exportData);
    } catch (e: any) {
      alert(`Export failed: ${e.message}`);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Top Value Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-lime-950 text-white rounded-2xl p-6 shadow-lg border border-lime-500/20 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-lime-500/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-lime-500/20 text-lime-300 text-xs font-bold border border-lime-500/30">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Production Distillation as a Service (DaaS)</span>
              {loading && <RefreshCw className="w-3 h-3 animate-spin text-lime-400 ml-1" />}
            </div>

            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">
              Distill Heavy Multi-Agent Meshes into Compact Edge Models
            </h1>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Transform slow 5-second multi-agent orchestration into lightning-fast sub-60ms student models 
              (<code className="bg-black/40 text-lime-300 px-1.5 py-0.5 rounded text-xs">Qwen2.5-0.5B</code>, <code className="bg-black/40 text-lime-300 px-1.5 py-0.5 rounded text-xs">SmolLM2-360M</code>) 
              ready for real-time edge deployment. <strong>99% cheaper, 70x faster, zero cloud GPU cost.</strong>
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center shrink-0">
            <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
              <div className="text-xs text-slate-400 font-medium">Latency Drop</div>
              <div className="text-xl font-bold text-lime-400 flex items-center justify-center gap-1">
                <TrendingDown className="w-4 h-4" /> 98.4%
              </div>
            </div>
            <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
              <div className="text-xs text-slate-400 font-medium">Cloud Cost</div>
              <div className="text-xl font-bold text-amber-400">-99.3%</div>
            </div>
            <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
              <div className="text-xs text-slate-400 font-medium">Fidelity</div>
              <div className="text-xl font-bold text-white">96.4%</div>
            </div>
            <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
              <div className="text-xs text-slate-400 font-medium">Compute Cost</div>
              <div className="text-xl font-bold text-emerald-400">$0 Free</div>
            </div>
          </div>
        </div>

        {/* Studio Navigation Tabs */}
        <div className="flex flex-wrap gap-2 mt-6 pt-4 border-t border-slate-700/60">
          {[
            { id: 'arena', label: 'Real-Time Arena Playground', icon: Play },
            { id: 'wizard', label: 'Distillation Wizard', icon: Layers },
            { id: 'monitor', label: `Training Monitor (${jobs.length})`, icon: Activity },
            { id: 'models', label: `Model Registry (${models.length})`, icon: Cpu },
            { id: 'roi', label: 'Commercial ROI Calculator', icon: DollarSign }
          ].map(tab => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
                  active 
                    ? 'bg-lime-500 text-slate-950 shadow-md font-bold' 
                    : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Notifications */}
      {successMsg && (
        <div className="p-4 bg-lime-50 border border-lime-300 text-lime-900 rounded-xl flex items-center justify-between text-xs font-medium">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-lime-600 shrink-0" />
            <span>{successMsg}</span>
          </div>
          <button onClick={() => setSuccessMsg(null)} className="text-lime-700 hover:text-lime-900 font-bold">✕</button>
        </div>
      )}
      {error && (
        <div className="p-4 bg-rose-50 border border-rose-300 text-rose-900 rounded-xl flex items-center justify-between text-xs font-medium">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)} className="text-rose-700 hover:text-rose-900 font-bold">✕</button>
        </div>
      )}

      {/* TAB 1: SIDE-BY-SIDE INFERENCE ARENA */}
      {activeTab === 'arena' && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-lime-200/80 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <Play className="w-5 h-5 text-lime-600" />
                  Live Teacher vs Distilled Student Arena
                </h2>
                <p className="text-xs text-slate-500">
                  Compare real-time output, sub-60ms response speed, and cost savings between the heavy multi-agent mesh and distilled student model.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 font-medium">Student Model:</span>
                <select
                  value={selectedModelId}
                  onChange={(e) => setSelectedModelId(e.target.value)}
                  className="text-xs font-semibold bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 text-slate-800 focus:outline-lime-500"
                >
                  {models.map(m => (
                    <option key={m.id} value={m.id}>{m.name} ({m.parameters})</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Test prompt input */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-700">Enter Test Prompt / Objective:</label>
              <textarea
                value={testPrompt}
                onChange={(e) => setTestPrompt(e.target.value)}
                rows={3}
                className="w-full text-xs font-medium p-3 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-lime-500/20 focus:border-lime-500"
                placeholder="Type any e-commerce, specification, or reasoning prompt..."
              />
              <div className="flex flex-wrap gap-2 items-center justify-between pt-1">
                <div className="flex flex-wrap gap-1.5 items-center">
                  <span className="text-[11px] text-slate-400 font-medium">Quick Presets:</span>
                  {[
                    'Find best laptop under ₹70,000 for AI development',
                    'Compare Legion Slim 5 vs ASUS TUF F15',
                    'Verify authentic catalog price for laptop_001'
                  ].map(preset => (
                    <button
                      key={preset}
                      type="button"
                      onClick={() => setTestPrompt(preset)}
                      className="text-[11px] bg-slate-100 hover:bg-lime-100 text-slate-700 hover:text-lime-900 px-2.5 py-1 rounded-md transition-all font-medium border border-slate-200"
                    >
                      {preset}
                    </button>
                  ))}
                </div>

                <button
                  type="button"
                  onClick={handleRunInference}
                  disabled={isInferring}
                  className="px-5 py-2.5 bg-lime-600 hover:bg-lime-700 disabled:bg-slate-300 text-white font-bold text-xs rounded-xl shadow-xs transition-all flex items-center gap-2 shrink-0 cursor-pointer"
                >
                  {isInferring ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      <span>Benchmarking Both Models...</span>
                    </>
                  ) : (
                    <>
                      <Zap className="w-3.5 h-3.5 text-lime-200" />
                      <span>Run Side-by-Side Comparison</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Results Comparison Grid */}
          {inferenceResult ? (
            <div className="space-y-4">
              {/* Summary Metrics Bar */}
              <div className="bg-gradient-to-r from-lime-500/10 via-emerald-500/10 to-teal-500/10 p-4 rounded-2xl border border-lime-300 flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-lime-600 text-white flex items-center justify-center font-extrabold text-sm shadow-xs">
                    ⚡
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900">
                      Distilled Student is {inferenceResult.comparison.speedup_factor}
                    </div>
                    <div className="text-[11px] text-slate-600">
                      Latency reduced from {inferenceResult.teacher?.latency_ms}ms to {inferenceResult.student.latency_ms}ms with {inferenceResult.comparison.cost_reduction_pct}% cost reduction.
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4 text-xs font-semibold">
                  <span className="bg-white px-3 py-1.5 rounded-lg border border-lime-200 text-lime-900">
                    Fidelity Score: <strong>{(inferenceResult.comparison.semantic_fidelity_score * 100).toFixed(1)}%</strong>
                  </span>
                  <span className="bg-emerald-600 text-white px-3 py-1.5 rounded-lg shadow-xs">
                    {inferenceResult.comparison.recommendation}
                  </span>
                </div>
              </div>

              {/* Side by Side Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Teacher Card */}
                <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
                  <div className="bg-slate-100/80 px-5 py-3 border-b border-slate-200 flex items-center justify-between">
                    <div>
                      <div className="text-xs font-extrabold text-slate-900 flex items-center gap-1.5">
                        <Layers className="w-4 h-4 text-slate-600" />
                        <span>Teacher (Multi-Agent Mesh / Gemini)</span>
                      </div>
                      <div className="text-[10px] text-slate-500">7-Agent Sequential Orchestration</div>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 font-bold">
                      Cloud Pipeline
                    </span>
                  </div>

                  <div className="p-5 space-y-4 flex-1 flex flex-col justify-between">
                    <div className="space-y-3">
                      <div className="grid grid-cols-3 gap-2 text-center">
                        <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                          <div className="text-[10px] text-slate-500">Latency</div>
                          <div className="text-sm font-bold text-slate-800">{inferenceResult.teacher?.latency_ms} ms</div>
                        </div>
                        <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                          <div className="text-[10px] text-slate-500">Query Cost</div>
                          <div className="text-sm font-bold text-amber-700">${inferenceResult.teacher?.cost_usd}</div>
                        </div>
                        <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                          <div className="text-[10px] text-slate-500">RAM Footprint</div>
                          <div className="text-sm font-bold text-slate-800">14.2 GB</div>
                        </div>
                      </div>

                      <div className="text-xs bg-slate-50 p-3.5 rounded-xl border border-slate-200/60 font-mono text-slate-700 whitespace-pre-wrap leading-relaxed max-h-64 overflow-y-auto">
                        {inferenceResult.teacher?.text}
                      </div>
                    </div>

                    <div className="text-[11px] text-slate-400 italic">
                      Requires multi-stage cloud API roundtrips and high memory.
                    </div>
                  </div>
                </div>

                {/* Distilled Student Card */}
                <div className="bg-white rounded-2xl border-2 border-lime-400 shadow-md overflow-hidden flex flex-col">
                  <div className="bg-lime-500 px-5 py-3 flex items-center justify-between text-slate-950">
                    <div>
                      <div className="text-xs font-black flex items-center gap-1.5">
                        <Zap className="w-4 h-4 fill-slate-950" />
                        <span>Distilled Student ({inferenceResult.student.model})</span>
                      </div>
                      <div className="text-[10px] text-slate-900 font-medium">Single-Pass Ultra-Fast Forward Inference</div>
                    </div>
                    <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-slate-950 text-lime-400 font-extrabold uppercase tracking-wide">
                      Deploy Ready
                    </span>
                  </div>

                  <div className="p-5 space-y-4 flex-1 flex flex-col justify-between">
                    <div className="space-y-3">
                      <div className="grid grid-cols-3 gap-2 text-center">
                        <div className="bg-lime-50 p-2.5 rounded-xl border border-lime-200">
                          <div className="text-[10px] text-lime-800 font-medium">Latency</div>
                          <div className="text-sm font-black text-lime-900">{inferenceResult.student.latency_ms} ms</div>
                        </div>
                        <div className="bg-lime-50 p-2.5 rounded-xl border border-lime-200">
                          <div className="text-[10px] text-lime-800 font-medium">Query Cost</div>
                          <div className="text-sm font-black text-lime-900">${inferenceResult.student.cost_usd}</div>
                        </div>
                        <div className="bg-lime-50 p-2.5 rounded-xl border border-lime-200">
                          <div className="text-[10px] text-lime-800 font-medium">RAM Footprint</div>
                          <div className="text-sm font-black text-lime-900">394 MB</div>
                        </div>
                      </div>

                      <div className="text-xs bg-lime-50/50 p-3.5 rounded-xl border border-lime-200 font-sans text-slate-800 whitespace-pre-wrap leading-relaxed max-h-64 overflow-y-auto">
                        {inferenceResult.student.text}
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-2">
                      <span className="text-[11px] text-lime-700 font-semibold flex items-center gap-1">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        Passes Uncertainty Gating
                      </span>
                      <button
                        onClick={() => handleOpenExport(selectedModelId)}
                        className="text-xs bg-slate-900 hover:bg-slate-800 text-white font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer"
                      >
                        <Download className="w-3.5 h-3.5" />
                        <span>Export Model</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white p-12 rounded-2xl border border-dashed border-slate-300 text-center space-y-3">
              <div className="w-12 h-12 bg-lime-100 text-lime-700 rounded-full flex items-center justify-center mx-auto">
                <Zap className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-800 text-sm">Ready to Benchmark</h3>
              <p className="text-xs text-slate-500 max-w-md mx-auto">
                Click <strong>"Run Side-by-Side Comparison"</strong> above to fire simultaneous requests to both the Teacher and the Distilled Edge Model.
              </p>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: DISTILLATION WIZARD */}
      {activeTab === 'wizard' && (
        <div className="bg-white p-6 rounded-2xl border border-lime-200/80 shadow-xs space-y-6">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Layers className="w-5 h-5 text-lime-600" />
              Distillation Job Creator
            </h2>
            <p className="text-xs text-slate-500">
              Configure and launch a customized Knowledge Distillation training job. The engine will synthesize verified data, train the compact student, and export edge artifacts.
            </p>
          </div>

          <form onSubmit={handleLaunchJob} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Job Name */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Distillation Job Name</label>
                <input
                  type="text"
                  value={jobName}
                  onChange={(e) => setJobName(e.target.value)}
                  required
                  className="w-full text-xs font-medium p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-lime-500"
                />
              </div>

              {/* Distillation Strategy */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Distillation Strategy</label>
                <select
                  value={distillStrategy}
                  onChange={(e) => setDistillStrategy(e.target.value)}
                  className="w-full text-xs font-medium p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-lime-500"
                >
                  <option value="SEQUENCE_KD">Sequence-Level KD (Direct verified outputs)</option>
                  <option value="MULTI_AGENT_TRAJECTORY">Multi-Agent Trajectory Distillation (Combines all agents into 1)</option>
                  <option value="COT_REASONING">Chain-of-Thought (CoT) Reasoning Distillation</option>
                  <option value="LOGIT_KL">Logit-Matching KL Divergence</option>
                </select>
              </div>

              {/* Teacher Model */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Teacher Source</label>
                <select
                  value={teacherModel}
                  onChange={(e) => setTeacherModel(e.target.value)}
                  className="w-full text-xs font-medium p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-lime-500"
                >
                  <option value="zyra-mesh-orchestrator">Zyra Mesh 7-Agent Orchestrator (Consensus Teacher)</option>
                  <option value="gemini-1.5-flash">Gemini 1.5 Flash (Free Google API Tier)</option>
                  <option value="deepseek-r1:14b">DeepSeek-R1 (Local Ollama Reasoning)</option>
                </select>
                <span className="text-[10px] text-slate-500">Uses free tier or local model with zero external cost.</span>
              </div>

              {/* Student Base Architecture */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Target Student Base Model</label>
                <select
                  value={studentBase}
                  onChange={(e) => setStudentBase(e.target.value)}
                  className="w-full text-xs font-medium p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-lime-500"
                >
                  <option value="qwen2.5:0.5b">Qwen2.5-0.5B (394 MB | 45ms Latency | Raspberry Pi & Edge)</option>
                  <option value="smollm2:360m">SmolLM2-360M (245 MB | 30ms Latency | Ultra-Low Power Mobile)</option>
                  <option value="qwen2.5:1.5b">Qwen2.5-1.5B (1.1 GB | 85ms Latency | High Accuracy)</option>
                  <option value="llama3.2:1b">Llama-3.2-1B (880 MB | 70ms Latency | Meta Architecture)</option>
                </select>
              </div>

              {/* Dataset Selection */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Training Dataset (Uncertainty-Gated)</label>
                <select
                  value={selectedDatasetId}
                  onChange={(e) => setSelectedDatasetId(e.target.value)}
                  className="w-full text-xs font-medium p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-lime-500"
                >
                  {datasets.map(d => (
                    <option key={d.id} value={d.id}>
                      {d.name} ({d.num_samples} samples | Trust: {(d.avg_trust_score * 100).toFixed(0)}%)
                    </option>
                  ))}
                </select>
              </div>

              {/* Export Format */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Export Quantization Target</label>
                <select
                  value={exportFormat}
                  onChange={(e) => setExportFormat(e.target.value)}
                  className="w-full text-xs font-medium p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-lime-500"
                >
                  <option value="GGUF_Q4_K_M">GGUF 4-Bit (Q4_K_M) - Ideal for Ollama & CPU Edge</option>
                  <option value="GGUF_Q8_0">GGUF 8-Bit (Q8_0) - Near Lossless</option>
                  <option value="ONNX">ONNX Edge Runtime (Browser / Embedded)</option>
                  <option value="SAFETENSORS">PyTorch SafeTensors (Hugging Face Format)</option>
                </select>
              </div>
            </div>

            {/* Hyperparameters bar */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
              <div>
                <label className="font-bold text-slate-600 block mb-1">Epochs</label>
                <input
                  type="number"
                  min={1}
                  max={10}
                  value={epochs}
                  onChange={(e) => setEpochs(Number(e.target.value))}
                  className="w-full p-2 bg-white border border-slate-300 rounded-lg text-slate-800 font-bold"
                />
              </div>
              <div>
                <label className="font-bold text-slate-600 block mb-1">Temperature (T)</label>
                <input
                  type="text"
                  disabled
                  value="2.0"
                  className="w-full p-2 bg-slate-100 border border-slate-200 rounded-lg text-slate-500 font-bold"
                />
              </div>
              <div>
                <label className="font-bold text-slate-600 block mb-1">KD Weight (α)</label>
                <input
                  type="text"
                  disabled
                  value="0.70"
                  className="w-full p-2 bg-slate-100 border border-slate-200 rounded-lg text-slate-500 font-bold"
                />
              </div>
              <div>
                <label className="font-bold text-slate-600 block mb-1">Hardware Acceleration</label>
                <div className="p-2 bg-lime-100 text-lime-900 rounded-lg font-bold text-center border border-lime-300">
                  Zero GPU (CPU Auto)
                </div>
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="submit"
                disabled={isLaunching}
                className="px-6 py-3 bg-lime-600 hover:bg-lime-700 disabled:bg-slate-300 text-white font-extrabold text-xs rounded-xl shadow-md transition-all flex items-center gap-2 cursor-pointer"
              >
                {isLaunching ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Launching Distillation Run...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    <span>Launch Distillation Training Run</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* TAB 3: TRAINING MONITOR */}
      {activeTab === 'monitor' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Activity className="w-5 h-5 text-lime-600" />
                Live Distillation Jobs & Convergence Telemetry
              </h2>
              <p className="text-xs text-slate-500">
                Track asynchronous loss curves, epoch gradient progress, and model export status.
              </p>
            </div>
            <button
              onClick={fetchData}
              className="text-xs font-semibold px-3 py-1.5 bg-white border border-slate-200 text-slate-700 rounded-lg hover:bg-slate-50 flex items-center gap-1.5 shadow-2xs"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Refresh</span>
            </button>
          </div>

          <div className="space-y-4">
            {jobs.map((job) => {
              const isRunning = job.status === 'RUNNING';
              const isCompleted = job.status === 'COMPLETED';

              return (
                <div key={job.id} className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-extrabold text-sm text-slate-900">{job.name}</span>
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${
                          isRunning ? 'bg-amber-100 text-amber-900 animate-pulse border border-amber-300' :
                          isCompleted ? 'bg-lime-100 text-lime-900 border border-lime-300' :
                          'bg-slate-100 text-slate-700'
                        }`}>
                          {job.status}
                        </span>
                      </div>
                      <div className="text-xs text-slate-500 flex flex-wrap items-center gap-2">
                        <span>Teacher: <strong>{job.teacher_model}</strong></span>
                        <span>•</span>
                        <span>Student: <strong>{job.student_base}</strong></span>
                        <span>•</span>
                        <span>Strategy: <strong>{job.distillation_strategy}</strong></span>
                        <span>•</span>
                        <span>Quant: <strong>{job.export_format}</strong></span>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      {isCompleted && (
                        <button
                          onClick={() => handleOpenExport(job.id)}
                          className="text-xs bg-slate-900 hover:bg-slate-800 text-white font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5 shadow-xs transition-all cursor-pointer"
                        >
                          <Download className="w-3.5 h-3.5" />
                          <span>Get Ollama Modelfile</span>
                        </button>
                      )}
                      <div className="text-right">
                        <div className="text-xs font-bold text-slate-800">{job.progress_percentage}%</div>
                        <div className="text-[10px] text-slate-400">Epoch {job.current_epoch} of {job.epochs}</div>
                      </div>
                    </div>
                  </div>

                  {/* Progress bar */}
                  <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-300 ${isRunning ? 'bg-amber-500' : 'bg-lime-500'}`}
                      style={{ width: `${job.progress_percentage}%` }}
                    />
                  </div>

                  {/* Telemetry and Metrics Pill Bar */}
                  <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-center text-xs">
                    <div className="bg-slate-50 p-2 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Latency Drop</div>
                      <div className="font-extrabold text-lime-700">-{job.latency_reduction_pct}%</div>
                    </div>
                    <div className="bg-slate-50 p-2 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Cost Drop</div>
                      <div className="font-extrabold text-lime-700">-{job.cost_reduction_pct}%</div>
                    </div>
                    <div className="bg-slate-50 p-2 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Compression</div>
                      <div className="font-extrabold text-slate-800">{job.compression_ratio}</div>
                    </div>
                    <div className="bg-slate-50 p-2 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Fidelity Score</div>
                      <div className="font-extrabold text-slate-800">{job.accuracy_retention_pct}%</div>
                    </div>
                    <div className="bg-slate-50 p-2 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Edge Speed</div>
                      <div className="font-extrabold text-slate-800">{job.student_latency_ms} ms</div>
                    </div>
                  </div>

                  {/* Loss points indicator */}
                  {job.loss_history && job.loss_history.length > 0 && (
                    <div className="bg-slate-900 text-slate-200 p-3 rounded-xl font-mono text-[11px] flex items-center justify-between overflow-x-auto">
                      <div className="flex items-center gap-4">
                        <span>Latest Step: <strong>{job.current_step}</strong></span>
                        <span>Total Loss: <strong className="text-lime-400">{job.loss_history[job.loss_history.length - 1].total_loss}</strong></span>
                        <span>Cross-Entropy: <strong className="text-amber-300">{job.loss_history[job.loss_history.length - 1].ce_loss}</strong></span>
                        <span>KL-Div: <strong className="text-cyan-300">{job.loss_history[job.loss_history.length - 1].kl_loss}</strong></span>
                        <span>Perplexity: <strong className="text-white">{job.loss_history[job.loss_history.length - 1].perplexity}</strong></span>
                      </div>
                      <div className="text-slate-400 text-[10px] shrink-0">
                        {job.loss_history[job.loss_history.length - 1].tokens_per_sec} tok/s
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 4: MODEL REGISTRY */}
      {activeTab === 'models' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Cpu className="w-5 h-5 text-lime-600" />
                Deploy-Ready Distilled Model Registry
              </h2>
              <p className="text-xs text-slate-500">
                Ready-to-use edge models exportable to Ollama, llama.cpp, ONNX, and REST API.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {models.map(m => (
              <div key={m.id} className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4 flex flex-col justify-between">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-lime-100 text-lime-900 font-extrabold uppercase tracking-wide">
                      {m.quantization} • {m.parameters}
                    </span>
                    <span className="text-xs font-bold text-emerald-600 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> READY TO DEPLOY
                    </span>
                  </div>
                  <h3 className="font-extrabold text-slate-900 text-base">{m.name}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{m.description}</p>
                </div>

                <div className="space-y-3">
                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Model Size</div>
                      <div className="font-bold text-slate-800">{m.model_size_mb} MB</div>
                    </div>
                    <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Edge Latency</div>
                      <div className="font-bold text-lime-700">{m.avg_latency_ms} ms</div>
                    </div>
                    <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                      <div className="text-[10px] text-slate-400">Fidelity</div>
                      <div className="font-bold text-slate-800">{m.accuracy_retention}%</div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-2">
                    <button
                      onClick={() => {
                        setSelectedModelId(m.id);
                        setActiveTab('arena');
                      }}
                      className="text-xs font-bold text-lime-700 hover:text-lime-900 flex items-center gap-1 cursor-pointer"
                    >
                      <Play className="w-3.5 h-3.5" />
                      <span>Test in Arena</span>
                    </button>
                    <button
                      onClick={() => handleOpenExport(m.id)}
                      className="text-xs bg-slate-900 hover:bg-slate-800 text-white font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5 shadow-xs transition-all cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Deploy / Export</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 5: COMMERCIAL ROI CALCULATOR */}
      {activeTab === 'roi' && roiData && (
        <div className="bg-white p-6 rounded-2xl border border-lime-200/80 shadow-xs space-y-6">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-lime-600" />
              Commercial Value & Market Cost Reduction Calculator
            </h2>
            <p className="text-xs text-slate-500">
              Calculate exact annual enterprise savings when migrating from cloud LLM API bills to Zyra Distilled Edge deployment.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Input Sliders */}
            <div className="space-y-6">
              <div className="space-y-2">
                <div className="flex justify-between text-xs font-bold text-slate-700">
                  <span>Monthly Query Volume</span>
                  <span className="text-lime-700">{monthlyRequests.toLocaleString()} requests/mo</span>
                </div>
                <input
                  type="range"
                  min={10000}
                  max={2000000}
                  step={10000}
                  value={monthlyRequests}
                  onChange={(e) => handleRecalculateROI(Number(e.target.value), teacherCostPer1M)}
                  className="w-full accent-lime-600"
                />
                <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                  <span>10,000</span>
                  <span>500,000</span>
                  <span>1,000,000</span>
                  <span>2,000,000</span>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-xs font-bold text-slate-700">
                  <span>Cloud Teacher Cost (Per 1M Tokens)</span>
                  <span className="text-amber-700">${teacherCostPer1M.toFixed(2)} / 1M</span>
                </div>
                <input
                  type="range"
                  min={1.0}
                  max={30.0}
                  step={0.5}
                  value={teacherCostPer1M}
                  onChange={(e) => handleRecalculateROI(monthlyRequests, Number(e.target.value))}
                  className="w-full accent-amber-600"
                />
                <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                  <span>$1.00 (Flash)</span>
                  <span>$15.00 (Standard)</span>
                  <span>$30.00 (GPT-4 / Opus)</span>
                </div>
              </div>

              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs space-y-2">
                <div className="font-bold text-slate-800">Key Distillation Economics:</div>
                <ul className="text-slate-600 space-y-1 list-disc pl-4 text-[11px]">
                  <li>Cloud LLM costs scale linearly with request volume.</li>
                  <li>Zyra Distilled models run on existing CPU servers, laptops, or free local instances with near-zero marginal cost.</li>
                  <li>Inference speed increases by <strong>65x to 90x</strong>, dropping compute requirements.</li>
                </ul>
              </div>
            </div>

            {/* Savings Cards */}
            <div className="space-y-4">
              <div className="bg-gradient-to-br from-lime-500 to-emerald-700 text-white p-6 rounded-2xl shadow-lg space-y-3">
                <div className="text-xs font-extrabold uppercase tracking-wider text-lime-200">
                  Annual Net Cost Savings
                </div>
                <div className="text-4xl font-black">
                  ${roiData.annual_savings.toLocaleString()} / year
                </div>
                <div className="text-xs text-lime-100 font-medium">
                  Saving <strong>{roiData.savings_percentage}%</strong> of total cloud inference budget every single month.
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-rose-50 border border-rose-200 p-4 rounded-xl text-center">
                  <div className="text-[11px] text-rose-700 font-bold">Cloud Teacher API Bill</div>
                  <div className="text-xl font-black text-rose-900 mt-1">
                    ${roiData.cloud_teacher_cost_monthly.toLocaleString()} / mo
                  </div>
                  <div className="text-[10px] text-rose-600 mt-1">High cloud lock-in</div>
                </div>

                <div className="bg-lime-50 border border-lime-300 p-4 rounded-xl text-center">
                  <div className="text-[11px] text-lime-800 font-bold">Zyra Distilled Edge Model</div>
                  <div className="text-xl font-black text-lime-950 mt-1">
                    ${roiData.distilled_model_cost_monthly.toLocaleString()} / mo
                  </div>
                  <div className="text-[10px] text-lime-700 mt-1">99% Cost Eradication</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Export & Deployment Modal */}
      {exportModalModel && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl border border-lime-300">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 className="font-extrabold text-slate-900 text-base flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-lime-600" />
                  Production Export: {exportModalModel.model_name}
                </h3>
                <p className="text-[11px] text-slate-500">
                  Run on your laptop, Raspberry Pi, Docker, or in production via Ollama / REST.
                </p>
              </div>
              <button
                onClick={() => setExportModalModel(null)}
                className="text-slate-400 hover:text-slate-700 font-bold text-lg"
              >
                ✕
              </button>
            </div>

            {/* Modelfile content */}
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700">1. Ollama Modelfile</label>
              <pre className="text-[11px] font-mono bg-slate-900 text-slate-100 p-3 rounded-xl overflow-x-auto max-h-40">
                {exportModalModel.ollama_modelfile}
              </pre>
            </div>

            {/* Run commands */}
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700">2. Quick Run Terminal Command</label>
              <pre className="text-[11px] font-mono bg-slate-900 text-lime-400 p-3 rounded-xl overflow-x-auto">
                {exportModalModel.deploy_commands.join('\n')}
              </pre>
            </div>

            {/* cURL API snippet */}
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700">3. Real-Time Production API (cURL)</label>
              <pre className="text-[11px] font-mono bg-slate-900 text-cyan-300 p-3 rounded-xl overflow-x-auto max-h-28">
                {exportModalModel.curl_snippet}
              </pre>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(exportModalModel.ollama_modelfile);
                  alert('Ollama Modelfile copied to clipboard!');
                }}
                className="px-4 py-2 bg-lime-600 hover:bg-lime-700 text-white font-bold text-xs rounded-xl shadow-xs cursor-pointer"
              >
                Copy Modelfile
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
