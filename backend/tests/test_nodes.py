import pytest
from unittest.mock import AsyncMock, patch
from ..src.graphs.nodes.planner_node import PlannerNode, PlannerOutput
from ..src.graphs.nodes.supervisor_node import SupervisorNode, SupervisorOutput, SupervisorFeedback
from ..src.graphs.nodes.coder_node import CoderNode, CodeOutput
from ..src.graphs.nodes.tester_node import TesterNode, TestOutput
from ..src.graphs.nodes.evaluator_node import EvaluatorNode, EvaluationOutput

@pytest.fixture
def mock_openai_response():
    return AsyncMock(content="""
    {
        "apis": {
            "api1": {"name": "Weather API", "auth": "api_key"},
            "api2": {"name": "SMS API", "auth": "oauth2"}
        },
        "integration_plan": {
            "steps": ["Initialize clients", "Set up webhooks"]
        },
        "requirements": ["python>=3.8", "requests"],
        "expected_output": {"status": "success"},
        "validation_rules": ["Check API responses"]
    }
    """)

@pytest.mark.asyncio
async def test_planner_node(mock_openai_response):
    with patch('langchain.chat_models.ChatOpenAI.ainvoke', return_value=mock_openai_response):
        planner = PlannerNode()
        result = await planner.process("Connect Weather API with SMS API")
        
        assert isinstance(result, PlannerOutput)
        assert "Weather API" in result.apis["api1"]["name"]
        assert len(result.requirements) > 0

@pytest.mark.asyncio
async def test_supervisor_node(mock_openai_response):
    with patch('langchain.chat_models.ChatOpenAI.ainvoke', return_value=mock_openai_response):
        supervisor = SupervisorNode()
        plan = {
            "apis": {"api1": {"name": "Weather API"}},
            "integration_plan": {"steps": ["Step 1"]}
        }
        
        result = await supervisor.process(plan)
        assert isinstance(result, SupervisorOutput)
        assert "task" in result.coding_task
        
        # Test review functionality
        evaluation = {
            "code_evaluation": {"quality": "good"},
            "is_acceptable": True
        }
        review_result = await supervisor.review_evaluation(evaluation, plan)
        assert isinstance(review_result, SupervisorFeedback)
        assert isinstance(review_result.requires_changes, bool)

@pytest.mark.asyncio
async def test_evaluator_node(mock_openai_response):
    with patch('langchain.chat_models.ChatOpenAI.ainvoke', return_value=mock_openai_response):
        evaluator = EvaluatorNode()
        code_output = {"implementation": {"main.py": "code here"}}
        test_output = {"test_cases": {"test1": "passed"}}
        plan = {"requirements": ["req1"]}
        
        result = await evaluator.process(code_output, test_output, plan)
        assert isinstance(result, EvaluationOutput)
        assert isinstance(result.is_acceptable, bool) 