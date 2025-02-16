import os
import sys
import re
import subprocess
import uvicorn
from fastapi import FastAPI , File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, List, Annotated, Any
from langgraph.graph import StateGraph, END
from groq import Groq
from pydantic import BaseModel, Field
import json
from io import BytesIO

def extract_code_blocks(text):
    """
    Extracts code blocks enclosed in triple backticks from the given text.
    
    :param text: str, input text containing code blocks
    :return: list of extracted code blocks
    """
    pattern = r'```(?:\w+\s)?(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def run_unit_tests(test_filename):
    test_results = []
    try:
        test_result = subprocess.run(['python', '-m', 'pytest', test_filename], capture_output=True, text=True,timeout=30)
        test_success = test_result.returncode == 0
        test_results.append({
            'success': test_success,
            'output': test_result.stdout,
            'error': test_result.stderr
        })
        return test_results
    except Exception as e:
        test_results.append({
            'success': False,
            'error': str(e)
        })
        return f"Error running tests: {str(e)}"

def run_code(code_filename):
    """Run the unit tests"""
    execution_results = []
    try:
        result = subprocess.run(['python', code_filename], capture_output=True, text=True,timeout=30)
        execution_success = result.returncode == 0
        execution_results.append({
            'success': execution_success,
            'output': result.stdout,
            'error': result.stderr
        })
        return execution_results
    except Exception as e:
        return f"Error running tests: {str(e)}"


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
    max_iterations: int = 3
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
    1. Data transformation steps
    2. Error handling requirements
    3. Expected input/output formats
    """
    
    response = plan_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
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
    1. "generate code" - if code does not exist or is not working
    2. "generate tests" - if we have code but need tests
    3. "evaluate" - if we have both code and tests to evaluate
    4. "end" - only if everything is complete and validated

    Respond with ONLY ONE of these exact phrases: "generate code", "generate tests", "evaluate", or "end". After selecting do not add any other text.
    """
    
    response = supervisor_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="qwen-2.5-32b",
        temperature=0.3,
    )
    
    decision = response.choices[0].message.content.lower().strip()
    log(f"Supervisor raw decision: {decision}")
    
    # Parse decision
    if state.iteration >= state.max_iterations:
        state.next_step = "end"
    elif not state.code or state.last_agent == "evaluator":
        state.next_step = "coder"
    elif not state.tests:
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
    """Generates unit tests for the code with improved error handling and model fallback."""
    log("\n=== TESTER AGENT ===")
    
    prompt = f"""
    You are a unit test creator that creates 5 tests ONLY and always imports everything that is needed. Create unit tests for this code123.py file:
    {state.code}
    
    Based on these requirements:
    {state.plan}
    
    Your output should be a list of unit tests.
    """
    
    # Define model hierarchy for fallback
    models = [
        "qwen-2.5-32b",
        "llama-3.3-70b-versatile",
        "deepseek-r1-distill-llama-70b"
    ]
    
    response = None
    last_error = None
    
    for model in models:
        try:
            log(f"Attempting to use model: {model}")
            response = tester_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0.2,
            )
            
            # Log successful model use
            log(f"Successfully used model: {model}")
            break
            
        except Exception as e:
            last_error = e
            error_message = str(e)
            log(f"Error with model {model}: {error_message}")
            
            # If it's not a rate limit error, we might want to try the next model
            if "rate_limit" not in error_message.lower():
                continue
                
            # If it's a rate limit error, check if it's for Mixtral
            if "mixtral" in error_message.lower():
                log("Detected Mixtral rate limit despite not requesting Mixtral. This might indicate a model fallback issue.")
            
            # Wait a short time before trying the next model
            import time
            time.sleep(1)
    
    if response is None:
        # If all models failed, we need to handle this gracefully
        error_msg = f"All models failed. Last error: {last_error}"
        log(f"CRITICAL ERROR: {error_msg}")
        state.evaluation = f"Error in test generation: {error_msg}"
        state.next_step = "supervisor"
        state.last_agent = "tester"
        return state
    
    try:
        tmp = extract_code_blocks(response.choices[0].message.content)
        if not tmp:
            raise ValueError("No code blocks found in response")
        state.tests = tmp[0]
        
    except Exception as e:
        log(f"Error extracting code blocks: {str(e)}")
        state.tests = "# Error generating tests\n# Please review the code and try again"
    
    state.next_step = "supervisor"
    state.last_agent = "tester"
    
    log("Generated tests:")
    log(state.tests[:200] + "..." if len(state.tests) > 200 else state.tests)
    return state

def evaluator_agent(state: AgentState) -> AgentState:
    """Evaluates code and tests, providing feedback."""
    log("\n=== EVALUATOR AGENT ===")
    
    
    code_filename = "code123.py"
    with open(code_filename, "w") as f:
        f.write(state.code)
    print(f"\nCode has been saved to {code_filename}")
    
    test_filename = "tests.py"
    with open(test_filename, "w") as f:
        f.write(state.tests)
    print(f"\nTests have been saved to {test_filename}")
    
    test_results = run_unit_tests(test_filename)
    
    prompt = f"""
    based on the test results, {test_results}, and the code, {state.code},
    
    if the code is working, do not change the plan. if the code is not working,
    alter the plan: {state.plan}, to fix the issues in the code.
    
    Provide specific feedback on:
    1. Code functionality
    2. Test coverage
    3. Error handling
    
    
    """
    
    response = evaluator_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.3,
    )
    
    state.plan = response.choices[0].message.content
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
        result = workflow.invoke(initial_state, {"recursion_limit": 100})
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


app=FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JSONInput(BaseModel):
    prompt: str
    app1: str
    app2: str
    app_schemas: Dict[str, Any]

@app.post("/graph")
async def run_api_integration_endpoint(user_input: JSONInput):
    json_string = json.dumps(user_input.prompt)
    return run_api_integration(json_string)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)