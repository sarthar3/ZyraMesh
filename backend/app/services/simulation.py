import random
from typing import Dict, Any, Optional

class SimulationManager:
    """
    Module 27: Failure Simulation & Demonstration Mode.
    Manages active failure injection flags and deterministic triggers for demonstration mode.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimulationManager, cls).__new__(cls)
            cls._instance.active_failures = {}
            cls._instance.seed = 42
        return cls._instance

    def set_failure_injection(
        self,
        agent_id: Optional[str] = None,
        failure_type: str = "SCHEMA_FAILURE", # SCHEMA_FAILURE, TIMEOUT, UNCERTAINTY, VERIFIER_DISAGREEMENT, TOOL_FAILURE, UNAVAILABLE
        target_task_index: Optional[int] = None,
        enabled: bool = True
    ):
        if not enabled:
            self.active_failures.clear()
            return {"status": "DISABLED", "active_failures": {}}

        self.active_failures = {
            "agent_id": agent_id,
            "failure_type": failure_type,
            "target_task_index": target_task_index,
            "enabled": True
        }
        return {"status": "ACTIVE", "configuration": self.active_failures}

    def get_simulation_state(self) -> Dict[str, Any]:
        return {
            "enabled": len(self.active_failures) > 0,
            "configuration": self.active_failures,
            "seed": self.seed
        }

    def should_inject_failure(self, agent_id: str, task_index: int) -> Optional[str]:
        if not self.active_failures.get("enabled"):
            return None

        target_agent = self.active_failures.get("agent_id")
        target_idx = self.active_failures.get("target_task_index")

        # Match by agent_id or task index or fallback to first matching agent
        if target_agent and target_agent.lower() in agent_id.lower():
            return self.active_failures.get("failure_type", "SCHEMA_FAILURE")
        
        if target_idx is not None and target_idx == task_index:
            return self.active_failures.get("failure_type", "SCHEMA_FAILURE")

        # Special default for demonstration mode: SpecificationAgent-A fails
        if target_agent is None and target_idx is None and "specificationagent-a" in agent_id.lower():
            return self.active_failures.get("failure_type", "SCHEMA_FAILURE")

        return None

simulation_manager = SimulationManager()
