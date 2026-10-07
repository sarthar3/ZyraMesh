# ZyraMesh Baseline Strategy Definitions

## 1. Single Generalist Agent (`SINGLE_GENERALIST`)
A single monolithic LLM generalist agent attempts to execute all subtasks sequentially without dynamic agent decomposition or specialized tool interfaces.

## 2. Fixed Multi-Agent Team (`FIXED_MULTI_AGENT`)
A static, hardcoded team of multi-agent roles is assigned at workflow submission. No dynamic matching or in-flight replacement occurs if an agent degrades.

## 3. Capability-Only Selection (`CAPABILITY_ONLY`)
Agents are matched strictly based on capability tag overlap. Trust mean, uncertainty variance, cost, and latency SLAs are ignored during team formation.

## 4. Reputation/Trust-Only Selection (`REPUTATION_ONLY`)
Agents are selected solely based on global trust score. Capability fit and tool compatibility are not constrained.

## 5. Dynamic Baseline (`DYNAMIC_BASELINE`)
Dynamic matching with basic heuristic scoring, but without dual-graph ACTG synergy or conservative trust bounds.

## 6. ZyraMesh Full System (`ZYRAMESH`)
Proposed framework featuring dual-graph TDG+ACTG team formation, conservative trust ranking, multi-signal uncertainty gate, and dynamic in-flight re-orchestration.
