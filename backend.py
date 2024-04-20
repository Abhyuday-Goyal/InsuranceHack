from flask import Flask, request, jsonify
import pandas as pd
import joblib
from pdftext import pdf_to_text
from main import read_pdf, add_embeds
from pinecone import Pinecone
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.vectorstores import Pinecone as Pine
from pinecone.config import Config
from pinecone import ServerlessSpec
from langchain_openai import OpenAIEmbeddings
import os 
from langchain_openai import ChatOpenAI

from main import create_index, read_pdf, add_embeds, split_into_sentence_chunks, execute_query

app = Flask(__name__)

pc_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pc_api_key)

spec = ServerlessSpec(
    cloud="aws", region="us-east-1"
)

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(
    openai_api_key= OPENAI_KEY,
    model='gpt-3.5-turbo'
)

#the embeddings model for vector embeddings
embed_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key = OPENAI_KEY)

messages = [
    SystemMessage(content="""You are a complete insurance policy expert. You can answer questions about insurance policies and compare two insurance policies
                  to determine the differences and similarities between them. You can also provide recommendations based on the policies provided.
                  You can also provide explanations on insurance terms and concepts. You can also provide general information on insurance policies.
                  
                  Return your responses in a structured report format. You can also provide a summary of the differences and similarities between the two policies.
                  Remember to mention clearly which company you are talking about so that the reader can understand the context of the information provided.
                  You can also provide numbers and clear differences between the two policies."""),
    #SystemMessage(content="You are a helpful assistant that answers questions and asks questions if prompted using the contexts given."),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?"),
    # HumanMessage(content="I'd like to understand string theory.")
]

max_chunk_length = 500  # Choose the maximum length for each chunk
index_name = 'abhy21'

# pc.delete_index(index_name)

# create_index(index_name, spec, pc)

index = pc.Index(index_name)

text_field = "context"  # the metadata field that contains our text

# initialize the vector store object
vectorstore = Pine(
    index, embed_model.embed_query, text_field
)


@app.route('/predict-premium', methods=['POST'])
def predict_premium():
    input_data = request.get_json()
    df = pd.DataFrame(input_data)
 
    model = joblib.load('xgb_regression_model.pkl')

    result = model.predict(df)
    return str(result[0])

@app.route('/upload-policies', methods=['POST'])
def upload_policies():
    if 'pdf1' not in request.files or 'pdf2' not in request.files:
        return 'Missing files', 400
    
    uploaded_files = request.files.getlist("file")
    print(uploaded_files)


    pdf1 = request.files['pdf1']
    pdf2 = request.files['pdf2']
    pdf1.save('./pdf1.pdf')
    pdf2.save('./pdf2.pdf')

    text1 = pdf_to_text(r'C:\Nishkal\Bitcamp 2024\InsuranceHack\pdf1.pdf')
    text2 = pdf_to_text(r'C:\Nishkal\Bitcamp 2024\InsuranceHack\pdf2.pdf')

    pdf1_data = read_pdf(text1)
    pdf2_data = read_pdf(text2)

    pdf1_chunks = split_into_sentence_chunks(pdf1_data, max_chunk_length)
    pdf2_chunks = split_into_sentence_chunks(pdf2_data, max_chunk_length)

    add_embeds(pdf1_chunks, embed_model, index)
    add_embeds(pdf2_chunks, embed_model, index)

    return "Policies processed!", 200

@app.route('/compare-policies', methods=['POST'])
def compare_policies():
    input_data = request.json
    query = input_data.get('query')
    output = execute_query(query, messages, chat, vectorstore)
    return jsonify(output=output)

@app.route('/clear_database', methods=['GET'])
def clear_database():
    pc.delete_index(index_name)
    create_index(index_name, spec, pc)
    return "Database cleared!", 200

if __name__ == '__main__':
    app.run(debug = False)