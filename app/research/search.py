from tavily import TavilyClient

from app.core.config import settings
from app.schemas.research import(
    SearchQuery,
    SearchResult,
    QuerySearchResult
)

client = TavilyClient(
    api_key = settings.taviliy_api_key
)

def search_web(
        search_query: SearchQuery
) -> QuerySearchResult:
    response = client.search(
        query = search_query.query,
        search_depth = "basic",
        max_results = 5
    )
    results = []

    for item in response ["results"]:
        results.append(
            SearchResult(
                title=item["title"],
                url=item["url"],
                content=item["content"],
                score=item.get("score")
            )
        )
    return QuerySearchResult(
        query=search_query.query,
        purpose=search_query.purpose,
        results=results
    )