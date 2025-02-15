from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from ..graphs.flows.api_integration_flow import create_planning_flow, GraphState
from ..utils.logging import logger

router = APIRouter(prefix="/api/v1")

class IntegrationRequest(BaseModel):
    user_input: str
    config: Dict[str, Any] | None = None

class IntegrationResponse(BaseModel):
    plan: dict
    supervisor_output: dict
    code_output: dict
    test_output: dict
    evaluation: dict
    supervisor_feedback: dict | None
    iteration_count: int
    final_status: str

@router.post("/integration/plan", response_model=IntegrationResponse)
async def create_integration_plan(request: IntegrationRequest):
    """
    Create an integration plan and execute the API integration flow.
    
    Args:
        request: IntegrationRequest containing user input and optional configuration
    
    Returns:
        IntegrationResponse with the complete flow results
        
    Raises:
        HTTPException: If flow execution fails or validation errors occur
    """
    try:
        logger.info(f"Starting integration flow for request: {request.user_input}")
        
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
            "iteration_count": 0,
            "final_status": ""
        }
        
        # Execute the flow
        final_state = await flow.ainvoke(initial_state)
        
        logger.info(f"Flow completed with status: {final_state['final_status']}")
        
        return IntegrationResponse(
            plan=final_state["plan"],
            supervisor_output=final_state["supervisor_output"],
            code_output=final_state["code_output"],
            test_output=final_state["test_output"],
            evaluation=final_state["evaluation"],
            supervisor_feedback=final_state.get("supervisor_feedback"),
            iteration_count=final_state["iteration_count"],
            final_status=final_state["final_status"]
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Flow execution error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Flow execution failed: {str(e)}"
        ) 