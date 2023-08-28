"""Initialize the OpenAI API key."""
import os
import openai

# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Azure Open Ai
# Set OpenAI configuration settings
openai.api_type = "azure"
openai.api_base = "https://longfellowai.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")


def get_open_module():
    """Return the openai module."""
    return openai
