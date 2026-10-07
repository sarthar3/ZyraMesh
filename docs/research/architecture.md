# Zyra & ZyraMesh System Architecture

## Overview
**Zyra** is an open, intelligent multi-agent marketplace platform, while **ZyraMesh** represents its underlying research methodology: *Trust-Calibrated Dual-Graph Agent Team Formation with Uncertainty-Gated Re-Orchestration*.

## Architectural Layers

```
                                  +-----------------------+
                                  |   USER INTERFACE      |
                                  | React + TS Dashboard  |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  |   FASTAPI GATEWAY     |
                                  | CORS, Security, Auth  |
                                  +-----------+-----------+
                                              |
      +---------------------------------------+---------------------------------------+
      |                                       |                                       |
      v                                       v                                       v
+-----------------------+           +-----------------------+           +-----------------------+
|  DUAL-GRAPH ENGINE    |           |    RUNTIME ENGINE     |           |  RESEARCH EVALUATION  |
| - TDG DAG Builder     |           | - Runtime Orchestrator|           | - Baseline Suite (6)  |
| - ACTG Builder        |           | - Uncertainty Gate    |           | - Ablation Suite (7)  |
| - Cross-Graph Matcher |           | - Verifier Engine     |           | - Stress Test Engine  |
| - Team Composer       |           | - Dynamic Re-Orch     |           | - Audit & Telemetry   |
+-----------------------+           +-----------------------+           +-----------------------+
      |                                       |                                       |
      +---------------------------------------+---------------------------------------+
                                              |
                                              v
                                  +-----------------------+
                                  |    DATA & STORAGE     |
                                  | SQLite/PostgreSQL DB  |
                                  | DaaS Data Providers   |
                                  +-----------------------+
```

### 1. Dual-Graph Engine
- **Task Dependency Graph (TDG)**: Captures subtask decomposition, required capabilities, tools, input/output schemas, sensitivity, criticality, and topological dependency order.
- **Agent Capability-Trust Graph (ACTG)**: Models heterogeneous marketplace topology mapping Agents, Capability Nodes, Tool Nodes, Permission Boundaries, Bayesian Trust Distributions, and Pairwise Collaboration Edges.

### 2. Runtime Engine
- **Async Runtime Orchestrator**: Executes task DAGs while emitting real-time WebSocket events.
- **Multi-Signal Uncertainty Gate**: Evaluates aleatoric entropy, trust variance, verifier disagreement, and schema validity to compute risk scores.
- **Verification System**: Inspects high-uncertainty task outputs using dual-oracle inspection.
- **Dynamic Re-Orchestrator**: Reroutes subtasks in-flight to replacement marketplace candidates upon failure.

### 3. Bayesian Trust & Collaboration Memory
- **Evidence-Driven Bayesian Engine**: Updates capability-specific trust means and variance upon verification observations.
- **Pairwise Collaboration Memory**: Records handoff success rates, schema compatibility, and latency between agent pairs.
