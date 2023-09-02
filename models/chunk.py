"""Chunk model"""
from pydantic import BaseModel, conlist


class Chunk(BaseModel):
    """Chunk model"""

    chunk_id: int
    document_id: int
    content: str
    word_count: int
    # list should be 1546 in size
    # content_embedding: conlist(float, min_length=1536, max_length=1536)  # type: ignore
    content_embedding: list #conlist(float, min_items==1536, max_items==1536)  # type: ignore
