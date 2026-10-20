import type { 
  Agent, Workflow, ExecutionLog, TrustLeaderboardItem, BenchmarkMetric,
  DistillationJob, DistillationDataset, DistilledModel, DistillationInferenceResult, PricingROI 
} from '../types';

const API_BASE = '/api/v1';


export const api = {
  // Agents
  async getAgents(capability?: string): Promise<Agent[]> {
    const url = capability ? `${API_BASE}/agents?capability=${encodeURIComponent(capability)}` : `${API_BASE}/agents`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch agents');
    return res.json();
  },

  async getAgentDetails(agentId: string): Promise<Agent> {
    const res = await fetch(`${API_BASE}/agents/${agentId}`);
    if (!res.ok) throw new Error('Agent not found');
    return res.json();
  },

  // Workflows
  async submitWorkflow(payload: {
    raw_user_objective: string;
    execution_strategy: string;
    ablation_config: Record<string, boolean>;
    max_budget?: number;
    max_latency_ms?: number;
  }): Promise<Workflow> {
    const res = await fetch(`${API_BASE}/workflows/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to submit workflow');
    return res.json();
  },

  async getWorkflow(workflowId: string): Promise<Workflow> {
    const res = await fetch(`${API_BASE}/workflows/${workflowId}`);
    if (!res.ok) throw new Error('Workflow not found');
    return res.json();
  },

  async getACTG(workflowId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/workflows/${workflowId}/actg`);
    if (!res.ok) throw new Error('Failed to fetch ACTG');
    return res.json();
  },

  async executeWorkflow(workflowId: string): Promise<{ status: string }> {
    const res = await fetch(`${API_BASE}/workflows/${workflowId}/execute`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to start execution');
    return res.json();
  },

  // Executions
  async getExecutions(workflowId: string): Promise<ExecutionLog[]> {
    const res = await fetch(`${API_BASE}/executions/workflow/${workflowId}`);
    if (!res.ok) throw new Error('Failed to fetch execution logs');
    return res.json();
  },

  // Trust Analytics
  async getTrustLeaderboard(): Promise<TrustLeaderboardItem[]> {
    const res = await fetch(`${API_BASE}/trust/leaderboard`);
    if (!res.ok) throw new Error('Failed to fetch trust leaderboard');
    return res.json();
  },

  // Evaluation & Benchmarking
  async runBenchmark(numSamples: number = 10): Promise<BenchmarkMetric[]> {
    const res = await fetch(`${API_BASE}/eval/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ num_samples: numSamples }),
    });
    if (!res.ok) throw new Error('Failed to execute evaluation benchmark');
    return res.json();
  },

  async getEvaluationMetrics(): Promise<BenchmarkMetric[]> {
    const res = await fetch(`${API_BASE}/eval/metrics`);
    if (!res.ok) throw new Error('Failed to fetch evaluation metrics');
    return res.json();
  },

  // Stats & Overview
  async getOverviewStats() {
    const res = await fetch(`${API_BASE}/stats/overview`);
    if (!res.ok) throw new Error('Failed to fetch overview stats');
    return res.json();
  },

  // Auth & Security
  async login(username: string, password: string = 'password') {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem('zyra_token', data.access_token);
    }
    return data;
  },

  async getMe() {
    const token = localStorage.getItem('zyra_token');
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!res.ok) throw new Error('Failed to fetch user profile');
    return res.json();
  },

  // Agent Management
  async registerAgent(agentData: any): Promise<Agent> {
    const res = await fetch(`${API_BASE}/agents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(agentData)
    });
    if (!res.ok) throw new Error('Failed to register agent');
    return res.json();
  },

  async updateAgent(agentId: string, agentData: any): Promise<Agent> {
    const res = await fetch(`${API_BASE}/agents/${agentId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(agentData)
    });
    if (!res.ok) throw new Error('Failed to update agent');
    return res.json();
  },

  async getWorkflowAudit(workflowId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/workflows/${workflowId}/audit`);
    if (!res.ok) throw new Error('Failed to fetch workflow audit trace');
    return res.json();
  },

  async getTrustObservations(agentId?: string): Promise<any[]> {
    const url = agentId ? `${API_BASE}/trust/observations?agent_id=${agentId}` : `${API_BASE}/trust/observations`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch trust observations');
    return res.json();
  },

  async runAblation(numSamples: number = 10, seed: number = 42): Promise<BenchmarkMetric[]> {
    const res = await fetch(`${API_BASE}/eval/ablation`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ num_samples: numSamples, seed }),
    });
    if (!res.ok) throw new Error('Failed to run ablation study');
    return res.json();
  },

  async runStressTest(agentCounts: number[] = [10, 25, 50, 100, 250], seed: number = 42) {
    const res = await fetch(`${API_BASE}/eval/stress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent_counts: agentCounts, seed }),
    });
    if (!res.ok) throw new Error('Failed to run stress test');
    return res.json();
  },

  async injectFailure(payload: {
    agent_id?: string;
    failure_type: string;
    target_task_index?: number;
    enabled: boolean;
  }) {
    const res = await fetch(`${API_BASE}/simulations/inject-failure`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to set failure injection');
    return res.json();
  },

  async getSimulationState() {
    const res = await fetch(`${API_BASE}/simulations/state`);
    if (!res.ok) throw new Error('Failed to fetch simulation state');
    return res.json();
  },

  // Distillation as a Service (DaaS)
  async getDistillationJobs(): Promise<DistillationJob[]> {
    const res = await fetch(`${API_BASE}/distill/jobs`);
    if (!res.ok) throw new Error('Failed to fetch distillation jobs');
    return res.json();
  },

  async getDistillationJob(jobId: string): Promise<DistillationJob> {
    const res = await fetch(`${API_BASE}/distill/jobs/${jobId}`);
    if (!res.ok) throw new Error('Failed to fetch distillation job details');
    return res.json();
  },

  async createDistillationJob(payload: {
    name: string;
    description?: string;
    teacher_model: string;
    student_base: string;
    distillation_strategy: string;
    dataset_id?: string;
    epochs?: number;
    batch_size?: number;
    learning_rate?: number;
    temperature?: number;
    alpha_kd?: number;
    export_format?: string;
  }): Promise<DistillationJob> {
    const res = await fetch(`${API_BASE}/distill/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to create distillation job');
    return res.json();
  },

  async cancelDistillationJob(jobId: string): Promise<DistillationJob> {
    const res = await fetch(`${API_BASE}/distill/jobs/${jobId}/cancel`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to cancel distillation job');
    return res.json();
  },

  async getDistillationDatasets(): Promise<DistillationDataset[]> {
    const res = await fetch(`${API_BASE}/distill/datasets`);
    if (!res.ok) throw new Error('Failed to fetch distillation datasets');
    return res.json();
  },

  async generateDistillationDataset(payload: {
    name: string;
    domain: string;
    num_samples: number;
    teacher_source: string;
    uncertainty_threshold: number;
  }): Promise<DistillationDataset> {
    const res = await fetch(`${API_BASE}/distill/generate-dataset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to generate dataset');
    return res.json();
  },

  async getDistilledModels(): Promise<DistilledModel[]> {
    const res = await fetch(`${API_BASE}/distill/models`);
    if (!res.ok) throw new Error('Failed to fetch distilled models');
    return res.json();
  },

  async runDistillationInference(payload: {
    prompt: string;
    student_model_id?: string;
    teacher_model?: string;
    compare_teacher?: boolean;
  }): Promise<DistillationInferenceResult> {
    const res = await fetch(`${API_BASE}/distill/infer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to execute distillation inference');
    return res.json();
  },

  async getPricingROI(monthlyRequests: number = 100000, teacherCost: number = 15.0): Promise<PricingROI> {
    const res = await fetch(`${API_BASE}/distill/roi?monthly_requests=${monthlyRequests}&teacher_cost_per_1m=${teacherCost}`);
    if (!res.ok) throw new Error('Failed to calculate pricing ROI');
    return res.json();
  },

  async exportDistilledModel(modelId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/distill/export/${encodeURIComponent(modelId)}`);
    if (!res.ok) throw new Error('Failed to export model');
    return res.json();
  }
};

