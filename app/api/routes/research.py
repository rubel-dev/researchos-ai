from fastapi import APIRouter, HTTPException
from openai import InternalServerError

from app.research.deduplicator import deduplicate_results
from app.research.ranker import rank_results
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
    except InternalServerError as exc:
        print(exc)

        raise HTTPException(
            status_code=503,
            detail = "AI service is temporarily unavailable. Please try again."
        )
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate research plan"
        )
@router.post("/search")
def research_search(data: ResearchRequest):
    plan = generate_search_queries(data.question)
    searches = []

    for query in plan.queries:
        result = search_web(query)
        searches.append(result)
    unique_results = deduplicate_results(searches)
    ranked_results = rank_results(unique_results)
    top_sources = ranked_results[:5]
    return{
            "question": data.question,
            "plan": plan,
            "searches": searches,
            "unique_results": unique_results,
            "top_sources": top_sources
    }