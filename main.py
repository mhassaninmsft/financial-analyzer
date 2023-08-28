#!/bin/python3
"""Hello World App"""

from embedding_generation import generate_embedding
from markdown_conversion import process_file
from populate.populate import start_batch_job
from vector_database import bootsrtap, search_data
from configure_logging import configure_logging

configure_logging()

print("Hello world")

if __name__ == "__main__":
    print("Hi there")
    # bootsrtap()
    # start_batch_job()
    # my_emb = generate_embedding("This is a test")
    # print(f"Embedding: {my_emb}")
    # process_file("Resources/hdr2021-22pdf_1.docx")
    search_data("How does uncertainity affect the human development index?")
