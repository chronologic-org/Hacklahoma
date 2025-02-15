from langgraph.graph import Graph, END
from ..nodes.planner_node import PlannerNode
from ..nodes.supervisor_node import SupervisorNode
from ..nodes.coder_node import CoderNode
from ..nodes.tester_node import TesterNode
from ..nodes.evaluator_node import EvaluatorNode
from typing import Dict, Any, TypedDict, Annotated
from ..utils.logging import logger

class GraphState(TypedDict):
    user_input: str
    plan: Dict[str, Any]
    supervisor_output: Dict[str, Any]
    code_output: Dict[str, Any]
    test_output: Dict[str, Any]
    evaluation: Dict[str, Any]
    supervisor_feedback: Dict[str, Any]
    iteration_count: int
    final_status: str
    error: str

async def create_planning_flow() -> Graph:
    # Initialize nodes
    planner = PlannerNode()
    supervisor = SupervisorNode()
    coder = CoderNode()
    tester = TesterNode()
    evaluator = EvaluatorNode()
    
    # Define the graph
    workflow = Graph()

    # Add nodes
    @workflow.node("planner")
    async def planning_node(state: GraphState) -> GraphState:
        try:
            plan = await planner.process(state["user_input"])
            state["plan"] = plan.dict()
            return state
        except Exception as e:
            logger.error(f"Planning node error: {str(e)}")
            state["error"] = str(e)
            return state

    @workflow.node("supervisor")
    async def supervisor_node(state: GraphState) -> GraphState:
        if "evaluation" not in state:
            # Initial planning
            supervisor_output = await supervisor.process(state["plan"])
            state["supervisor_output"] = supervisor_output.dict()
        else:
            # Review evaluation
            feedback = await supervisor.review_evaluation(
                state["evaluation"],
                state["plan"]
            )
            state["supervisor_feedback"] = feedback.dict()
        return state

    @workflow.node("coder")
    async def coder_node(state: GraphState) -> GraphState:
        try:
            code_output = await coder.process(state["supervisor_output"]["coding_task"])
            state["code_output"] = code_output.dict()
            return state
        except Exception as e:
            logger.error(f"Coder node error: {str(e)}")
            state["error"] = str(e)
            return state

    @workflow.node("tester")
    async def tester_node(state: GraphState) -> GraphState:
        try:
            test_output = await tester.process(state["supervisor_output"]["testing_task"])
            state["test_output"] = test_output.dict()
            return state
        except Exception as e:
            logger.error(f"Tester node error: {str(e)}")
            state["error"] = str(e)
            return state

    @workflow.node("evaluator")
    async def evaluator_node(state: GraphState) -> GraphState:
        try:
            evaluation = await evaluator.process(
                state["code_output"],
                state["test_output"],
                state["plan"]
            )
            state["evaluation"] = evaluation.dict()
            return state
        except Exception as e:
            logger.error(f"Evaluator node error: {str(e)}")
            state["error"] = str(e)
            return state

    # Define conditional routing
    @workflow.node("check_completion")
    async def check_completion(state: GraphState) -> Annotated[str, {"supervisor", END}]:
        state["iteration_count"] = state.get("iteration_count", 0) + 1
        
        # Add more detailed state validation
        if not all(key in state for key in ["evaluation", "code_output", "test_output"]):
            raise ValueError("Missing required state components")
        
        if state["iteration_count"] > 3:  # Prevent infinite loops
            state["final_status"] = "max_iterations_reached"
            return END
            
        if state["evaluation"].get("is_acceptable", False):
            state["final_status"] = "success"
            return END
        
        state["final_status"] = "needs_revision"
        return "supervisor"

    # Define the edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "supervisor")
    workflow.add_edge("supervisor", "coder")
    workflow.add_edge("supervisor", "tester")
    workflow.add_edge("coder", "evaluator")
    workflow.add_edge("tester", "evaluator")
    workflow.add_edge("evaluator", "check_completion")
    
    return workflow.compile() 