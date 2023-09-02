#!/bin/python3
"""Hello World App"""
import config
from configure_logging import configure_logging

# from playground import (
#     custom_prompt,
#     extract_metadata_from_json,
#     extract_info_from_documet,
# )

configure_logging()
import asyncio

# from embedding_generation import generate_embedding
# from markdown_conversion import process_file
# from populate.populate import start_batch_job
from running_summary import summarize_document, test1_async, json_summary_async

# from vector_database import bootsrtap, search_data
from langchain_trials import trail1

# import running_summary
from langchain_expirements import refiner, tool_user


print("Hello world")

if __name__ == "__main__":
    print("Hi there")
    # bootsrtap()
    # start_batch_job()
    # my_emb = generate_embedding("This is a test")
    # print(f"Embedding: {my_emb}")
    # process_file("Resources/2022_Annual_Report.docx")
    # process_file("Resources/hdr2021-22pdf_1.docx")
    # search_data("How does uncertainity affect the human development index?")
    # trail1()
    # refiner.start()
    # tool_user.start()
    # running_summary.test1()
    # custom_prompt()
    # extract_info_from_documet()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(test1_async())
    loop.run_until_complete(json_summary_async())
    # extract_metadata_from_json()
