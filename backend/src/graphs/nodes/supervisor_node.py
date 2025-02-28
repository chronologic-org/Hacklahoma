from typing import Dict, Any, Tuple
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from .base_node import BaseNode

class SupervisorOutput(BaseModel):
    coding_task: Dict[str, Any] = Field(
        description="The coding node is in charge of writing the program that will be used to interact with the APIs"
    )
    testing_task: Dict[str, Any] = Field(
        description="The testing node is in charge of taking the code provided by the coding node and testing it thoroughly using unit tests and other testing strategies"
    )
    acceptance_criteria: list[str] = Field(
        description="If the code runs and passes all of the tests, it is accepted as a successful integration"
    )

class SupervisorFeedback(BaseModel):
    requires_changes: bool = Field(
        description="Whether changes are needed"
    )
    feedback: Dict[str, Any] = Field(
        description="Detailed feedback for improvements"
    )
    next_steps: list[str] = Field(
        description="Steps to take next"
    )

class SupervisorNode(BaseNode):
    def __init__(self):
        super().__init__(temperature=0.3)
        self.output_parser = JsonOutputParser(pydantic_object=SupervisorOutput)
        
        self.prompt = PromptTemplate(
            template="""<task>
            You are a technical lead supervising an API integration project.
            Review this integration plan and divide it into specific tasks:

            Integration Plan: {plan}

            Create two separate task descriptions:
            1. For the coding team: Include specific implementation details, required functions, and data structures
            2. For the testing team: Include test scenarios, edge cases, and validation requirements

            Ensure both tasks align with the original plan and cover all requirements.
            </task>

            {format_instructions}
            """,
            input_variables=["plan"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

        self.review_prompt = PromptTemplate(
            template="""<task>
            You are a technical lead reviewing evaluation results.
            Review this evaluation and determine if changes are needed:

            Evaluation Results: {evaluation}
            Original Plan: {original_plan}

            Determine:
            1. If the implementation meets requirements
            2. What changes or improvements are needed
            3. Next steps for the team
            </task>

            {format_instructions}
            """,
            input_variables=["evaluation", "original_plan"],
            partial_variables={"format_instructions": JsonOutputParser(pydantic_object=SupervisorFeedback).get_format_instructions()}
        )

    async def process(self, plan: Dict[str, Any]) -> SupervisorOutput:
        formatted_prompt = self.prompt.format(plan=str(plan))
        response = await self.model.ainvoke(formatted_prompt)
        return self.output_parser.parse(response.content)

    async def review_evaluation(
        self, 
        evaluation: Dict[str, Any],
        original_plan: Dict[str, Any]
    ) -> SupervisorFeedback:
        formatted_prompt = self.review_prompt.format(
            evaluation=str(evaluation),
            original_plan=str(original_plan)
        )
        response = await self.model.ainvoke(formatted_prompt)
        return self.output_parser.parse(response.content) 