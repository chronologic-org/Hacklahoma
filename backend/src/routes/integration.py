from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..graphs.flows.api_integration_flow import create_planning_flow, GraphState

router = APIRouter()

class IntegrationRequest(BaseModel):
    user_input: str

class IntegrationResponse(BaseModel):
    plan: dict
    supervisor_output: dict
    code_output: dict
    test_output: dict
    evaluation: dict
    supervisor_feedback: dict | None
    iteration_count: int

@router.post("/plan", response_model=IntegrationResponse)
async def create_integration_plan(request: IntegrationRequest):
    try:
        # Initialize the flow
        flow = await create_planning_flow()
        
        # Create initial state
        initial_state: GraphState = {
            "user_input": request.user_input,
            "plan": {},
            "supervisor_output": {},
            "code_output": {},
            "test_output": {},
            "evaluation": {},
            "supervisor_feedback": {},
            "iteration_count": 0
        }
        
        # Execute the flow
        final_state = await flow.ainvoke(initial_state)
        
        return IntegrationResponse(
            plan=final_state["plan"],
            supervisor_output=final_state["supervisor_output"],
            code_output=final_state["code_output"],
            test_output=final_state["test_output"],
            evaluation=final_state["evaluation"],
            supervisor_feedback=final_state.get("supervisor_feedback"),
            iteration_count=final_state["iteration_count"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 