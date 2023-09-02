# load dotenv file
import os
from dotenv import load_dotenv

load_dotenv(".env")

# OPENAI_API_BASE="https://longfellowai.openai.azure.com"
# OPENAI_API_VERSION="2023-03-15-preview"
# OPENAI_API_KEY="eec94a2ef2dd4b1c93c953cbe368ef8f"
print("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
print("OPENAI_API_BASE", os.getenv("OPENAI_API_BASE"))
print("OPENAI_API_VERSION", os.getenv("OPENAI_API_VERSION"))
