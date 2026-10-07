# ZyraMesh Methodology & Formulation

## Problem Statement
Open agent marketplaces exhibit high dynamics: agent capabilities overlap, reliability fluctuates, and execution outputs may degrade or fail due to schema mismatch, hallucination, or tool timeouts. Traditional static multi-agent pipelines fail under runtime failure.

## Key Theoretical Contributions

### 1. Dual-Graph Representation
- **Task Dependency Graph (TDG)** \( G_{TDG} = (V_T, E_T) \): A Directed Acyclic Graph where nodes \( v_i \in V_T \) represent subtasks and directed edges \( (v_i, v_j) \in E_T \) enforce dependency ordering.
- **Agent Capability-Trust Graph (ACTG)** \( G_{ACTG} = (V_A \cup V_C \cup V_O, E_{cap} \cup E_{tool} \cup E_{collab}) \): A heterogeneous graph encoding agent capabilities, tools, and pairwise handoff compatibility.

### 2. Conservative Trust Formulation
To prevent over-optimistic assignment of unverified or high-variance agents, agent candidate selection uses conservative trust bound:
\[ \text{trust}_{\text{conservative}} = \mu_i - k \cdot \sigma_i \]
where \( \mu_i \) is the capability-specific trust mean, \( \sigma_i \) is the trust uncertainty standard deviation, and \( k \) is a risk penalty coefficient (default \( k = 1.0 \)).

### 3. Multi-Signal Uncertainty Gate
Uncertainty \( U(o) \) for output \( o \) is computed as:
\[ U(o) = w_1 \cdot (1 - c) + w_2 \cdot H(o) + w_3 \cdot \delta_{\text{verifier}} + w_4 \cdot \text{Risk}_{\text{prop}} \]
If \( U(o) > \tau_{\text{verify}} \) (default \( 0.40 \)), output verification is triggered.
