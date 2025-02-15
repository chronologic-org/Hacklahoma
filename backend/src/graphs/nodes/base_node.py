from typing import Dict, Any
from langchain.chat_models import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from ...config.settings import settings
from ...utils.logging import logger
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks import get_openai_callback

class BaseNode:
    def __init__(self, temperature: float = None):
        try:
            self.model = ChatGroq(
                groq_api_key=settings.GROQ_API_KEY,
                temperature=temperature or settings.MODEL_TEMPERATURE,
                model_name=settings.MODEL_NAME,
                request_timeout=60,
                max_retries=3
            )
        except Exception as e:
            logger.error(f"Failed to initialize {self.__class__.__name__}: {str(e)}")
            raise
        
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