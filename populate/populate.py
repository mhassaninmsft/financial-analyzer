"""Populate the database with data.""" ""
import random
from models.chunk import Chunk
from vector_database import bootsrtap


def start_batch_job():
    """Starts a batch job to populate the database with data."""
    print("Starting batch job")
    print("Batch job completed")
    # generate 100 chunks
    chunks = []
    for i in range(100):
        embs = [random.uniform(-1, 1) for _ in range(1536)]
        chunks.append(
            Chunk(
                chunk_id=i,
                document_id=5,
                content=f"This is a chunk {i}",
                word_count=100,
                content_embedding=embs,
            )
        )
    print(f"Generated {len(chunks)} chunks")
    collection = bootsrtap()
    json_docs = [chunk.dict() for chunk in chunks]
    data = [
        [chunk.chunk_id for chunk in chunks],
        [chunk.document_id for chunk in chunks],
        [chunk.content for chunk in chunks],
        [chunk.word_count for chunk in chunks],
        [chunk.content_embedding for chunk in chunks],
    ]

    # collection.insert(data)

    # generate a ramdom float between -1 and 1 vector with length 1536
    data = [random.uniform(-1, 1) for _ in range(1536)]
    search_param = {
        "data": [data],
        "anns_field": "content_embedding",
        "param": {"metric_type": "COSINE", "params": {"ef": 10}, "offset": 0},
        "limit": 10,
        "output_fields": ["content", "word_count"],
        "expr": "word_count <= 11000",
    }
    collection.load()
    res = collection.search(**search_param)
    print(f"Search result: {res}")
    hits = res[0]
    print(f"Search hits: {hits}")
    return "dsa"
