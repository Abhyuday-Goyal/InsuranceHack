import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.vectorstores import Pinecone as Pine
from pinecone import Pinecone
from pinecone.config import Config
from pinecone import ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from chunk_converter import split_into_sentence_chunks
import PyPDF2


def create_index(index_name, spec, pc):
    if index_name not in pc.list_indexes():
        # if does not exist, create index
        pc.create_index(
            index_name,
            dimension=1536,  # dimensionality of ada 002
            metric="dotproduct",
            spec=spec,
        )


def read_pdf(path):
    with open(os.path.join(path), "rb") as f:
        byte_sequence = f.read()
        content = byte_sequence.decode("utf-8", errors="ignore")
        return content


def add_embeds(sentence_chunks, embed_model, index):
    from tqdm.auto import tqdm
    from uuid import uuid4
    import time

    batch_size = 250
    for i in tqdm(range(0, len(sentence_chunks), batch_size)):

        i_min = min(i + batch_size, len(sentence_chunks))
        batch = sentence_chunks[i:i_min]
        meta_data = [{"title": "notes", "context": row} for row in batch]
        ids = [str(uuid4()) for _ in range(len(batch))]
        # Encode the text to obtain its vector representation
        embeds = embed_model.embed_documents(batch)

        # Upsert the vector and text into the Pinecone index
        index.upsert(vectors=zip(ids, embeds, meta_data))
        print("sleepin")
        time.sleep(4)


def augment_prompt(query: str, vectorstore: Pinecone):
    # get top 5 results from knowledge base
    results = vectorstore.similarity_search(query, k=5)
    # get the text from the results
    source_knowledge = "\n".join([x.page_content for x in results])
    # feed into an augmented prompt
    # augmented_prompt = f"""Using the contexts below, answer the query.

    # Contexts:
    # {source_knowledge}

    # Query: {query}"""

    augmented_prompt = f"""Use the given context to provide answers to the query.

    Contexts:
    {source_knowledge}

    Quert:
    {query}"""
    return augmented_prompt


def execute_query(query, messages, chat, vectorstore: Pinecone):
    prompt = HumanMessage(content=augment_prompt(query, vectorstore=vectorstore))
    # add to messages
    messages.append(prompt)
    res = chat.invoke(messages)
    return res.content
