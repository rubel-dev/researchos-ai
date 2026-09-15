from app.schemas.research import QuerySearchResult, SearchResult

def deduplicate_results(
        searches: list[QuerySearchResult],
) -> list[SearchResult]:
    seen_urls = set()
    unique_results = []
    for search in searches:
        for result in search.results:
            if result.url in seen_urls:
                continue
            seen_urls.add(result.url)
            unique_results.append(result)
    return unique_results