from fastapi import FastAPI
from app.api.routes.research import router as research_router

app = FastAPI(
    title= "ResearchOS",
    version="0.1.0",
)

app.include_router(research_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }