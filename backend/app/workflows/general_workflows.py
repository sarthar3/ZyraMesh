from typing import Dict, Any, List

class GeneralDomainWorkflows:
    """
    Module 18: General Domain Workflows.
    Demonstrates domain-independence of the ZyraMesh engine across non-shopping categories:
      1. Research -> Report
      2. Data Analysis & Python Execution
      3. Coding & Testing Task
    """
    @staticmethod
    def get_template(category: str, objective: str) -> List[Dict[str, Any]]:
        cat = category.lower()
        if cat == "research":
            return [
                {
                    "subtask_index": 1,
                    "description": f"Gather literature & primary sources for: '{objective}'",
                    "required_capabilities": ["report_synthesis", "data_analysis"],
                    "required_tools": ["academic_fetcher"],
                    "sensitivity": 0.1,
                    "criticality": 0.8,
                    "propagation_risk": 0.6,
                    "verification_required": "AUTO",
                    "dependencies": []
                },
                {
                    "subtask_index": 2,
                    "description": "Synthesize executive literature summary & citation trace",
                    "required_capabilities": ["summarization", "report_synthesis"],
                    "required_tools": ["markdown_formatter"],
                    "sensitivity": 0.1,
                    "criticality": 0.95,
                    "propagation_risk": 0.8,
                    "verification_required": "ALWAYS",
                    "dependencies": [1]
                }
            ]
        elif cat in ["coding", "analysis"]:
            return [
                {
                    "subtask_index": 1,
                    "description": f"Analyze technical code requirements for: '{objective}'",
                    "required_capabilities": ["code_execution", "schema_validation"],
                    "required_tools": ["python_interpreter"],
                    "sensitivity": 0.2,
                    "criticality": 0.8,
                    "propagation_risk": 0.7,
                    "verification_required": "AUTO",
                    "dependencies": []
                },
                {
                    "subtask_index": 2,
                    "description": "Execute sandboxed Python script and validate test output",
                    "required_capabilities": ["code_execution", "machine_learning"],
                    "required_tools": ["python_interpreter"],
                    "sensitivity": 0.3,
                    "criticality": 0.95,
                    "propagation_risk": 0.9,
                    "verification_required": "ALWAYS",
                    "dependencies": [1]
                }
            ]
        else:
            return [
                {
                    "subtask_index": 1,
                    "description": f"Process general objective step: '{objective}'",
                    "required_capabilities": ["general_intelligence"],
                    "required_tools": [],
                    "sensitivity": 0.2,
                    "criticality": 0.8,
                    "propagation_risk": 0.5,
                    "verification_required": "AUTO",
                    "dependencies": []
                }
            ]
