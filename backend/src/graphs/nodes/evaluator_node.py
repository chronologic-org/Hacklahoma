from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class EvaluationOutput(BaseModel):
    code_evaluation: Dict[str, Any] = Field(
        description="Results of code evaluation and testing"
    )
    issues_found: list[Dict[str, Any]] = Field(
        description="List of issues found during evaluation"
    )
    test_results: Dict[str, Any] = Field(
        description="Results of running test cases"
    )
    recommendations: list[str] = Field(
        description="Recommendations for improvements"
    )
    is_acceptable: bool = Field(
        description="Whether the implementation meets requirements"
    )

class EvaluatorNode:
    def __init__(self):
        self.model = ChatOpenAI(temperature=0.2)
        self.output_parser = JsonOutputParser(pydantic_object=EvaluationOutput)
        
        self.prompt = PromptTemplate(
            template="""You are an expert system evaluator analyzing both implementation code and test results.
            Review the following code implementation and test results:

            Implementation Code:
            {code_output}

            Test Results:
            {test_output}

            Original Requirements:
            {original_plan}

            Evaluate:
            1. Code quality and correctness
            2. Test coverage and effectiveness
            3. Alignment with original requirements
            4. Potential issues or vulnerabilities
            5. Performance considerations

            Provide a detailed evaluation and determine if the implementation is acceptable.

            {format_instructions}
            """,
            input_variables=["code_output", "test_output", "original_plan"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

    async def process(
        self, 
        code_output: Dict[str, Any], 
        test_output: Dict[str, Any],
        original_plan: Dict[str, Any]
    ) -> EvaluationOutput:
        formatted_prompt = self.prompt.format(
            code_output=str(code_output),
            test_output=str(test_output),
            original_plan=str(original_plan)
        )
        response = await self.model.ainvoke(formatted_prompt)
        return self.output_parser.parse(response.content) 