from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from .base_node import BaseNode

class CodeOutput(BaseModel):
    implementation: Dict[str, str] = Field(
        description="Generated code for different components"
    )
    dependencies: list[str] = Field(
        description="Required dependencies and versions"
    )
    setup_instructions: list[str] = Field(
        description="Instructions for setting up the code"
    )

class CoderNode(BaseNode):
    def __init__(self):
        super().__init__(temperature=0.2)
        self.output_parser = JsonOutputParser(pydantic_object=CodeOutput)
        
        self.prompt = PromptTemplate(
            template="""<task>
            You are an expert programmer implementing an API integration.
            Create code based on these specifications:

            Task Details: {coding_task}

            Generate implementation code that:
            1. Follows best practices and design patterns
            2. Includes error handling and logging
            3. Is well-documented and maintainable

            Provide complete, working code implementations.
            </task>

            {format_instructions}
            """,
            input_variables=["coding_task"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

    async def process(self, coding_task: Dict[str, Any]) -> CodeOutput:
        formatted_prompt = self.prompt.format(coding_task=str(coding_task))
        response = await self.model.ainvoke(formatted_prompt)
        return self.output_parser.parse(response.content) 