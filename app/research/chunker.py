from app.schemas.research import ExtractedSource, SourceChunk


def chunk_source(
        source: ExtractedSource,
        max_chars: int = 2500,
) -> list[SourceChunk]:
    paragraphs = [
        p.strip()
        for p in source.content.split("\n")
        if p.strip()
    ]
    chunks = []
    current_parts = []
    current_length = 0
    chunk_index = 1

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)
        if current_parts and current_length + paragraph_length > max_chars:
            content = "\n\n".join(current_parts)
            chunks.append(
                SourceChunk(
                    source_url=source.url,
                    chunk_id=f"{source.url}#chunk-{chunk_index}",
                    content=content
                )
            )
            chunk_index += 1
            current_parts = []
            current_length = 0
        current_parts.append(paragraph)
        current_length += paragraph_length
    if current_parts:
        chunks.append(
            SourceChunk(
                source_url=source.url,
                chunk_id=f"{source.url}#chunk-{chunk_index}",
                content="\n\n".join(current_parts)
            )
        )
    return chunks

def chunk_sources(
        sources: list[ExtractedSource],
) -> list[SourceChunk]:
    all_chunks = []
    for source in sources:
        all_chunks.extend(chunk_source(source))
    return all_chunks