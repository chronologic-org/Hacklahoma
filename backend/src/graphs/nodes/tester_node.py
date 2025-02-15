from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class TestOutput(BaseModel):
    test_cases: Dict[str, Dict[str, Any]] = Field(
        description="Test cases with inputs and expected outputs"
    )
    test_implementation: Dict[str, str] = Field(
        description="Generated test code"
    )
    coverage_requirements: list[str] = Field(
        description="Required test coverage criteria"
    )

class TesterNode:
    def __init__(self):
        self.model = ChatOpenAI(temperature=0.2)
        self.output_parser = JsonOutputParser(pydantic_object=TestOutput)
        
        self.prompt = PromptTemplate(
            template="""You are a QA engineer creating tests for an API integration.
            Design comprehensive tests based on the following specifications:

            Testing Requirements: {testing_task}

            Create test cases that:
            1. Cover all critical functionality
            2. Include edge cases and error scenarios
            3. Validate integration points
            4. Follow testing best practices

            {format_instructions}
            """,
            input_variables=["testing_task"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

    async def process(self, testing_task: Dict[str, Any]) -> TestOutput:
        formatted_prompt = self.prompt.format(testing_task=str(testing_task))
        response = await self.model.ainvoke(formatted_prompt)
        return self.output_parser.parse(response.content) 