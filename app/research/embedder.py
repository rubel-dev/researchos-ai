from pydoc import text

from openai import OpenAI

from app.core.config import settings
from app.schemas.research import SourceChunk, EmbeddedChunk

client = OpenAI(
    api_key=settings.gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

EMBEDDING_MODEL = "gemini-embedding-001"

def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

def embed_chunks(
        chunks: list[SourceChunk],
) -> list[EmbeddedChunk]:
    embedded_chunks = []
    for chunk in chunks:
        vector = embed_text(chunk.content)

        embedded_chunks.append(
            EmbeddedChunk(
                source_url=chunk.source_url,
                chunk_id=chunk.chunk_id,
                content=chunk.content,
                embedding=vector
            )
        )
    return embedded_chunks