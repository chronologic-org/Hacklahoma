from fastapi import APIRouter
from .api_v1 import router as api_v1_router
from .health import router as health_router

# Main router that includes all sub-routers
router = APIRouter()

# Include all routers
router.include_router(health_router)
router.include_router(api_v1_router) 