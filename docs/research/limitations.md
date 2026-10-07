# ZyraMesh System Limitations & Research Boundary

## Explicitly Stated System Boundaries

1. **Local Hardware Constraints**:
   - Default local execution uses lightweight Ollama `qwen2.5:1.5b-instruct` or deterministic Mock adapters. Complex reasoning performance depends on underlying LLM model parameter capacity.

2. **DaaS Data Scope**:
   - E-commerce laptop pricing and specs originate from curated local JSON/Mock Data-as-a-Service providers (`data_mode = MOCK / CACHED`) to prevent rate-limiting or anti-scraping blocks. Live web scraping is disabled by policy.

3. **Bayesian Cold-Start Sensitivity**:
   - Newly registered agents with high variance \(\sigma^2\) are penalized initially by conservative trust bounds \( \mu - k \cdot \sigma \) until sufficient observation history accumulates.

4. **Network Graph Scale**:
   - Exact graph topological matching complexity increases quadratically for teams exceeding 50 agents per single workflow.
