# ZyraMesh Failure Simulation & Recovery Scenarios

## Supported Deterministic Failure Injection Scenarios

### 1. Schema Failure (`SCHEMA_FAILURE`)
- **Simulated Behavior**: Agent produces malformed or invalid JSON output failing Pydantic schema validation.
- **Recovery Sequence**:
  1. Output schema validator flags failure.
  2. Uncertainty Gate elevates score to 0.85 (CRITICAL).
  3. Verifier rejects output (agreement = 0.20).
  4. Dynamic Re-Orchestrator searches marketplace for alternative candidate.
  5. Subtask rerouted to replacement agent.
  6. Replacement succeeds; failing agent trust penalized.

### 2. Execution Timeout (`TIMEOUT`)
- **Simulated Behavior**: Agent execution latency exceeds maximum SLA limit (e.g. > 5000ms).
- **Recovery Sequence**: Async orchestrator cancels hanging request, marks task RE_ROUTING, and transfers subtask to secondary agent with lower latency.

### 3. Verifier Disagreement (`VERIFIER_DISAGREEMENT`)
- **Simulated Behavior**: Dual-oracle verifiers disagree on evidence quality.
- **Recovery Sequence**: Triggers human review or secondary verifier consensus round.
