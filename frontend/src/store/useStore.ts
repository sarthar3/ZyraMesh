import { create } from 'zustand';
import type { Agent, Workflow, ExecutionLog, TrustLeaderboardItem, BenchmarkMetric } from '../types';
import { api } from '../services/api';

interface StoreState {
  agents: Agent[];
  activeWorkflow: Workflow | null;
  executionLogs: ExecutionLog[];
  leaderboard: TrustLeaderboardItem[];
  evaluationMetrics: BenchmarkMetric[];
  isExecuting: boolean;
  liveEvents: Array<{ event_type: string; data: any; timestamp: string }>;
  
  fetchAgents: () => Promise<void>;
  fetchTrustLeaderboard: () => Promise<void>;
  fetchMetrics: () => Promise<void>;
  submitObjective: (objective: string, strategy: string, ablations: Record<string, boolean>) => Promise<Workflow>;
  startExecution: (workflowId: string) => Promise<void>;
  loadWorkflowDetails: (workflowId: string) => Promise<void>;
  addLiveEvent: (event: { event_type: string; data: any; timestamp: string }) => void;
}

export const useStore = create<StoreState>((set, get) => ({
  agents: [],
  activeWorkflow: null,
  executionLogs: [],
  leaderboard: [],
  evaluationMetrics: [],
  isExecuting: false,
  liveEvents: [],

  fetchAgents: async () => {
    try {
      const agents = await api.getAgents();
      set({ agents });
    } catch (e) {
      console.error(e);
    }
  },

  fetchTrustLeaderboard: async () => {
    try {
      const leaderboard = await api.getTrustLeaderboard();
      set({ leaderboard });
    } catch (e) {
      console.error(e);
    }
  },

  fetchMetrics: async () => {
    try {
      const evaluationMetrics = await api.getEvaluationMetrics();
      set({ evaluationMetrics });
    } catch (e) {
      console.error(e);
    }
  },

  submitObjective: async (objective: string, strategy: string, ablations: Record<string, boolean>) => {
    const workflow = await api.submitWorkflow({
      raw_user_objective: objective,
      execution_strategy: strategy,
      ablation_config: ablations
    });
    set({ activeWorkflow: workflow, liveEvents: [] });
    return workflow;
  },

  startExecution: async (workflowId: string) => {
    set({ isExecuting: true });
    await api.executeWorkflow(workflowId);
    const interval = setInterval(async () => {
      try {
        const logs = await api.getExecutions(workflowId);
        const wf = await api.getWorkflow(workflowId);
        set({ executionLogs: logs, activeWorkflow: wf });
        if (wf.status === 'COMPLETED' || wf.status === 'FAILED') {
          clearInterval(interval);
          set({ isExecuting: false });
          get().fetchTrustLeaderboard();
        }
      } catch (e) {
        clearInterval(interval);
        set({ isExecuting: false });
      }
    }, 1500);
  },

  loadWorkflowDetails: async (workflowId: string) => {
    try {
      const wf = await api.getWorkflow(workflowId);
      const logs = await api.getExecutions(workflowId);
      set({ activeWorkflow: wf, executionLogs: logs });
    } catch (e) {
      console.error(e);
    }
  },

  addLiveEvent: (event) => {
    set((state) => ({ liveEvents: [event, ...state.liveEvents] }));
  }
}));
