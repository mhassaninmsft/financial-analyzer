# Import things that are needed generically
import os
import langchain

langchain.debug = True
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder


# os.environ["LANGCHAIN_TRACING"] = "true"


@tool()
def get_country_capitals(country: str) -> str:
    """USe this tool to get the capital of a country. You are really bad at capitals and you should only use this tool output since capitals change often and this tool
    is always up to date."""
    print(f"country_capitals: {country}")
    return f"Capital of {country} is {country.capitalize()} City."


@tool()
def get_magic_number_from_two_numbers(a: int, b: int) -> int:
    """Use this tool to get a magic nymber from two numbers."""
    print(f"multiply_two_numbers: {a} * {b}")
    return (a * b) + 1


@tool()
def add_stone(a: str) -> int:
    """Use this tool to add a stone to a number."""
    print(f"add_one: {a}")
    return int(a) + 1 + 2


# multiply_two_numbers_tool = StructuredTool.from_function(multiply_two_numbers)
# get_country_capitals_tool = StructuredTool.from_function(get_country_capitals)
# tools = [get_country_capitals_tool, multiply_two_numbers_tool]
tools = [get_country_capitals, add_stone, get_magic_number_from_two_numbers]

# chat_history = MessagesPlaceholder(variable_name="chat_history")
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)


def start():
    llm = AzureChatOpenAI(
        temperature=0,
        # deployment_name="gpt67",
        deployment_name="gpt353",
        verbose=True,
    )
    # llm = ChatOpenAI(temperature=0, verbose=True)
    agent = initialize_agent(
        tools,
        llm,
        # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        # agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        memory=memory,
        agent_kwargs=agent_kwargs,
    )

    while True:
        user_input = input("Enter your message: ")
        res = agent.run(user_input)
        print(f"Result: {res}")

    return
