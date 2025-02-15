from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from typing import Dict
from ..config.database import Database
from ..utils.logging import logger

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    details: Dict[str, str]

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check the health of the application and its dependencies.
    
    Returns:
        HealthResponse containing status and details of each component
    """
    health_details = {
        "api": "healthy",
        "database": "unknown"
    }
    
    try:
        # Check MongoDB connection
        await Database.client.admin.command('ping')
        health_details["database"] = "healthy"
        
        return HealthResponse(
            status="healthy",
            details=health_details
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        health_details["database"] = "unhealthy"
        
        return HealthResponse(
            status="degraded",
            details=health_details
        ) 