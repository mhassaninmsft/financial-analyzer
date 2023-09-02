"""Generate embeddings for a string."""
import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from openai_class import get_open_module


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))  
def generate_embedding(text: str) -> list[float]:
    """Generate embedding for the string."""
    # openai = get_open_module()
    # model = "text-embedding-ada-002"
    engine = "adaembedding1"
    return openai.Embedding.create(input=[text], engine=engine)["data"][0]["embedding"]  # type: ignore


def chunk_string(s: str, chunk_size=1000, overlap=200) -> list[str]:
    """Chunk the string into smaller chunks."""
    if len(s) <= chunk_size:
        return [s]
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    chunks: list[str] = []
    idx = 0
    while idx < len(s):
        end_idx = idx + chunk_size
        chunks.append(s[idx:end_idx])
        idx += chunk_size - overlap
    return chunks
