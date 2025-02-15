import pytest
from ..src.graphs.flows.api_integration_flow import create_planning_flow, GraphState
from unittest.mock import patch, AsyncMock

@pytest.fixture
def mock_responses():
    return {
        "planner": AsyncMock(return_value={
            "apis": {"api1": {"name": "Weather API"}},
            "integration_plan": {"steps": ["Step 1"]},
            "requirements": ["req1"],
            "expected_output": {"status": "success"},
            "validation_rules": ["rule1"]
        }),
        "supervisor": AsyncMock(return_value={
            "coding_task": {"task": "Implement API client"},
            "testing_task": {"task": "Test API integration"},
            "acceptance_criteria": ["criterion1"]
        }),
        "evaluator": AsyncMock(return_value={
            "code_evaluation": {"quality": "good"},
            "issues_found": [],
            "test_results": {"passed": True},
            "recommendations": ["rec1"],
            "is_acceptable": True
        })
    }

@pytest.mark.asyncio
async def test_flow_execution(mock_responses):
    with patch('src.graphs.nodes.planner_node.PlannerNode.process', mock_responses["planner"]), \
         patch('src.graphs.nodes.supervisor_node.SupervisorNode.process', mock_responses["supervisor"]), \
         patch('src.graphs.nodes.evaluator_node.EvaluatorNode.process', mock_responses["evaluator"]):
        
        flow = await create_planning_flow()
        
        initial_state: GraphState = {
            "user_input": "Connect Weather API with SMS API",
            "plan": {},
            "supervisor_output": {},
            "code_output": {},
            "test_output": {},
            "evaluation": {},
            "supervisor_feedback": {},
            "iteration_count": 0
        }
        
        final_state = await flow.ainvoke(initial_state)
        
        assert "plan" in final_state
        assert "supervisor_output" in final_state
        assert "evaluation" in final_state
        assert final_state["iteration_count"] >= 0 