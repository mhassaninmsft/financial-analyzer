# extrach the metadata fields from the json file
import json
from embedding_generation import chunk_string
from chatbot import ChatBot
def extract_metadata_from_json() :
    """
    Extracts the metadata fields from the json file
    """
    json_file = "Output/summaries2.json"
    with open(json_file, "r") as f:
        data = json.load(f)
    # data is in array, for each element, extract the metadata
    # metadata= [d: for d in data]
    # print(data[0])
    # print(len(data))
    # metadata = []
    # for idx, chunk in enumerate(data):
    #     print(f"Chunk {idx}: {chunk}")


    content = [(d["content"]) for d in data]
    # if metadata is none, kip it
    # if metadata is not none, extract the metadata

    metadata = [d for d in content]
    for idx, chunk in enumerate(metadata):
        print(idx)
        try:
            d12 = json.loads(chunk)
            print(d12["metadata"])
        except:
            print(f"Chunk {idx}: failed with summary {chunk}")

        # print(f"Chunk {idx}: {chunk}")
    print(metadata[0])
    d1 = json.loads(metadata[0])
    print(d1["metadata"])
    return 

def custom_prompt():
    """Return the custom prompt."""
    # open the file and read the content to a string
    with open("Output/summaries2.json", "rb") as f:
        document = f.read()
    print(f"length of doc is {len(document)}")
    # take only the first 8000 words
    # document = document[:30000]
    # document = document[30000:60000]
    document = document[90000:150000]
    system_message="""I am working on a system that lets the users ask questions about financial statements documents using the Retriver Augmenet 
    Generation model. I need to complement what is available in the RAG pattern using custom anootations and extra table fields. based on the above summary and 
     question answer pairs. Can you suggest some extra information to store in an external database which a traditional RAG system would return poor results
      There will be multiple of such financial statements, one for each company and it will be yearly. We are looking to potentially get the annual statemets from perhaps 
       a couple of hundred companies """
    chat_bot = ChatBot(system_message=system_message)  # assuming ChatBot is an async class or doesn't block
    response = chat_bot.add_chatbot_message(f"Here is the document: {document}")  
    print(response)

def extract_info_from_documet() -> str:
    """This script will extract """
    with open("prompts/schema.txt", "rb") as f:
        schema = f.read()
    summary_so_far = "{}"
    system_message=f"""Based on the following schema {schema} , generate the appropriate JSON summary of this document chunk: 
    You should enhance the summary given the summary so far from previous chunks of the document. You should produce a new summary JSON document that
    follows the provided schema and that incorporates/modifies (enriches) the information from the previous chunks if applicable. IF the information
     is not available in the current summary or the current document chunk leave the summary sections null , do not make up fictitious information.
     Also you should keep the summary concise and to the point. each field should be a few to several words"""
    # chat_bot = ChatBot(system_message=system_message)  # assuming ChatBot is an async class or doesn't block
    # read the document itself as a string
    document=""
    with open("Output/file4.md", "rb") as f:
        document = f.read().decode("utf-8")
    # print(document) 
    # chunk the document
    chunks = chunk_string(document, chunk_size=12000, overlap=1000)
    print(f"Number of chunks: {len(chunks)}")
    for idx, chunk in enumerate(chunks):
        # print(f"Chunk {idx}: {chunk}")
        chat_bot = ChatBot(system_message=system_message)
        response = chat_bot.add_chatbot_message(f"Here is the document: {chunk} and here is the previous summary {summary_so_far}")
        print(response)
        summary_so_far = response
        print(f"summarizing chunk {idx}")
    print(f"final summary: {summary_so_far}")
    return summary_so_far
             