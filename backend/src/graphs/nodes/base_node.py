from typing import Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from ...config.settings import settings
from ...utils.logging import logger

class BaseNode:
    def __init__(self, temperature: float = None):
        self.model = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature or settings.MODEL_TEMPERATURE,
            model_name=settings.MODEL_NAME
        )
        
    async def safe_parse(self, parser: JsonOutputParser, content: str) -> Dict[str, Any]:
        try:
            return parser.parse(content)
        except Exception as e:
            logger.error(f"Parsing error in {self.__class__.__name__}: {str(e)}")
            error_response = {
                "error": str(e),
                "content": content,
                "status": "failed"
            }
            return error_response 