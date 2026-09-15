from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    question: str = Field(min_length=5, max_length=1000)

class SearchQuery(BaseModel):
    query: str
    purpose: str

class QueryPlan(BaseModel):
    querires: list[SearchQuery]

class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    score: float | None = None
class QuerySearchResult(BaseModel):
    query: str
    purpose: str
    results: list[SearchResult]