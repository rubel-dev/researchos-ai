

import math

from app.research.embedder import embed_text
from app.schemas.research import EmbeddedChunk, RetrievedChunk


def cosine_similarity(
        vector_a: list[float],
        vector_b: list[float]
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)

def retrieve_chunks(
        question: str,
        chunks: list[EmbeddedChunk],
        top_k: int = 5,
        
) -> list[RetrievedChunk]:
    question_embedding = embed_text(question)
    scored_chunks = []
    for chunk in chunks:
        score = cosine_similarity(
            question_embedding,
            chunk.embedding
        )

        scored_chunks.append(
            RetrievedChunk(
                source_url=chunk.source_url,
                chunk_id=chunk.chunk_id,
                content=chunk.content,
                similarity=score
            )
        )
    scored_chunks.sort(
        key=lambda chunk: chunk.similarity,
        reverse=True
    )
    return scored_chunks[:top_k]