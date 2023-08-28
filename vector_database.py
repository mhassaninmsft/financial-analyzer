import random
from pymilvus import (
    connections,
    # db,
    CollectionSchema,
    FieldSchema,
    DataType,
    Collection,
    utility,
)
from embedding_generation import generate_embedding


def bootsrtap() -> Collection:
    """Bootsrtap the database."""
    connections.connect(
        alias="default",
        user="username",
        password="password",
        host="localhost",
        port="19530",
        db_name="default",
    )
    chunk_id = FieldSchema(
        name="chunk_id",
        dtype=DataType.INT64,
        is_primary=True,
    )
    document_id = FieldSchema(
        name="document_id",
        dtype=DataType.INT64,
    )

    content = FieldSchema(
        name="content",
        dtype=DataType.VARCHAR,
        max_length=3000,
    )
    word_count = FieldSchema(
        name="word_count",
        dtype=DataType.INT64,
        # The default value will be used if this field is left empty during data inserts or upserts.
        # The data type of `default_value` must be the same as that specified in `dtype`.
        default_value=9999,
    )
    content_embedding = FieldSchema(
        name="content_embedding", dtype=DataType.FLOAT_VECTOR, dim=1536
    )
    schema = CollectionSchema(
        fields=[chunk_id, document_id, content, word_count, content_embedding],
        description="Chucnk Document Store",
        enable_dynamic_field=True,
    )
    collection_name = "book4"
    collection = Collection(
        name=collection_name, schema=schema, using="default", shards_num=2
    )
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 32, "efConstruction": 200},
    }
    collection.create_index(field_name="content_embedding", index_params=index_params)
    utility.index_building_progress("book")
    return collection

    # database = db.create_database("book")
    # connections.disconnect("default")


def search_data(text: str) -> list[str]:
    """Search the database for the text."""
    # generate a ramdom float between -1 and 1 vector with length 1536
    collection = bootsrtap()
    emb = generate_embedding(text)
    search_param = {
        "data": [emb],
        "anns_field": "content_embedding",
        "param": {"metric_type": "COSINE", "params": {"ef": 10}, "offset": 0},
        "limit": 10,
        "output_fields": ["content", "word_count"],
        # "output_fields": [],
        "expr": "word_count <= 11000",
    }
    collection.load()
    res = collection.search(**search_param)
    print(f"Search result: {res}")
    hits = res[0]
    print(f"Search hits: {hits}")
    result_content = []
    for hit in hits:
        result_content.append(hit.entity.content)
    print(f"Search result content: {result_content}")
    return result_content
