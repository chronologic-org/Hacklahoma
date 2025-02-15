from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class PlannerOutput(BaseModel):
    apis: Dict[str, Dict[str, Any]] = Field(
        description="Details of the two APIs to connect, including endpoints and authentication needs"
    )
    integration_plan: Dict[str, Any] = Field(
        description="Step-by-step plan for connecting the APIs"
    )
    requirements: list[str] = Field(
        description="Technical requirements and dependencies"
    )
    expected_output: Dict[str, Any] = Field(
        description="Expected format and structure of the final output"
    )
    validation_rules: list[str] = Field(
        description="Rules for validating the integration"
    )

class PlannerNode:
    def __init__(self):
        self.model = ChatOpenAI(temperature=0.7)
        self.output_parser = JsonOutputParser(pydantic_object=PlannerOutput)
        
        self.prompt = PromptTemplate(
            template="""You are an expert system architect specializing in API integrations.
            Analyze the following user request and create a detailed plan for connecting two APIs:

            User Request: {user_input}

            Create a comprehensive plan that includes:
            1. Detailed analysis of both APIs
            2. Step-by-step integration plan
            3. Technical requirements
            4. Expected output format
            5. Validation rules

            Focus on creating a practical and implementable solution.
            Be specific about endpoints, data transformations, and error handling.

            {format_instructions}
            """,
            input_variables=["user_input"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

    async def process(self, user_input: str) -> PlannerOutput:
        formatted_prompt = self.prompt.format(user_input=user_input)
        response = await self.model.ainvoke(formatted_prompt)
        return self.output_parser.parse(response.content) 