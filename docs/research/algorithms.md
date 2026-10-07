# ZyraMesh Algorithms & Pseudo-code

## Algorithm 1: 2-Stage Cross-Graph Matching & Soft Ranking

```text
Input: Subtask t, Candidate Agents A, Parameter k
Output: Ranked Candidate List R

Stage 1: Hard Filtering
For each agent a in A:
    If a.status != ACTIVE: Reject
    If t.required_capabilities not subset of a.capabilities: Reject
    If t.required_tools not subset of a.tools: Reject
    If a.expected_latency > t.max_latency: Reject
    Keep a in ValidCandidates C

Stage 2: Soft Ranking
For each candidate c in C:
    conservative_trust = c.trust_mean - k * c.trust_uncertainty
    capability_fit = calculate_fit(t.required_capabilities, c.capabilities)
    collab_score = lookup_collaboration_memory(prior_agent, c)
    cost_penalty = c.cost_per_execution / max_cost
    latency_penalty = c.expected_latency / max_latency
    
    score = 0.35 * capability_fit + 0.30 * conservative_trust + 0.15 * collab_score - 0.10 * cost_penalty - 0.10 * latency_penalty
    Add (c, score) to R

Sort R in descending order of score
Return R
```

## Algorithm 2: Dynamic In-Flight Re-Orchestration

```text
Input: Workflow W, Failed Subtask t, Failed Agent a_f, Audit Log L
Output: Updated Workflow W' with Replacement Agent a_r

1. Trigger event: SIMULATED_FAILURE / SCHEMA_INVALID / VERIFIER_REJECTION
2. Mark task t state as RE_ROUTING
3. Query Marketplace for Candidate Agents C excluding a_f
4. Execute Stage 1 & Stage 2 matching for subtask t
5. If top candidate a_r found:
      Update task t assigned_agent_id = a_r.agent_id
      Re-execute subtask t with candidate a_r
      Emit event AGENT_RE_ROUTED
      Update Bayesian capability trust for a_f (penalize) and a_r (reward)
      Resume Workflow W execution
   Else:
      Escalate task t to HUMAN_REVIEW / FAILED
```
