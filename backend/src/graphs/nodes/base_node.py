from typing import Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

class BaseNode:
    def __init__(self, temperature: float = 0.2):
        self.model = ChatOpenAI(temperature=temperature)
        
    async def safe_parse(self, parser: JsonOutputParser, content: str) -> Dict[str, Any]:
        try:
            return parser.parse(content)
        except Exception as e:
            # Log the error and return a structured error response
            error_response = {
                "error": str(e),
                "content": content,
                "status": "failed"
            }
            # You might want to log this error
            return error_response 