"""Langchain Trials"""
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI

from langchain.chains import LLMChain, RefineDocumentsChain
from langchain.prompts import PromptTemplate


def trail1():
    llm = AzureChatOpenAI(
        temperature=0.9,
        deployment_name="gpt353",
        # deployment_name="gpt67",
        # openai_api_version="2023-05-15",
    )
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    # Run the chain only specifying the input variable.
    print(chain.run("colorful socks"))
