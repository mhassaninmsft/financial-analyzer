"""Convert a docx file to markdown."""
from models.chunk import Chunk
import logging
import mammoth

from embedding_generation import chunk_string, generate_embedding
from vector_database import bootsrtap

# from PIL import Image
global img_number
img_number = 0


def custom_image_handler(image, file_path: str):
    """Return True to ignore images, False to include them as base64."""
    logging.info(f"image: {image} and file_path: {file_path}")
    global img_number
    # save the image to a file
    # image_path = "Output/" + image.filename
    with image.open() as image_bytes:
        # save to disk
        with open(f"Output/${img_number}.jpg", "wb") as f:
            f.write(image_bytes.read())
            img_number += 1
    print("ignoring_images")
    return ""


def null_image_handler(image, file_path: str):
    """Return True to ignore images, False to include them as base64."""
    return ""


def process_file(file_path: str) -> str:
    """Convert a docx file to markdown."""
    with open(file_path, "rb") as docx_file:
        result = mammoth.convert_to_markdown(
            docx_file,
            convert_image=lambda image: null_image_handler(image, file_path),
        )
        markdown = result.value  # The generated MArkdown
        messages = result.messages  # Any messages, such as warnings during conversion
        logging.debug("messages: %s", messages)
        logging.info("markdown: %s", markdown)
        # Write the markdown to a file
        output_file_path = "Output/file3.md"
        with open(output_file_path, "w", encoding="utf8") as markdown_file:
            markdown_file.write(markdown)
        process_markdown_string(markdown)
    return markdown


# process the markdown file
def process_markdown_string(text: str):
    """Process the markdown string."""
    string_chuncks = chunk_string(text)
    logging.info(f"total number of chunks: {len(string_chuncks)}")
    idx = 0
    chunks = []
    for string_chunck in string_chuncks:
        logging.info(f"processing chunk: {idx}")
        emb = generate_embedding(string_chunck)
        chunks.append(
            Chunk(
                chunk_id=idx,
                document_id=5,
                content=f"{string_chunck}",
                word_count=len(string_chunck.split()),
                content_embedding=emb,
            )
        )
        idx += 1

    print(f"Generated {len(chunks)} chunks")
    collection = bootsrtap()
    # json_docs = [chunk.dict() for chunk in chunks]
    data = [
        [chunk.chunk_id for chunk in chunks],
        [chunk.document_id for chunk in chunks],
        [chunk.content for chunk in chunks],
        [chunk.word_count for chunk in chunks],
        [chunk.content_embedding for chunk in chunks],
    ]
    collection.insert(data)
