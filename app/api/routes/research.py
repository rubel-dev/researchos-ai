from fastapi import APIRouter, HTTPException
from openai import InternalServerError

from app.research.chunker import chunk_sources
from app.research.deduplicator import deduplicate_results
from app.research.embedder import embed_chunks
from app.research.extractor import extract_sources
from app.research.ranker import rank_results
from app.research.retrieval_evaluator import retrieval_diagnostics
from app.research.retriever import retrieve_chunks
from app.research.search import search_web
from app.research.synthesizer import synthesize_answer
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
    extracted_sources = extract_sources(top_sources)
    chunks = chunk_sources(extracted_sources)
    embedded = embed_chunks(chunks)

    retrieved_chunks = retrieve_chunks(
        question=data.question,
        chunks = embedded,
        top_k=5
    )
    diagnostics = retrieval_diagnostics(
        top_sources=top_sources,
        retrieved_chunks=retrieved_chunks
    )
    answer = synthesize_answer(
        question = data.question,
        chunks=retrieved_chunks
    )
    return{
            "question": data.question,
            "plan": plan, 
            "top_sources": top_sources,
            "retrieved_chunks": retrieved_chunks,
            "retrieval_diagnostics": diagnostics,
            "answer": answer
             
    }