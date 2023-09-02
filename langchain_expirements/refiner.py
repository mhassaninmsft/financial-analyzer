from langchain.chains import RefineDocumentsChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import AzureOpenAI


def start():
    # This controls how each document will be formatted. Specifically,
    # it will be passed to `format_document` - see that function for more
    # details.
    document_prompt = PromptTemplate(
        input_variables=["page_content"], template="{page_content}"
    )
    document_variable_name = "context"
    llm = AzureOpenAI(deployment_name="gpt67")
    # The prompt here should take as an input variable the
    # `document_variable_name`
    prompt = PromptTemplate.from_template("Summarize this content: {context}")
    initial_llm_chain = LLMChain(llm=llm, prompt=prompt)
    initial_response_name = "prev_response"
    # The prompt here should take as an input variable the
    # `document_variable_name` as well as `initial_response_name`
    prompt_refine = PromptTemplate.from_template(
        "Here's your first summary: {prev_response}. "
        "Now add to it based on the following context: {context}"
    )
    refine_llm_chain = LLMChain(llm=llm, prompt=prompt_refine)
    chain = RefineDocumentsChain(
        initial_llm_chain=initial_llm_chain,
        refine_llm_chain=refine_llm_chain,
        document_prompt=document_prompt,
        document_variable_name=document_variable_name,
        initial_response_name=initial_response_name,
    )
    # read the file as string
    context = ""
    # with open("Output/file4.md", "r") as f:
    with open("Output/file4.md", "rb") as f:
        context = f.read().decode("utf-8")
    chain.run({"input_documents": {"page_content": [context]}})
    # chain.invoke()
