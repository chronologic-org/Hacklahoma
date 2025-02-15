from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import connect_to_mongo, close_mongo_connection
from routes.example import router as example_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

app.include_router(example_router, prefix="/api") 