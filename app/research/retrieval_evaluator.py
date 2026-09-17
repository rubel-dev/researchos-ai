from collections import Counter

from app.schemas.research import RetrievedChunk, SearchResult

def retrieval_diagnostics(
        top_sources: list[SearchResult],
        retrieved_chunks: list[RetrievedChunk]
) -> dict:
    retrieved_urls = [
        chunk.source_url
        for chunk in retrieved_chunks
    ]

    retrieved_url_set = set(retrieved_urls)

    source_coverage = []

    for source in top_sources:
        source_coverage.append(
            {
                "url": source.url,
                "search_score": source.score,
                "represented_in_retrieval":
                source.url in retrieved_url_set
            }
        )
    counts = Counter(retrieved_urls)

    return {
        "retrieved_chunk_count": len(retrieved_chunks),
        "unique_sources_retrieved": len(retrieved_url_set),
        "chunks_per_source": dict(counts),
        "source_coverage": source_coverage,
    }