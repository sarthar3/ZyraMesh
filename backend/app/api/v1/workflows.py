import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.database import get_db
from app.models.task import WorkflowModel, TaskModel
from app.models.agent import AgentModel
from app.schemas.workflow import WorkflowSubmitRequest, WorkflowResponse, SubtaskSchema
from app.services.objective_analyzer import ObjectiveAnalyzer
from app.services.actg_builder import ACTGBuilder
from app.services.team_composer import TeamComposer
from app.services.marketplace import list_agents
from app.services.orchestrator import WorkflowOrchestrator

router = APIRouter(prefix="/workflows", tags=["Workflows & Dynamic Team Formation"])

from app.services.audit import AuditService

@router.post("/submit", response_model=WorkflowResponse)
async def submit_workflow_objective(
    req: WorkflowSubmitRequest,
    db: Session = Depends(get_db)
):
    workflow_id = f"wf_{uuid.uuid4().hex[:12]}"
    
    # 1. Analyze Objective & Build TDG
    analyzer = ObjectiveAnalyzer()
    no_tdg = req.ablation_config.get("no_tdg", False)
    subtasks, tdg_structure = await analyzer.analyze_objective(req.raw_user_objective, no_tdg=no_tdg)

    # Log TDG creation event
    AuditService.log_event(
        db,
        event_type="TDG_BUILT",
        actor="ObjectiveAnalyzer",
        payload={"raw_objective": req.raw_user_objective, "subtask_count": len(subtasks), "tdg": tdg_structure},
        workflow_id=workflow_id
    )

    # 2. Get Available Marketplace Agents
    agents = list_agents(db)
    if not agents:
        raise HTTPException(status_code=400, detail="No active agents in marketplace")

    # 3. Constrained Team Composer
    composer = TeamComposer(strategy=req.execution_strategy, ablation_config=req.ablation_config)
    assigned_subtasks, meta = composer.compose_team(
        subtasks=subtasks,
        agents=agents,
        max_budget=req.max_budget,
        max_latency_ms=req.max_latency_ms
    )

    # Log Team Composition event
    AuditService.log_event(
        db,
        event_type="TEAM_FORMED",
        actor="TeamComposer",
        payload={"team_metadata": meta, "assignments": [s.get("assigned_agent_id") for s in assigned_subtasks]},
        workflow_id=workflow_id
    )

    # Save Workflow to DB
    wf = WorkflowModel(
        workflow_id=workflow_id,
        raw_user_objective=req.raw_user_objective,
        status="TEAM_FORMED",
        execution_strategy=req.execution_strategy,
        ablation_config=req.ablation_config,
        max_budget=req.max_budget,
        max_latency_ms=req.max_latency_ms,
        required_security_tier=req.required_security_tier,
        tdg_structure=tdg_structure,
        created_at=datetime.datetime.utcnow()
    )
    db.add(wf)

    task_models = []
    for s in assigned_subtasks:
        tm = TaskModel(
            task_id=f"t_{uuid.uuid4().hex[:10]}",
            workflow_id=workflow_id,
            subtask_index=s["subtask_index"],
            description=s["description"],
            required_capabilities=s["required_capabilities"],
            required_tools=s.get("required_tools", []),
            sensitivity_score=s.get("sensitivity_score", 0.0),
            criticality_score=s.get("criticality_score", 0.5),
            propagation_risk=s.get("propagation_risk", 0.5),
            verification_requirement=s.get("verification_requirement", "AUTO"),
            dependencies=[f"t_{d}" for d in s.get("dependencies", [])],
            assigned_agent_id=s.get("assigned_agent_id"),
            status="PENDING"
        )
        db.add(tm)
        task_models.append(tm)

    db.commit()
    db.refresh(wf)

    res_tasks = [
        SubtaskSchema(
            task_id=t.task_id,
            subtask_index=t.subtask_index,
            description=t.description,
            required_capabilities=t.required_capabilities,
            required_tools=t.required_tools,
            sensitivity_score=t.sensitivity_score,
            criticality_score=t.criticality_score,
            propagation_risk=t.propagation_risk,
            verification_requirement=t.verification_requirement,
            dependencies=t.dependencies,
            assigned_agent_id=t.assigned_agent_id,
            assigned_agent_name=next((a.name for a in agents if a.agent_id == t.assigned_agent_id), None),
            status=t.status
        )
        for t in task_models
    ]

    return WorkflowResponse(
        workflow_id=wf.workflow_id,
        raw_user_objective=wf.raw_user_objective,
        status=wf.status,
        execution_strategy=wf.execution_strategy,
        ablation_config=wf.ablation_config,
        tdg_structure=wf.tdg_structure,
        tasks=res_tasks,
        created_at=wf.created_at,
        completed_at=wf.completed_at
    )

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow_by_id(workflow_id: str, db: Session = Depends(get_db)):
    wf = db.query(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id).first()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    tasks = db.query(TaskModel).filter(TaskModel.workflow_id == workflow_id).order_by(TaskModel.subtask_index).all()
    agents = db.query(AgentModel).all()

    res_tasks = [
        SubtaskSchema(
            task_id=t.task_id,
            subtask_index=t.subtask_index,
            description=t.description,
            required_capabilities=t.required_capabilities,
            required_tools=t.required_tools,
            sensitivity_score=t.sensitivity_score,
            criticality_score=t.criticality_score,
            propagation_risk=t.propagation_risk,
            verification_requirement=t.verification_requirement,
            dependencies=t.dependencies,
            assigned_agent_id=t.assigned_agent_id,
            assigned_agent_name=next((a.name for a in agents if a.agent_id == t.assigned_agent_id), None),
            status=t.status
        )
        for t in tasks
    ]

    return WorkflowResponse(
        workflow_id=wf.workflow_id,
        raw_user_objective=wf.raw_user_objective,
        status=wf.status,
        execution_strategy=wf.execution_strategy,
        ablation_config=wf.ablation_config,
        tdg_structure=wf.tdg_structure,
        tasks=res_tasks,
        created_at=wf.created_at,
        completed_at=wf.completed_at
    )

@router.get("/{workflow_id}/actg")
def get_workflow_actg(workflow_id: str, db: Session = Depends(get_db)):
    agents = list_agents(db)
    _, actg_json = ACTGBuilder.build_actg(agents)
    return actg_json

@router.get("/{workflow_id}/audit")
def get_workflow_audit_log(workflow_id: str, db: Session = Depends(get_db)):
    audit_trace = AuditService.get_workflow_audit_trace(db, workflow_id)
    if "error" in audit_trace:
        raise HTTPException(status_code=404, detail=audit_trace["error"])
    return audit_trace

@router.post("/{workflow_id}/execute")
async def execute_workflow_endpoint(
    workflow_id: str,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    orchestrator = WorkflowOrchestrator(db)
    bg_tasks.add_task(orchestrator.execute_workflow, workflow_id)
    return {"status": "EXECUTING_IN_BACKGROUND", "workflow_id": workflow_id}

