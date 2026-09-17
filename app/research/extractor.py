from tavily import TavilyClient
from app.core.config import settings

from app.schemas.research import ExtractedSource, SearchResult

client = TavilyClient(
    api_key=settings.tavily_api_key
)

def extract_sources(
        sources: list[SearchResult],
) -> list[ExtractedSource]:
    urls = [source.url for source in sources]

    response = client.extract(
        urls= urls,
        extract_depth='basic',
    )
    extract_sources = []
    for item in response["results"]:
        extract_sources.append(
            ExtractedSource(
                
                url= item["url"],
                content= item["raw_content"]
                 
            )
        )
    return extract_sources