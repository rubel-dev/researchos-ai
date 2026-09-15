from fastapi import APIRouter, HTTPException

from app.research.search import search_web
from app.schemas.research import ResearchRequest, QueryPlan
from app.research.query_planner import generate_search_queries

router = APIRouter(
    prefix="/research",
    tags = ["Research"],
)

@router.post("/plan", response_model= QueryPlan)
def create_research_plan(data: ResearchRequest):
    try:
        return generate_search_queries(data.question)
    except Exception as exc:
        print(exc)

        raise HTTPException(
            status_code=500,
            detail = "Failed to generate research plan"
        )

@router.post("/search")
def research_search(data: ResearchRequest):
    plan = generate_search_queries(data.question)
    searches = []

    for query in plan.queries:
        result = search_web(query)
        searches.append(result)

    return{
            "question": data.question,
            "plan": plan,
            "searches": searches
    }