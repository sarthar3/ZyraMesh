from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import datetime
from app.models.agent import AgentModel
from app.schemas.agent import AgentCreate, AgentUpdate

SEED_AGENTS = [
    {
        "agent_id": "ProductSearchAgent-A",
        "name": "E-Commerce Fast Search Agent",
        "description": "Searches marketplace inventory rapidly with flexible fuzzy keyword matching.",
        "category": "shopping",
        "capabilities": ["product_search", "data_retrieval"],
        "tools": [{"name": "fast_catalog_search", "type": "search_engine"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0008,
        "cost_per_1k_tokens": 0.0008,
        "expected_latency": 110,
        "avg_latency_ms": 110,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["db_read", "standard"],
        "provenance": {"developer": "ShopEngine AI", "tier": "verified"},
        "global_trust": 0.88,
        "trust_mean": 0.88,
        "trust_uncertainty": 0.06,
        "capability_specific_trust": {
            "product_search": {"mean": 0.90, "var": 0.04},
            "data_retrieval": {"mean": 0.86, "var": 0.08}
        },
        "successful_executions": 120,
        "failed_executions": 5,
        "verifier_agreement": 0.92,
        "schema_validity": 0.96,
        "tool_success": 0.98,
        "recent_performance": 0.90,
        "historical_performance": 0.88,
        "collaboration_history": {
            "SpecificationAgent-A": {"count": 45, "success_rate": 0.95}
        }
    },
    {
        "agent_id": "ProductSearchAgent-B",
        "name": "Deep Inventory Query Agent",
        "description": "High-precision product database retrieval supporting detailed category filtering.",
        "category": "shopping",
        "capabilities": ["product_search", "data_retrieval", "query_optimization"],
        "tools": [{"name": "deep_db_query", "type": "database_connector"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0015,
        "cost_per_1k_tokens": 0.0015,
        "expected_latency": 220,
        "avg_latency_ms": 220,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["db_read", "standard"],
        "provenance": {"developer": "DataPipeline Inc", "tier": "community"},
        "global_trust": 0.94,
        "trust_mean": 0.94,
        "trust_uncertainty": 0.03,
        "capability_specific_trust": {
            "product_search": {"mean": 0.95, "var": 0.02},
            "data_retrieval": {"mean": 0.93, "var": 0.03}
        },
        "successful_executions": 210,
        "failed_executions": 4,
        "verifier_agreement": 0.96,
        "schema_validity": 0.98,
        "tool_success": 0.99,
        "recent_performance": 0.95,
        "historical_performance": 0.94,
        "collaboration_history": {
            "SpecificationAgent-B": {"count": 60, "success_rate": 0.97}
        }
    },
    {
        "agent_id": "SpecificationAgent-A",
        "name": "Hardware Tech Spec Analyzer",
        "description": "Extracts detailed technical specs (CPU, GPU, RAM, VRAM, Battery) from product listings.",
        "category": "shopping",
        "capabilities": ["specification_analysis", "schema_validation"],
        "tools": [{"name": "spec_parser", "type": "extractor"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0012,
        "cost_per_1k_tokens": 0.0012,
        "expected_latency": 160,
        "avg_latency_ms": 160,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["standard"],
        "provenance": {"developer": "TechAudit Labs", "tier": "verified"},
        "global_trust": 0.91,
        "trust_mean": 0.91,
        "trust_uncertainty": 0.04,
        "capability_specific_trust": {
            "specification_analysis": {"mean": 0.93, "var": 0.03},
            "schema_validation": {"mean": 0.89, "var": 0.05}
        },
        "successful_executions": 95,
        "failed_executions": 3,
        "verifier_agreement": 0.94,
        "schema_validity": 0.97,
        "tool_success": 0.96,
        "recent_performance": 0.92,
        "historical_performance": 0.91,
        "collaboration_history": {}
    },
    {
        "agent_id": "SpecificationAgent-B",
        "name": "Fast Specification Extractor",
        "description": "Lightweight specification parser optimized for low-latency batch processing.",
        "category": "shopping",
        "capabilities": ["specification_analysis"],
        "tools": [{"name": "regex_spec_extractor", "type": "parser"}],
        "model_backend": "mock",
        "model_name": "mock/deterministic",
        "cost_per_execution": 0.0004,
        "cost_per_1k_tokens": 0.0004,
        "expected_latency": 60,
        "avg_latency_ms": 60,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["standard"],
        "provenance": {"developer": "Zyra Core", "tier": "verified"},
        "global_trust": 0.82,
        "trust_mean": 0.82,
        "trust_uncertainty": 0.09,
        "capability_specific_trust": {
            "specification_analysis": {"mean": 0.82, "var": 0.09}
        },
        "successful_executions": 50,
        "failed_executions": 8,
        "verifier_agreement": 0.85,
        "schema_validity": 0.90,
        "tool_success": 0.92,
        "recent_performance": 0.83,
        "historical_performance": 0.82,
        "collaboration_history": {}
    },
    {
        "agent_id": "PriceVerificationAgent",
        "name": "Live Price & Deal Verification Agent",
        "description": "Cross-references product prices against discount history and checks budget thresholds.",
        "category": "shopping",
        "capabilities": ["price_verification", "data_analysis"],
        "tools": [{"name": "price_oracle", "type": "comparator"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0010,
        "cost_per_1k_tokens": 0.0010,
        "expected_latency": 130,
        "avg_latency_ms": 130,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["standard"],
        "provenance": {"developer": "DealGuard AI", "tier": "verified"},
        "global_trust": 0.93,
        "trust_mean": 0.93,
        "trust_uncertainty": 0.03,
        "capability_specific_trust": {
            "price_verification": {"mean": 0.95, "var": 0.02},
            "data_analysis": {"mean": 0.91, "var": 0.04}
        },
        "successful_executions": 180,
        "failed_executions": 2,
        "verifier_agreement": 0.97,
        "schema_validity": 0.99,
        "tool_success": 0.98,
        "recent_performance": 0.94,
        "historical_performance": 0.93,
        "collaboration_history": {}
    },
    {
        "agent_id": "ReviewAnalysisAgent",
        "name": "Customer Review & Sentiment Analyzer",
        "description": "Analyzes verified customer reviews, synthesizes pros/cons, and calculates sentiment scores.",
        "category": "shopping",
        "capabilities": ["review_analysis", "summarization"],
        "tools": [{"name": "sentiment_analyzer", "type": "nlp"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0014,
        "cost_per_1k_tokens": 0.0014,
        "expected_latency": 180,
        "avg_latency_ms": 180,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["standard"],
        "provenance": {"developer": "Sentiment AI", "tier": "verified"},
        "global_trust": 0.89,
        "trust_mean": 0.89,
        "trust_uncertainty": 0.05,
        "capability_specific_trust": {
            "review_analysis": {"mean": 0.91, "var": 0.04},
            "summarization": {"mean": 0.87, "var": 0.06}
        },
        "successful_executions": 140,
        "failed_executions": 6,
        "verifier_agreement": 0.90,
        "schema_validity": 0.95,
        "tool_success": 0.94,
        "recent_performance": 0.88,
        "historical_performance": 0.89,
        "collaboration_history": {}
    },
    {
        "agent_id": "RecommendationAgent",
        "name": "Multi-Criteria Decision Recommendation Agent",
        "description": "Synthesizes specs, price, and review evidence to generate rank-ordered recommendations.",
        "category": "shopping",
        "capabilities": ["recommendation", "report_synthesis"],
        "tools": [{"name": "decision_matrix_ranker", "type": "ranker"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0018,
        "cost_per_1k_tokens": 0.0018,
        "expected_latency": 240,
        "avg_latency_ms": 240,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["standard"],
        "provenance": {"developer": "Zyra Core", "tier": "verified"},
        "trust_mean": 0.92,
        "trust_uncertainty": 0.04,
        "global_trust": 0.92,
        "capability_specific_trust": {
            "recommendation": {"mean": 0.94, "var": 0.03},
            "report_synthesis": {"mean": 0.90, "var": 0.05}
        },
        "successful_executions": 160,
        "failed_executions": 4,
        "verifier_agreement": 0.95,
        "schema_validity": 0.97,
        "tool_success": 0.96,
        "recent_performance": 0.93,
        "historical_performance": 0.92,
        "collaboration_history": {}
    },
    {
        "agent_id": "ResearchAgent",
        "name": "Domain Research Analyst",
        "description": "Conducts deep multi-source academic and technical literature research.",
        "category": "research",
        "capabilities": ["report_synthesis", "summarization", "data_analysis"],
        "tools": [{"name": "academic_fetcher", "type": "web_search"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0020,
        "cost_per_1k_tokens": 0.0020,
        "expected_latency": 280,
        "avg_latency_ms": 280,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["standard"],
        "provenance": {"developer": "Research Labs", "tier": "verified"},
        "global_trust": 0.90,
        "trust_mean": 0.90,
        "trust_uncertainty": 0.05,
        "capability_specific_trust": {
            "report_synthesis": {"mean": 0.92, "var": 0.04},
            "summarization": {"mean": 0.88, "var": 0.06}
        },
        "successful_executions": 110,
        "failed_executions": 5,
        "verifier_agreement": 0.92,
        "schema_validity": 0.96,
        "tool_success": 0.95,
        "recent_performance": 0.90,
        "historical_performance": 0.90,
        "collaboration_history": {}
    },
    {
        "agent_id": "DataAnalysisAgent",
        "name": "Sandboxed Python & ML Execution Engine",
        "description": "Executes data analysis algorithms, numerical computations, and machine learning routines.",
        "category": "analysis",
        "capabilities": ["code_execution", "machine_learning", "data_analysis"],
        "tools": [{"name": "python_interpreter", "type": "code_sandbox"}],
        "model_backend": "ollama",
        "model_name": "qwen2.5:1.5b-instruct",
        "cost_per_execution": 0.0025,
        "cost_per_1k_tokens": 0.0025,
        "expected_latency": 350,
        "avg_latency_ms": 350,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["sandbox_exec"],
        "provenance": {"developer": "Zyra Core", "tier": "verified"},
        "global_trust": 0.88,
        "trust_mean": 0.88,
        "trust_uncertainty": 0.06,
        "capability_specific_trust": {
            "code_execution": {"mean": 0.91, "var": 0.03},
            "machine_learning": {"mean": 0.84, "var": 0.07}
        },
        "successful_executions": 130,
        "failed_executions": 7,
        "verifier_agreement": 0.91,
        "schema_validity": 0.94,
        "tool_success": 0.93,
        "recent_performance": 0.88,
        "historical_performance": 0.88,
        "collaboration_history": {}
    },
    {
        "agent_id": "VerificationAgent",
        "name": "Dual-Oracle Cross-Verifier",
        "description": "Independent verifier checking task execution outputs for schema validity, evidence, and correctness.",
        "category": "verification",
        "capabilities": ["verification", "agreement_scoring", "schema_validation"],
        "tools": [{"name": "cross_verifier", "type": "oracle"}],
        "model_backend": "gemini",
        "model_name": "gemini-1.5-flash",
        "cost_per_execution": 0.0018,
        "cost_per_1k_tokens": 0.0018,
        "expected_latency": 140,
        "avg_latency_ms": 140,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["verifier"],
        "provenance": {"developer": "Zyra Research", "tier": "verified"},
        "global_trust": 0.96,
        "trust_mean": 0.96,
        "trust_uncertainty": 0.02,
        "capability_specific_trust": {
            "verification": {"mean": 0.97, "var": 0.01},
            "agreement_scoring": {"mean": 0.95, "var": 0.02}
        },
        "successful_executions": 300,
        "failed_executions": 2,
        "verifier_agreement": 0.98,
        "schema_validity": 0.99,
        "tool_success": 0.99,
        "recent_performance": 0.97,
        "historical_performance": 0.96,
        "collaboration_history": {}
    },
    {
        "agent_id": "SafetyAgent",
        "name": "Guardrail & Policy Audit Agent",
        "description": "Scans inputs and outputs for prompt injection, policy risk, and data leak violations.",
        "category": "security",
        "capabilities": ["security_audit", "policy_verification"],
        "tools": [{"name": "guardrail_scanner", "type": "policy_checker"}],
        "model_backend": "gemini",
        "model_name": "gemini-1.5-flash",
        "cost_per_execution": 0.0016,
        "cost_per_1k_tokens": 0.0016,
        "expected_latency": 100,
        "avg_latency_ms": 100,
        "availability": "AVAILABLE",
        "availability_status": "AVAILABLE",
        "status": "ACTIVE",
        "permissions": ["admin_audit"],
        "provenance": {"developer": "CyberGuard Lab", "tier": "verified"},
        "global_trust": 0.97,
        "trust_mean": 0.97,
        "trust_uncertainty": 0.02,
        "capability_specific_trust": {
            "security_audit": {"mean": 0.98, "var": 0.01},
            "policy_verification": {"mean": 0.96, "var": 0.02}
        },
        "successful_executions": 280,
        "failed_executions": 1,
        "verifier_agreement": 0.99,
        "schema_validity": 0.99,
        "tool_success": 1.00,
        "recent_performance": 0.98,
        "historical_performance": 0.97,
        "collaboration_history": {}
    }
]

def seed_marketplace(db: Session):
    for agent_data in SEED_AGENTS:
        existing = db.query(AgentModel).filter(AgentModel.agent_id == agent_data["agent_id"]).first()
        if not existing:
            agent = AgentModel(**agent_data)
            db.add(agent)
    db.commit()

def list_agents(
    db: Session,
    capability: Optional[str] = None,
    tool: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = "ACTIVE",
    min_trust: Optional[float] = None
) -> List[AgentModel]:
    query = db.query(AgentModel)
    if status:
        query = query.filter(AgentModel.status == status)
    if min_trust is not None:
        query = query.filter(AgentModel.trust_mean >= min_trust)
    if category:
        query = query.filter(AgentModel.category == category)
    
    agents = query.all()
    if capability:
        agents = [a for a in agents if capability in a.capabilities]
    if tool:
        agents = [a for a in agents if any(t.get("name") == tool for t in (a.tools or []))]
    return agents

def get_agent_by_id(db: Session, agent_id: str) -> Optional[AgentModel]:
    return db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()

def create_agent(db: Session, agent_in: AgentCreate) -> AgentModel:
    agent_dict = agent_in.model_dump()
    if not agent_dict.get("agent_id"):
        agent_dict["agent_id"] = f"agent_{int(datetime.datetime.utcnow().timestamp())}"
    agent = AgentModel(**agent_dict)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

def update_agent(db: Session, agent_id: str, agent_in: AgentUpdate) -> Optional[AgentModel]:
    agent = get_agent_by_id(db, agent_id)
    if not agent:
        return None
    update_data = agent_in.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(agent, field, val)
    agent.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(agent)
    return agent

def delete_agent(db: Session, agent_id: str) -> bool:
    agent = get_agent_by_id(db, agent_id)
    if not agent:
        return False
    db.delete(agent)
    db.commit()
    return True
