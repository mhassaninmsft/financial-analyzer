"""Initialize the OpenAI API key."""
import os
import openai
import httpx
import logging

# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Azure Open Ai
# Set OpenAI configuration settings
openai.api_type = "azure"
openai.api_base = "https://longfellowai.openai.azure.com/"
openai.api_version = "2023-08-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

azure_openai_api_key = os.getenv("OPENAI_API_KEY") or ""


def _send_to_openai(
    endpoint_url: str,
):
    async def send_to_openai(
        timeout: float, payload: dict, api_key: str = azure_openai_api_key
    ) -> httpx.Response:
        """
        Send a request to openai.
        :param api_key: your api key
        :param timeout: timeout in seconds
        :param payload: the request body, as detailed here: https://beta.openai.com/docs/api-reference
        """
        async with httpx.AsyncClient() as client:
            return await client.post(
                url=endpoint_url,
                json=payload,
                headers={"content_type": "application/json", "api-key": f"{api_key}"},
                timeout=timeout,
            )

    return send_to_openai


# POST https://{your-resource-name}.openai.azure.com/openai/deployments/{deployment-id}/chat/completions?api-version={api-version}
# POST https://{your-resource-name}.openai.azure.com/openai/deployments/{deployment-id}/embeddings?api-version={api-version}
complete = _send_to_openai("https://api.openai.com/v1/completions")
generate_img = _send_to_openai("https://api.openai.com/v1/images/generations")
embeddings = _send_to_openai(
    "https://longfellowai.openai.azure.com/openai/deployments/adaembedding1/embeddings?api-version=2023-08-01-preview"
)
chat_complete = _send_to_openai(
    "https://longfellowai.openai.azure.com/openai/deployments/gpt67/chat/completions?api-version=2023-08-01-preview"
)


def get_open_module():
    """Return the openai module."""
    return openai
