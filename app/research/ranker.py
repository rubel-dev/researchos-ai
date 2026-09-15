from app.schemas.research import SearchResult

def rank_results(
        results: list[SearchResult],
) -> list[SearchResult]:
    return sorted(
        results,
        key = lambda result: result.score or 0,
        reverse= True
    )