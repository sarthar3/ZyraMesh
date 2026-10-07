export interface Agent {
  agent_id: string;
  name: string;
  description: string;
  capabilities: string[];
  tools: Array<{ name: string; type: string }>;
  model_backend: string;
  cost_per_1k_tokens: number;
  avg_latency_ms: number;
  availability_status: string;
  permissions: string[];
  provenance: Record<string, any>;
  trust_mean: number;
  trust_uncertainty: number;
  capability_specific_trust: Record<string, { mean: number; var: number }>;
  collaboration_history: Record<string, { count: number; success_rate: number }>;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Subtask {
  task_id: string;
  subtask_index: number;
  description: string;
  required_capabilities: string[];
  required_tools: string[];
  sensitivity_score: number;
  criticality_score: number;
  propagation_risk: number;
  verification_requirement: string;
  dependencies: string[];
  assigned_agent_id?: string;
  assigned_agent_name?: string;
  status: string;
  match_score?: number;
}

export interface Workflow {
  workflow_id: string;
  raw_user_objective: string;
  status: string;
  execution_strategy: string;
  ablation_config: Record<string, boolean>;
  tdg_structure?: {
    nodes: Array<any>;
    edges: Array<any>;
  };
  tasks: Subtask[];
  created_at: string;
  completed_at?: string;
}

export interface ExecutionLog {
  execution_id: string;
  workflow_id: string;
  task_id: string;
  agent_id: string;
  agent_name?: string;
  input_data: Record<string, any>;
  output_data?: Record<string, any>;
  confidence_score?: number;
  uncertainty_score?: number;
  schema_valid?: boolean;
  verifier_agreement?: number;
  evidence_score?: number;
  tool_trace: Array<{ tool: string; status: string }>;
  policy_status: string;
  start_time: string;
  end_time?: string;
  status: string;
}

export interface TrustLeaderboardItem {
  agent_id: string;
  name: string;
  trust_mean: number;
  trust_uncertainty: number;
  capability_trust: Record<string, { mean: number; var: number }>;
  total_executions: number;
  success_rate: number;
}

export interface BenchmarkMetric {
  metric_id: string;
  run_id: string;
  strategy: string;
  ablation: string;
  workflow_success_rate: number;
  failure_propagation_rate: number;
  expected_calibration_error: number;
  avg_latency_ms: number;
  total_cost: number;
  verification_frequency: number;
  rerouting_success_rate: number;
  policy_violations_count: number;
  sample_size: number;
  timestamp: string;
}
