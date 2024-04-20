import os
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)

use_serverless = True
from langchain_core.prompts import ChatPromptTemplate
import getpass
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone import Pinecone, ServerlessSpec, PodSpec
import time
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain_pinecone import PineconeVectorStore

from langchain.vectorstores.base import VectorStore


api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
if use_serverless:
    spec = ServerlessSpec(cloud="aws", region="us-east-1")
else:
    # if not using a starter index, you should specify a pod_type too
    spec = PodSpec()
# check for and delete index if already exists

# Get index name from environment variable
index_name = "abhy21"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of text-embedding-ada-002
        metric="dotproduct",
        spec=spec,
    )
    # Wait for index to be initialized
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)
else:
    print("Index already exists.")

# wait for index to be initialized
while not pc.describe_index(index_name).status["ready"]:
    time.sleep(1)
index = pc.Index(index_name)
index.describe_index_stats()

# Check if Pinecone API key is provided
if pinecone_api_key is None:
    raise ValueError(
        "Pinecone API key must be provided in either PINECONE_API_KEY environment variable"
    )

    # Initialize OpenAI embeddings
model_name = "text-embedding-ada-002"
embeddings = OpenAIEmbeddings(model=model_name, openai_api_key=api_key)
text_field = "text"
vectorstore = PineconeVectorStore(index, embeddings, text_field)

# Initialize Pinecone vector store
# vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
loader = TextLoader("boston_extracted.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
# vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
# vectorstore_from_docs = PineconeVectorStore.from_documents(
#   docs, index_name=index_name, embedding=embeddings
# )
retriever = vectorstore.as_retriever()

vectorstore.add_documents(docs)
messages = [
    SystemMessage(
        content="You are a helpful assistant that answers questions and asks questions if prompted using the contexts given."
    ),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?"),
    # HumanMessage(content="I'd like to understand string theory.")
]
# Perform similarity search
query = "what is flight number"
results = vectorstore.similarity_search(
    query=query, k=3  # our search query  # return 3 most relevant docs
)


template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# RAG
model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    # Add this line
    | prompt
    | model
    | StrOutputParser()
)

print(chain.invoke("what is flight number"))
