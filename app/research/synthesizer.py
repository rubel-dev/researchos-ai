

from openai import OpenAI

from app.core.config import settings
from app.schemas.research import ResearchAnswer, RetrievedChunk


client = OpenAI(
    api_key=settings.gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def synthesize_answer(
        question: str,
        chunks: list[RetrievedChunk],
) -> ResearchAnswer:

    context_parts = []
    for chunk in chunks:
        context_parts.append(
            f"""
CHUNK_ID: {chunk.chunk_id}
SOURCE_URL: {chunk.source_url}

CONTENT:
{chunk.content}
"""
        )

    context = "\n\n---\n\n".join(context_parts)
    response = client.chat.completions.parse(
        model=settings.gemini_model,
        messages=[
            {
                "role": "system",
                "content":"""
You are a grounded research assistant.
Answer the user's question using ONLY the provided evidence.
Rules:
- Do not use outside knowledge.
- Do not invent facts.
- If evidence is insufficient, clearly say so.
- Use only chunk IDS and sources URLS that appear in the evidence.
- Return concise but complete research findings.
"""

            },
            {
                "role": "user",
                "content": f"""
QUESTION:
{question}

EVIDENCE:
{context}
""",

            }
        ],
        response_format=ResearchAnswer,

    )
    return response.choices[0].message.parsed