from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    question: str = Field(min_length=5, max_length=1000)

class SearchQuery(BaseModel):
    query: str
    purpose: str

class QueryPlan(BaseModel):
    queries: list[SearchQuery]

class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    score: float | None = None
class QuerySearchResult(BaseModel):
    query: str
    purpose: str
    results: list[SearchResult]

class ExtractedSource(BaseModel):
    url: str
    content: str

class SourceChunk(BaseModel):
    source_url: str
    chunk_id: str
    content: str

class EmbeddedChunk(BaseModel):
    source_url: str
    chunk_id: str
    content: str
    embedding: list[float]

class RetrievedChunk(BaseModel):
    source_url: str
    chunk_id: str
    content: str
    similarity:float

class Citation(BaseModel):
    chunk_id: str
    source_url: str

class ResearchAnswer(BaseModel):
    answer: str
    citations: list[Citation]
