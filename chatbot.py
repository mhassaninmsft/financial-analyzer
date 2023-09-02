"""Chatbot class for the chatbot app."""
import openai
from openai_class import chat_complete
from tenacity import retry, stop_after_attempt, wait_fixed, wait_exponential

class ChatBot:
    """Chatbot class for the chatbot app."""

    def __init__(
        self,
        system_message: str = "You are an AI assistant that helps people find information.",
    ):
        self._messages = [{"role": "system", "content": system_message}]
        self._engine = "gpt67"
        self._temperature = 0.2
        self._max_tokens = 2000
        self._top_p = 0.95
        self._frequency_penalty = 0
        self._presence_penalty = 0
        self._stop = None

    def _add_message(self, message: dict[str, str]):
        self._messages.append(message)

    @retry(stop=stop_after_attempt(6), wait=wait_exponential(multiplier=2, min=4, max=16))  
    def add_chatbot_message(self, message: str) -> str:
        """Add a message from the chatbot to the chat history.
        Typically executed after"""
        self._add_message({"role": "assistant", "content": message})
        response = openai.ChatCompletion.create(
            engine=self._engine,
            messages=self._messages,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            top_p=self._top_p,
            frequency_penalty=self._frequency_penalty,
            presence_penalty=self._presence_penalty,
            stop=self._stop,
        )
        self._add_message(response.choices[0].message)  # type: ignore
        return response.choices[0].message.content  # type: ignore
    
    @retry(stop=stop_after_attempt(6), wait=wait_exponential(multiplier=2, min=4, max=16))  
    async def add_chatbot_message_async(self, message: str) -> str:
        """Add a message from the chatbot to the chat history.
        Typically executed after"""
        self._add_message({"role": "assistant", "content": message})
        response = await chat_complete(timeout=60, payload={
            "messages": self._messages,
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
            "top_p": self._top_p,
            "frequency_penalty": self._frequency_penalty,
            "presence_penalty": self._presence_penalty,
            "stop": self._stop,
        })
        msg = response.json()["choices"][0]["message"]["content"]
        self._add_message(msg)  # type: ignore
        return msg  # type: ignore

    def add_user_message(self, message):
        """Add a message from the user to the chat history."""
        self._messages.append({"role": "user", "content": message})

    def get_chat_history(self):
        """Return the chat history."""
        return self._messages


# response = await openai_async.chat_complete(
#     _OPEN_AI_API_KEY,
#     timeout=2,
#     payload={
#         "model": "gpt-3.5-turbo",
#         "messages": [{"role": "user", "content": "Hello!"}],
#     },
# )
# print(response.json()["choices"][0]["message"])