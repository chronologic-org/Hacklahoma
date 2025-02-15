from typing import Dict, Any, Tuple
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class SupervisorOutput(BaseModel):
    coding_task: Dict[str, Any] = Field(
        description="Detailed instructions for the coding node"
    )
    testing_task: Dict[str, Any] = Field(
        description="Detailed instructions for the testing node"
    )
    acceptance_criteria: list[str] = Field(
        description="Criteria for accepting the final implementation"
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

class SupervisorNode:
    def __init__(self):
        self.model = ChatOpenAI(temperature=0.3)
        self.output_parser = JsonOutputParser(pydantic_object=SupervisorOutput)
        
        self.prompt = PromptTemplate(
            template="""You are a technical lead supervising an API integration project.
            Review the following integration plan and divide it into specific tasks for coding and testing:

            Integration Plan: {plan}

            Create two separate task descriptions:
            1. For the coding team: Include specific implementation details, required functions, and data structures
            2. For the testing team: Include test scenarios, edge cases, and validation requirements

            Ensure both tasks align with the original plan and cover all requirements.

            {format_instructions}
            """,
            input_variables=["plan"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

        self.review_prompt = PromptTemplate(
            template="""You are a technical lead reviewing the evaluation results of an API integration.
            Review the following evaluation and determine if changes are needed:

            Evaluation Results: {evaluation}
            Original Plan: {original_plan}

            Determine:
            1. If the implementation meets requirements
            2. What changes or improvements are needed
            3. Next steps for the team

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