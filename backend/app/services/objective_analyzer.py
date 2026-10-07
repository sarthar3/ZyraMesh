import json
import re
import networkx as nx
from typing import List, Dict, Any, Tuple, Optional
from app.adapters.provider_factory import get_llm_adapter

class ObjectiveAnalyzer:
    """
    Module 4: User Objective Analyzer.
    Parses natural language user prompts (e.g. 'Find the best laptop under ₹70,000 for AI development')
    into structured objective constraints, required capabilities, tools, and TDG subtasks.
    """
    def __init__(self, provider_name: str = "mock"):
        self.adapter = get_llm_adapter(provider_name)

    def extract_deterministic_constraints(self, raw_objective: str) -> Dict[str, Any]:
        """Rule-based extraction of budget, currency, domain, and key requirements."""
        constraints = {}
        
        # Regex for budget: e.g. "under ₹70,000", "below 70000", "under $1000"
        budget_match = re.search(r'(?:under|below|<|<=|\bmax\b)?\s*[₹$]?\s*([\d,]+)\s*(?:inr|rs|rupees|\$)?', raw_objective, re.IGNORECASE)
        if budget_match:
            try:
                num_str = budget_match.group(1).replace(",", "")
                val = float(num_str)
                if val > 100: # Sanity filter
                    constraints["max_budget"] = val
            except Exception:
                pass

        obj_lower = raw_objective.lower()
        if "laptop" in obj_lower or "phone" in obj_lower or "shopping" in obj_lower or "product" in obj_lower or "buy" in obj_lower:
            constraints["category"] = "shopping"
        elif "research" in obj_lower or "paper" in obj_lower:
            constraints["category"] = "research"
        elif "code" in obj_lower or "python" in obj_lower or "script" in obj_lower:
            constraints["category"] = "coding"
        else:
            constraints["category"] = "general"

        return constraints

    async def parse_and_decompose(
        self,
        raw_objective: str,
        no_tdg: bool = False
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
        
        extracted_constraints = self.extract_deterministic_constraints(raw_objective)

        if no_tdg:
            # Ablation mode: single monolithic subtask
            single_subtask = {
                "subtask_index": 1,
                "description": raw_objective,
                "required_capabilities": ["general_intelligence"],
                "required_tools": [],
                "sensitivity": 0.3,
                "criticality": 1.0,
                "propagation_risk": 0.5,
                "verification_required": "AUTO",
                "dependencies": []
            }
            subtasks = [single_subtask]
        elif extracted_constraints.get("category") == "shopping":
            # Domain-specific shopping workflow pipeline
            subtasks = [
                {
                    "subtask_index": 1,
                    "description": f"Identify criteria & search products for: '{raw_objective}'",
                    "required_capabilities": ["product_search", "data_retrieval"],
                    "required_tools": ["fast_catalog_search", "deep_db_query"],
                    "sensitivity": 0.1,
                    "criticality": 0.8,
                    "propagation_risk": 0.7,
                    "verification_required": "AUTO",
                    "dependencies": []
                },
                {
                    "subtask_index": 2,
                    "description": "Extract & validate hardware specifications (CPU, GPU, RAM, VRAM)",
                    "required_capabilities": ["specification_analysis"],
                    "required_tools": ["spec_parser"],
                    "sensitivity": 0.2,
                    "criticality": 0.9,
                    "propagation_risk": 0.8,
                    "verification_required": "AUTO",
                    "dependencies": [1]
                },
                {
                    "subtask_index": 3,
                    "description": f"Verify price and budget constraints (Max: ₹{extracted_constraints.get('max_budget', 70000)})",
                    "required_capabilities": ["price_verification"],
                    "required_tools": ["price_oracle"],
                    "sensitivity": 0.2,
                    "criticality": 0.85,
                    "propagation_risk": 0.75,
                    "verification_required": "AUTO",
                    "dependencies": [2]
                },
                {
                    "subtask_index": 4,
                    "description": "Analyze verified customer reviews & sentiment scores",
                    "required_capabilities": ["review_analysis", "summarization"],
                    "required_tools": ["sentiment_analyzer"],
                    "sensitivity": 0.1,
                    "criticality": 0.7,
                    "propagation_risk": 0.5,
                    "verification_required": "AUTO",
                    "dependencies": [2]
                },
                {
                    "subtask_index": 5,
                    "description": "Synthesize multi-criteria candidate rankings and final recommendation",
                    "required_capabilities": ["recommendation", "report_synthesis"],
                    "required_tools": ["decision_matrix_ranker"],
                    "sensitivity": 0.2,
                    "criticality": 0.95,
                    "propagation_risk": 0.9,
                    "verification_required": "ALWAYS",
                    "dependencies": [3, 4]
                }
            ]
        else:
            # General multi-step workflow pipeline
            subtasks = [
                {
                    "subtask_index": 1,
                    "description": f"Analyze requirements & validate input for: '{raw_objective}'",
                    "required_capabilities": ["data_analysis", "schema_validation"],
                    "required_tools": ["schema_checker"],
                    "sensitivity": 0.2,
                    "criticality": 0.7,
                    "propagation_risk": 0.6,
                    "verification_required": "AUTO",
                    "dependencies": []
                },
                {
                    "subtask_index": 2,
                    "description": f"Execute core domain computation / retrieval for: '{raw_objective}'",
                    "required_capabilities": ["code_execution", "data_retrieval"],
                    "required_tools": ["python_interpreter"],
                    "sensitivity": 0.4,
                    "criticality": 0.9,
                    "propagation_risk": 0.8,
                    "verification_required": "AUTO",
                    "dependencies": [1]
                },
                {
                    "subtask_index": 3,
                    "description": f"Audit safety and synthesize report for: '{raw_objective}'",
                    "required_capabilities": ["security_audit", "report_synthesis"],
                    "required_tools": ["guardrail_scanner"],
                    "sensitivity": 0.8,
                    "criticality": 0.95,
                    "propagation_risk": 0.9,
                    "verification_required": "ALWAYS",
                    "dependencies": [2]
                }
            ]

        # Build NetworkX TDG
        tdg = nx.DiGraph()
        for s in subtasks:
            node_id = f"task_{s['subtask_index']}"
            s["task_id"] = node_id
            tdg.add_node(node_id, **s)
            for parent_idx in s.get("dependencies", []):
                parent_id = f"task_{parent_idx}"
                tdg.add_edge(parent_id, node_id)

        tdg_json = {
            "nodes": [{"id": n, **tdg.nodes[n]} for n in tdg.nodes()],
            "edges": [{"source": u, "target": v} for u, v in tdg.edges()]
        }

        objective_analysis = {
            "raw_objective": raw_objective,
            "category": extracted_constraints.get("category", "general"),
            "constraints": extracted_constraints,
            "quality_requirements": "HIGH_PRECISION",
            "risk_level": "MEDIUM",
            "verification_requirement": "ALWAYS",
            "total_subtasks": len(subtasks)
        }

        return objective_analysis, subtasks, tdg_json

    async def analyze_objective(self, raw_objective: str, no_tdg: bool = False):
        _, subtasks, tdg_json = await self.parse_and_decompose(raw_objective, no_tdg=no_tdg)
        return subtasks, tdg_json
