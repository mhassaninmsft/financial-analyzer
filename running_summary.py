"""Generates a summary of the document which is large than the llm context window."""

from chatbot import ChatBot
from embedding_generation import chunk_string
import logging
import json
import asyncio

content_window = 16000
# read the system_prompt from file
with open("prompts/system_prompt.txt", "r") as f:
    system_prompt = f.read()

logging.info(f"System prompt: {system_prompt}")


def summarize_document(
    document: str,
) -> list[str]:
    """Summarize a document using the llm."""
    # split the document into chunks of 2000 characters
    chunks = chunk_string(document, chunk_size=4000, overlap=200)
    logging.info(f"Number of chunks: {len(chunks)}")
    idx = 0
    summaries = []
    for chunk in chunks:
        logging.info(f"Summarizing chunk {idx}")
        system_prompt = "You are an AI assistant helping a customer summarize a document. The customer says:\n"
        prompt_for_summary = f"Summarize the following document:\n{chunk}"
        chat_bot = ChatBot(system_message=system_prompt)
        resposne = chat_bot.add_chatbot_message(prompt_for_summary)
        logging.info(f"Summary: {resposne}")
        summaries.append(resposne)
        idx += 1
    return summaries


async def summarize_chunk(chunk: str, idx, semaphore: asyncio.Semaphore):
    async with semaphore:
        logging.info(f"Summarizing chunk {idx}")
        # system_prompt = "You are an AI assistant helping a customer summarize a document. The customer says:\n"
        prompt_for_summary = (
            f"Generate the appropriate JSON summary of this document chunk:\n{chunk}"
        )
        chat_bot = ChatBot(
            system_message=system_prompt
        )  # assuming ChatBot is an async class or doesn't block
        response = await chat_bot.add_chatbot_message_async(
            prompt_for_summary
        )  # this should be an async function
        # response = chat_bot.add_chatbot_message(prompt_for_summary)  # this should be an async function
        logging.info(f"Summary: {response}")
        return response


async def summarize_chunk_into_json(chunk: str, idx, semaphore: asyncio.Semaphore):
    async with semaphore:
        logging.info(f"Summarizing chunk {idx}")
        # system_prompt = "You are an AI assistant helping a customer summarize a document. The customer says:\n"
        with open("prompts/schema.txt", "rb") as f:
            schema = f.read()
        system_message = f"""Based on the following schema {schema} , generate the appropriate JSON summary of this document chunk: 
        do not make up fictitious information.
        Also you should keep the summary concise and to the point. each field should be a few to several words"""
        chat_bot = ChatBot(
            system_message=system_message
        )  # assuming ChatBot is an async class or doesn't block
        res = await chat_bot.add_chatbot_message_async(
            f"Create a JSON summary of the following document chunk:\n{chunk}"
        )
        return res


summaries = []


async def combine_summaries(summary1: str, summary2: str) -> str:
    # Your combiner logic here
    """This script will extract"""
    with open("prompts/schema.txt", "rb") as f:
        schema = f.read()
    system_message = f"""Based on the following schema {schema} , generate the appropriate JSON summary of this document chunk: 
    You should produce a new summary JSON document that
    follows the provided schema and that incorporates/modifies/comnbines (enriches) the information from the2 chunks. IF the information
     is not available in either summary leave such sections as null , do not make up fictitious information.
     Also you should keep the summary concise and to the point. each field should be a few to several words"""
    chat_bot = ChatBot(
        system_message=system_message
    )  # assuming ChatBot is an async class or doesn't block
    res = await chat_bot.add_chatbot_message_async(
        f"Here are the 2 summaries {summary1} and {summary2}"
    )
    print(f"combined summary: {res}")
    return res


async def worker(queue: asyncio.Queue, semaphore: asyncio.Semaphore):
    async with semaphore:
        while queue.qsize() > 1:
            summary1 = await queue.get()
            if queue.qsize() == 0:
                await queue.put(summary1)
                return
            summary2 = await queue.get()
            combined_summary = await combine_summaries(summary1, summary2)
            await queue.put(combined_summary)


async def combine_all_summaries(summaries: list[str]) -> str:
    queue = asyncio.Queue()
    for summary in summaries:
        await queue.put(summary)

    semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent tasks

    # Start worker tasks
    worker_tasks = [worker(queue, semaphore) for _ in range(10)]

    # Wait for all worker tasks to complete
    await asyncio.gather(*worker_tasks)

    return await queue.get()  # Return the final combined summary


async def summarize_document_async(document: str) -> list[str]:
    chunks = chunk_string(document, chunk_size=4000, overlap=200)
    logging.info(f"Number of chunks: {len(chunks)}")

    semaphore = asyncio.Semaphore(10)  # Limit to 10 parallel tasks

    summaries = await asyncio.gather(
        *[summarize_chunk(chunk, idx, semaphore) for idx, chunk in enumerate(chunks)]
    )

    return summaries


async def summarize_document_json_async(document: str) -> str:
    chunks = chunk_string(document, chunk_size=4000, overlap=200)
    logging.info(f"Number of chunks: {len(chunks)}")

    semaphore = asyncio.Semaphore(10)  # Limit to 10 parallel tasks

    summaries = await asyncio.gather(
        *[
            summarize_chunk_into_json(chunk, idx, semaphore)
            for idx, chunk in enumerate(chunks)
        ]
    )
    single_summary = await combine_all_summaries(summaries)

    return single_summary


def test1():
    # open the document
    document = ""
    with open("Output/file4.md", "r") as f:
        document = f.read()
    summaries = summarize_document(document)
    # save summaries to file as JSON
    with open("Output/summaries3.json", "w") as f:
        f.write(json.dumps(summaries))


async def test1_async():
    # open the document
    document = ""
    with open("Output/file4.md", "r") as f:
        document = f.read()
    summaries = await summarize_document_async(document)
    # save summaries to file as JSON
    with open("Output/summaries2.json", "w") as f:
        f.write(json.dumps(summaries))


async def json_summary_async():
    # open the document
    document = ""
    with open("Output/file4.md", "r") as f:
        document = f.read()
    summary = await summarize_document_json_async(document)

    print(f"final summary: {summary}")
