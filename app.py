import os
import sys
import re
from datetime import datetime
from typing import Dict, List, Annotated
from langgraph.graph import StateGraph, END
from groq import Groq
from pydantic import BaseModel, Field
import json

def extract_code_blocks(text):
    """
    Extracts code blocks enclosed in triple backticks from the given text.
    
    :param text: str, input text containing code blocks
    :return: list of extracted code blocks
    """
    pattern = r'```(?:\w+\s)?(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def log(message):
    """Force immediate output of log messages"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {message}", flush=True)
    sys.stdout.flush()

log("=== SCRIPT STARTING ===")

# Initialize Groq clients with verified API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    log("ERROR: GROQ_API_KEY environment variable is not set")
    sys.exit(1)

try:
    # Initialize different Groq clients for each agent
    plan_client = Groq(api_key=GROQ_API_KEY)
    supervisor_client = Groq(api_key=GROQ_API_KEY)
    coder_client = Groq(api_key=GROQ_API_KEY)
    tester_client = Groq(api_key=GROQ_API_KEY)
    evaluator_client = Groq(api_key=GROQ_API_KEY)
    log("All Groq clients initialized successfully")
except Exception as e:
    log(f"ERROR initializing Groq clients: {str(e)}")
    sys.exit(1)

# State Management
class AgentState(BaseModel):
    user_input: str
    plan: str = ""
    code: str = ""
    tests: str = ""
    evaluation: str = ""
    iteration: int = 0
    max_iterations: int = 5
    next_step: str = "planner"
    last_agent: str = ""

    def copy(self):
        return AgentState(
            user_input=self.user_input,
            plan=self.plan,
            code=self.code,
            tests=self.tests,
            evaluation=self.evaluation,
            iteration=self.iteration,
            max_iterations=self.max_iterations,
            next_step=self.next_step,
            last_agent=self.last_agent
        )

# Agent Definitions
def plan_agent(state: AgentState) -> AgentState:
    """Creates a detailed plan for API integration based on user input."""
    log("\n=== PLANNER AGENT ===")
    log(f"Planning for request: {state.user_input}")
    
    new_state = state.copy()  # Create a copy of the state
    
    prompt = f"""
    Create a detailed technical plan for integrating APIs based on this user request:
    {new_state.user_input}
    
    Include:
    1. Required API endpoints
    2. Data transformation steps
    3. Error handling requirements
    4. Expected input/output formats
    """
    
    response = plan_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
        temperature=0.7,
    )
    
    new_state.plan = response.choices[0].message.content
    new_state.next_step = "supervisor"
    new_state.last_agent = "planner"
    
    log("Plan created:")
    log(new_state.plan[:200] + "..." if len(new_state.plan) > 200 else new_state.plan)
    return new_state

def supervisor_agent(state: AgentState) -> AgentState:
    """Determines next steps based on the plan and current state."""
    log("\n=== SUPERVISOR AGENT ===")
    log(f"Current iteration: {state.iteration}")
    log(f"Code exists: {'Yes' if state.code else 'No'}")
    log(f"Tests exist: {'Yes' if state.tests else 'No'}")
    
    prompt = f"""
    Based on the current state:
    - Code exists: {"Yes" if state.code else "No"}
    - Tests exist: {"Yes" if state.tests else "No"}
    - Current iteration: {state.iteration}
    
    Analyze the situation and choose ONE of these next steps:
    1. "generate code" - if we need to create or modify code
    2. "generate tests" - if we have code but need tests
    3. "evaluate" - if we have both code and tests to evaluate
    4. "end" - only if everything is complete and validated

    Respond with ONLY ONE of these exact phrases: "generate code", "generate tests", "evaluate", or "end". After selecting do not add any other text.
    """
    
    response = supervisor_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
        temperature=0.3,
    )
    
    decision = response.choices[0].message.content.lower().strip()
    log(f"Supervisor raw decision: {decision}")
    
    # Parse decision
    if state.iteration >= state.max_iterations:
        state.next_step = "end"
    elif not state.code or "generate code" in decision:
        state.next_step = "coder"
    elif not state.tests or "generate test" in decision:
        state.next_step = "tester"
    elif "evaluate" in decision:
        state.next_step = "evaluator"
    elif "end" in decision and state.code and state.tests and state.evaluation:
        state.next_step = "end"
    else:
        # Default to generating code if we can't determine the next step
        state.next_step = "coder"
    
    state.last_agent = "supervisor"
    log(f"Next step decided: {state.next_step}")
    return state

def coder_agent(state: AgentState) -> AgentState:
    """Generates code based on the technical plan."""
    log("\n=== CODER AGENT ===")
    
    prompt = f"""
    Create Python code based on this technical plan:
    {state.plan}
    
    Previous code (if any):
    {state.code}
    
    Previous evaluation (if any):
    {state.evaluation}
    """
    
    response = coder_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="deepseek-r1-distill-llama-70b",
        temperature=0.2,
    )
    
    tmp = extract_code_blocks(response.choices[0].message.content)
    state.code = tmp[0]
    state.next_step = "supervisor"
    state.last_agent = "coder"
    
    log("Generated code:")
    log(state.code[:200] + "..." if len(state.code) > 200 else state.code)
    return state

def tester_agent(state: AgentState) -> AgentState:
    """Generates unit tests for the code."""
    log("\n=== TESTER AGENT ===")
    
    prompt = f"""
    You are a unit test creator. Create unit tests for this code:
    {state.code}
    
    Based on these requirements:
    {state.plan}
    
    Your output should be a list of unit tests.
    """
    
    response = tester_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
        temperature=0.2,
    )
    
    state.tests = response.choices[0].message.content
    state.next_step = "supervisor"
    state.last_agent = "tester"
    
    log("Generated tests:")
    log(state.tests[:200] + "..." if len(state.tests) > 200 else state.tests)
    return state

def evaluator_agent(state: AgentState) -> AgentState:
    """Evaluates code and tests, providing feedback."""
    log("\n=== EVALUATOR AGENT ===")
    
    prompt = f"""
    Evaluate this code:
    {state.code}
    
    And these tests:
    {state.tests}
    
    Against these requirements:
    {state.plan}
    
    Provide specific feedback on:
    1. Code functionality
    2. Test coverage
    3. Error handling
    4. API integration correctness
    """
    
    response = evaluator_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
        temperature=0.3,
    )
    
    state.evaluation = response.choices[0].message.content
    state.iteration += 1
    state.next_step = "supervisor"
    state.last_agent = "evaluator"
    
    log("Evaluation results:")
    log(state.evaluation[:200] + "..." if len(state.evaluation) > 200 else state.evaluation)
    return state

# Graph Configuration
def build_graph():
    log("\n=== BUILDING WORKFLOW GRAPH ===")
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("planner", plan_agent)
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("coder", coder_agent)
    workflow.add_node("tester", tester_agent)
    workflow.add_node("evaluator", evaluator_agent)
    log("All nodes added")
    
    # Set entry point
    workflow.set_entry_point("planner")
    log("Entry point set to planner")
    
    # Add edges
    workflow.add_edge("planner", "supervisor")
    workflow.add_edge("coder", "supervisor")
    workflow.add_edge("tester", "supervisor")
    workflow.add_edge("evaluator", "supervisor")
    
    # Add conditional edges from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x.next_step,
        {
            "coder": "coder",
            "tester": "tester",
            "evaluator": "evaluator",
            "end": END
        }
    )
    log("All edges added")
    
    compiled = workflow.compile()
    log("Graph compiled successfully")
    return compiled

def run_api_integration(user_input: str) -> Dict:
    """
    Main function to run the API integration workflow.
    """
    log("\n=== STARTING API INTEGRATION WORKFLOW ===")
    log(f"User request: {user_input}")
    
    try:
        workflow = build_graph()
        log("Workflow graph built successfully")
        
        initial_state = AgentState(
            user_input=user_input,
            max_iterations=5
        )
        log("Initial state created")
        
        # Run the workflow
        log("Invoking workflow...")
        result = workflow.invoke(initial_state)
        log("Workflow execution completed")
        
        # Process results
        log("\n=== PROCESSING RESULTS ===")
        if isinstance(result, dict):
            log(f"Result keys: {list(result.keys())}")
            
            # Get the final state
            states = []
            for node_name, output in result.items():
                log(f"Processing output from {node_name}")
                if isinstance(output, AgentState):
                    states.append(output)
                    log(f"Found state with iteration {output.iteration}")
            
            # Sort states by iteration number
            states.sort(key=lambda x: x.iteration)
            
            if states:
                final_state = states[-1]  # Get the state with highest iteration
                output = {
                    "code": final_state.code,  
                    "tests": final_state.tests,
                    "evaluation": final_state.evaluation,
                    "iterations": final_state.iteration,
                    "last_agent": final_state.last_agent
                }
                log("\n=== FINAL OUTPUT ===")
                log(f"Last agent: {output['last_agent']}")
                log(f"Iterations: {output['iterations']}")
                print(json.dumps(output, indent=2))
                return output
            else:
                error_msg = "No valid states found in workflow output"
                log(f"ERROR: {error_msg}")
                return {"error": error_msg, "raw_output": str(result)}
        else:
            error_msg = f"Unexpected result type: {type(result)}"
            log(f"ERROR: {error_msg}")
            return {"error": error_msg, "raw_output": str(result)}
            
    except Exception as e:
        error_msg = f"Workflow error: {str(e)}"
        log(f"ERROR: {error_msg}")
        return {"error": error_msg}

if __name__ == "__main__":
    user_request = "Make a calculator app that can add, subtract, multiply, and divide."
    result = run_api_integration(user_request)