# Zyra – An Intelligent Multi-Agent Marketplace & Orchestration Platform

Research Paper Extension:
> **ZyraMesh: Trust-Calibrated Dual-Graph Agent Team Formation with Uncertainty-Gated Re-Orchestration for Open Agent Marketplaces**

---

## 1. Project Overview

**Zyra** is an open, intelligent multi-agent marketplace platform where specialized AI agents register capabilities, tools, backend model providers, SLAs, costs, permissions, trust distributions, and historical collaboration memory.

When a user submits a complex objective (e.g., *"Find the best laptop under ₹70,000 for AI development"*), Zyra:
1. Decomposes the objective into a **Task Dependency Graph (TDG)** DAG using NetworkX.
2. Builds an **Agent Capability-Trust Graph (ACTG)** capturing calibrated trust distributions \((\mu_{\text{trust}}, \sigma^2_{\text{trust}})\) and handoff compatibility.
3. Solves constrained team composition optimizing capability fit, conservative trust bounds, collaboration synergy, and policy risk.
4. Executes tasks asynchronously through an **Uncertainty-Gated Controller**.
5. Triggers **Selective Dual-Oracle Verification** for high-risk steps.
6. Performs dynamic **In-Flight Re-Orchestration & Rerouting** upon failure detection or verifier rejection.
7. Updates capability-specific agent trust using evidence-driven Bayesian learning.
8. Logs immutable execution audit traces with complete explainability.
9. Runs non-synthetic research evaluations across 6 baselines, 7 ablation configurations, and stress testing scalability up to 250 agents.

---

## 2. Technology Stack

- **Backend**: Python 3.11+ + FastAPI + Pydantic v2 + SQLAlchemy 2.0 + NetworkX + Pytest
- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS + Lucide Icons + React Flow
- **Database**: PostgreSQL / SQLite (zero-config local dev)
- **AI Providers**: Local Ollama (`qwen2.5:1.5b-instruct`), Gemini API (`gemini-1.5-flash`), Mock Adapter
- **Deployment**: Docker, Docker Compose, Nginx

---

## 3. Quick Start & Running Locally

### Option A: Local Development Server

#### 1. Start Backend

```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

# Run automated unit test suite (16/16 tests)
pytest

# Start FastAPI server
uvicorn app.main:app --port 8000 --reload
```
- Swagger API Docs: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/health`

#### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```
- Web Application Dashboard: `http://localhost:3000` (or `http://localhost:5173`)

---

### Option B: Docker Compose Deployment

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

---

## 4. 14 Live Dashboard Pages (Module 19)

1. **Home / Overview** (`/`): Dynamic real-time statistics, active agent count, total workflows, avg latency, avg trust, and top calibrated marketplace agents.
2. **Agent Marketplace** (`/marketplace`): Marketplace grid view with capability, category, trust, cost, and availability filters.
3. **Agent Details** (`/marketplace/:agentId`): Capability breakdown, expected latency, token cost, trust history timeline, and collaboration links.
4. **Task Submission** (`/submit`): Natural language objective prompt input with max budget, SLA deadline, risk tolerance, and ablation toggles.
5. **TDG Visualization** (`/tdg`): Interactive React Flow task dependency graph DAG showing node execution states.
6. **ACTG Visualization** (`/actg`): Network topology graph mapping Agents, Capabilities, Tools, and Collaboration edges.
7. **Team Formation View** (`/team`): Constrained matching assignment breakdown with explicit AI selection explanations.
8. **Live Workflow Execution** (`/execution`): Real-time event log, progress bars, task states, and output streams.
9. **Uncertainty Gate** (`/uncertainty`): Multi-signal uncertainty gate inspector evaluating aleatoric entropy, schema validity, and propagation risk.
10. **Re-Orchestration View** (`/reorchestration`): In-flight rerouting visualizer showing failed agent, candidate ranking, replacement selection, and task continuation.
11. **Trust Analytics** (`/trust`): Bayesian trust update leaderboard and observation log.
12. **Workflow History** (`/history`): Workflow audit trace log viewer with downloadable JSON export.
13. **Evaluation Dashboard** (`/evaluation`): Empirical benchmark results across 6 baselines, 7 ablation configurations, stress testing (10 to 250 agents), and CSV/JSON export.
14. **Admin Management & Demo Panel** (`/admin`): Agent registration console and **Module 27 Failure Simulation Controller**.

