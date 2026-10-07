# ZyraMesh Ablation Experiment Methodology

## Purpose
Ablation studies isolate and quantify the explicit contribution of each major design component in the ZyraMesh methodology by disabling components one by one.

## 7 Ablation Configurations

1. **`FULL_ZYRA`**: Complete proposed pipeline with all features active.
2. **`NO_TDG`**: Disables Task Dependency Graph DAG structure; subtasks execute in flat arbitrary sequence.
3. **`GLOBAL_TRUST_ONLY`**: Replaces capability-specific trust with a single global agent trust score.
4. **`NO_UNCERTAINTY_PENALTY`**: Sets conservative trust parameter \( k = 0 \), ignoring trust variance during matching.
5. **`NO_COLLABORATION_MEMORY`**: Disables pairwise handoff compatibility lookup.
6. **`NO_GUARDRAILS`**: Disables prompt injection and safety policy checks.
7. **`NO_REORCHESTRATION`**: Disables in-flight subtask rerouting upon task failure.