---

## 5. Step-by-Step Final Project Demonstration Guide

Follow these 25 steps for the final-year project demonstration:

1. **Open Zyra Application**: Navigate to `http://localhost:3000`.
2. **View Home Overview**: Point out live dynamic metrics (total agents, active agents, average trust, avg latency).
3. **Navigate to Agent Marketplace**: Show registered specialized seed agents (`ProductSearchAgent-A`, `SpecificationAgent-A`, `PriceVerificationAgent`, `ReviewAnalysisAgent`, `RecommendationAgent`, `VerificationAgent`).
4. **Filter Agents**: Filter by category (`shopping`) and capability (`search`, `specification`).
5. **Inspect Agent Detail**: Click `SpecificationAgent-A` to show capability trust distribution (\(\mu = 0.88, \sigma = 0.12\)) and historical performance.
6. **Open Task Submission**: Go to Task Submission page (`/submit`).
7. **Enter Objective**: Type: *"Find the best laptop under ₹70,000 for AI development"*.
8. **Configure Parameters**: Set Max Budget = ₹70,000, SLA Deadline = 5000ms, Execution Strategy = `ZYRAMESH`.
9. **Submit Objective**: Click **Submit Objective & Form Team**.
10. **Inspect TDG Graph**: View the generated Task Dependency Graph DAG on `/tdg`.
11. **Inspect ACTG Topology**: Navigate to `/actg` to show the Agent Capability-Trust Graph.
12. **Inspect Team Composition**: Go to `/team` to show assigned candidate agents and backend explanations explaining why `SpecificationAgent-A` was selected.
13. **Arm Failure Injection (Module 27)**: Open `/admin` in another tab or use the Failure Simulation Panel, select `SpecificationAgent-A` -> `SCHEMA_FAILURE`, and click **Arm Failure Injection**.
14. **Start Live Execution**: Go to `/execution` and click **Execute Workflow**.
15. **Observe Task 1 Completion**: Watch `ProductSearchAgent-A` complete product search.
16. **Observe Task 2 Failure Injection**: Watch `SpecificationAgent-A` trigger a simulated schema failure.
17. **Observe Uncertainty Escalation**: Watch Uncertainty Gate detect schema invalidity and elevate risk score to CRITICAL (0.85).
18. **Observe Verification Rejection**: Watch VerifierEngine reject task output (agreement = 0.20).
19. **Observe Re-Orchestration Trigger**: Watch ReOrchestratorEngine search marketplace for alternative specification agents.
20. **Observe Candidate Ranking & Replacement**: Watch `SpecificationAgent-B` selected as the optimal replacement agent.
21. **Observe Task Rerouting & Resume**: Watch task rerouted to `SpecificationAgent-B`, execute successfully, and output valid laptop specifications.
22. **Observe Workflow Completion**: Watch remaining review, price check, and recommendation steps complete smoothly.
23. **Inspect Audit Trace**: Open `/history`, click **Inspect Audit Trace**, and view the complete event chronology log. Export JSON.
24. **Inspect Trust Leaderboard**: Open `/trust` to show Bayesian trust updates (`SpecificationAgent-A` trust penalized, `SpecificationAgent-B` rewarded).
25. **Run Evaluation & Ablations**: Open `/evaluation`, click **Run Baseline Experiments**, switch to **Ablation Experiments** tab, click **Run Ablation Study**, and click **Export CSV**.

---

## 6. Academic Research Documentation

Located in `docs/research/`:
- `architecture.md` – End-to-end system layer architecture.
- `methodology.md` – Dual-graph theoretical formulation and math.
- `algorithms.md` – Matching and re-orchestration pseudo-code.
- `database_schema.md` – Entity relation design.
- `api_design.md` – REST API specifications.
- `evaluation_methodology.md` – Metric definitions.
- `baseline_definitions.md` – 6 baseline execution strategies.
- `ablation_methodology.md` – 7 ablation configurations.
- `stress_testing_methodology.md` – Scalability benchmarks (10 to 250 agents).
- `failure_scenarios.md` – Deterministic failure recovery sequences.
- `limitations.md` – System boundaries.
