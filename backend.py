from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean
from pdftext import pdf_to_text
from main import read_pdf, add_embeds
from pinecone import Pinecone
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.vectorstores import Pinecone as Pine
from pinecone.config import Config
from pinecone import ServerlessSpec
from langchain_openai import OpenAIEmbeddings
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from langchain_openai import ChatOpenAI
from find_provider_details import search_in_excel
import requests
from flask_cors import CORS

Base = declarative_base()
from main import (
    create_index,
    read_pdf,
    add_embeds,
    split_into_sentence_chunks,
    execute_query,
)

app = Flask(__name__)
CORS(app)

pc_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pc_api_key)

spec = ServerlessSpec(cloud="aws", region="us-east-1")

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(openai_api_key=OPENAI_KEY, model="gpt-3.5-turbo")

# the embeddings model for vector embeddings
embed_model = OpenAIEmbeddings(
    model="text-embedding-ada-002", openai_api_key=OPENAI_KEY
)
messages2 = [
    SystemMessage(
        content="""You are a complete insurance policy expert. You can answer any questions about the insurance policy of a user. Analyze the uploaded insurance policy and provide a detailed reports on whatever the user requests.
        Remember to provide exact numbers and figures from the policy for better understanding.
        
        Focus on the costs of the policy, the coverage provided, and any other important details that the user may need to know. You can also provide a summary of the policy and its benefits."""
    ),
]
messages = [
    SystemMessage(
        content="""You are a complete insurance policy expert. You can answer questions about insurance policies and compare two insurance policies
                  to determine the differences and similarities between them. FOCUS ON THE COVERAGE INFORMATION, DEDUCTIBLES, AND SCHEDULE OF BENEFITS. You can also provide recommendations based on the policies provided.
                  You can also provide explanations on insurance terms and concepts. You can also provide general information on insurance policies.
                  
                  You can also provide a summary of the differences and similarities between the two policies.
                  Remember to mention clearly which company you are talking about so that the reader can understand the context of the information provided.
                  You can also provide numbers and clear differences between the two policies.
                  
                  Make sure to include the following:
                  Difference in coverage information
                  Difference in deductibles
                  Difference in schedule of benefits
                  
                  For example,
                  If one policy has out-of-pocket maximum for individual as $1000, and the other has it at $2000
                  show it as:
                  Policy 1: Out-of-pocket maximum for individual: $1000
                  Policy 2: Out-of-pocket maximum for individual: $2000
                  
                  Similar for deductible for individual and family."""
    ),
    # SystemMessage(content="You are a helpful assistant that answers questions and asks questions if prompted using the contexts given."),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?"),
    # HumanMessage(content="I'd like to understand string theory.")
]


messages3 = [
    SystemMessage(
        content="""Your only job is to give me the first word in the name of the insurance provider
                    For example, if the provider is 'UnitedHealthcare', just say 'United'
                    if the provider is 'Blue Cross Blue Shield', just say 'Blue'
                    if the provider is 'Aetna' or 'Aetna insurance', just say 'Aetna'
                    
                    You will not return anything else apart from this name."""
    ),
]


class Person(Base):
    __tablename__ = "people"
    userID = Column("ID ", Integer, primary_key=True)
    username = Column("FirstName", String)
    age = Column("Age", Integer)
    sex = Column("Sex", String)
    bmi = Column("BMI", Float)
    children = Column("Number of Children", Integer)
    smoker = Column("smoker", String)
    region = Column("region", String)
    riskIndex = Column("risk_index", Float)
    state = Column("state", String)


engine = create_engine("sqlite:///new_database.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


@app.route("/provider_details", methods=["POST"])
def provider_details():
    data = request.json
    provider = data["provider"]

    user_data = requests.get("http://127.0.0.1:5000/users")
    user_data = user_data.json()
    user_data = user_data["users"]
    user_data = user_data[-1]

    state = user_data["state"]
    file_path = "transparency_in_coverage_PUF.xlsx"
    sheet_name = "Transparency 2024 - Ind QHP"
    search_column_index = 4
    extract_columns = [14, 15, 16, 17]
    result = search_in_excel(
        file_path, sheet_name, search_column_index, provider, extract_columns, state
    )

    actual_result_dict = {}
    actual_result_dict["Total In Network Claims"] = result[14]
    actual_result_dict["Total Out of Network Claims"] = result[15]
    actual_result_dict["Total In Network Denied Claims"] = result[16]
    actual_result_dict["Total Out of Network Denied Claims"] = result[17]

    return jsonify(actual_result_dict)


@app.route("/add_person", methods=["POST"])
def add_person():
    session = Session()
    try:
        data = request.json

        input_data = {
            "age": [data["age"]],
            "sex": [data["sex"]],
            "bmi": [data["bmi"]],
            "children": [data["children"]],
            "smoker": [data["smoker"]],
            "region": [data["region"]],
            "state": [data["state"]],
        }

        df = pd.DataFrame(input_data)
        model = joblib.load("./xgb_regression_model.pkl")
        result = model.predict(df)
        result = (result[0] - 1121.87) / (63770.43 - 1121.87)

        data["riskIndex"] = result

        person = Person(**data)
        session.add(person)
        session.commit()

        return jsonify({"message": "Person added successfully"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route("/users", methods=["GET"])
def get_users():
    session = Session()
    users = session.query(Person).all()
    user_list = []
    for user in users:
        user_data = {
            "age": user.age,
            "sex": user.sex,
            "bmi": user.bmi,
            "children": user.children,
            "smoker": user.smoker,
            "region": user.region,
            "state": user.state,
        }
        user_list.append(user_data)
    return jsonify({"users": user_list})


max_chunk_length = 500  # Choose the maximum length for each chunk
index_name = "abhy21"

# pc.delete_index(index_name)

# create_index(index_name, spec, pc)

index = pc.Index(index_name)

text_field = "context"  # the metadata field that contains our text

# initialize the vector store object
vectorstore = Pine(index, embed_model.embed_query, text_field)


@app.route("/load_info_pdf", methods=["GET"])
def load_info_pdf():
    try:
        text = pdf_to_text(
            r"C:\Nishkal\Bitcamp 2024\InsuranceHack\002_Health_Coverage_Basics.pdf"
        )
        pdf_data = read_pdf(text)

        pdf_chunks = split_into_sentence_chunks(pdf_data, max_chunk_length)
        add_embeds(pdf_chunks, embed_model, index)
        return "Added PDF data to the database!", 200
    except Exception as e:
        # Log the error or print it for debugging
        print("Error:", e)
        # Return an appropriate error response
        return "Internal Server Error", 500


# @app.route("/predict-premium", methods=["POST"])
# def predict_premium():
#     try:
#         input_data = request.get_json()
#         df = pd.DataFrame(input_data)
#         print(df)

#         model = joblib.load("./xgb_regression_model.pkl")

#         result = model.predict(df)
#         return str(result[0])
#     except Exception as e:
#         # Log the error or print it for debugging
#         print("Error:", e)
#         # Return an appropriate error response
#         return "Internal Server Error", 500


@app.route("/chat-search-data", methods=["POST"])
def get_chat_search_data():
    if "pdf1" not in request.files:
        return "Missing files", 400
    pdf1 = request.files["pdf1"]
    pdf1.save("./pdf1.pdf")
    text1 = pdf_to_text(r"C:\Nishkal\Bitcamp 2024\InsuranceHack\pdf1.pdf")
    pdf1_data = read_pdf(text1)

    pdf1_chunks = split_into_sentence_chunks(pdf1_data, max_chunk_length)
    add_embeds(pdf1_chunks, embed_model, index)

    query = "Can you give me a detailed description of this policy, including deductibles and coverages. Also give me information about the provider"
    query += "\n\n\nKeywords: Schedule of Benefits, Coverage, Deductibles, $"
    output = execute_query(query, messages2, chat, vectorstore)

    if "provider" in query.lower():
        output += "\n\n\nProvider Details: \n\n"
        query_2 = """Give me the name of the provider"""
        provider = execute_query(query_2, messages3, chat, vectorstore)
        provider_info = requests.post(
            "http://127.0.0.1:5000/provider_details", json={"provider": provider}
        )
        provider_info = provider_info.json()
        for key, value in provider_info.items():
            output += f"{key}: {value}\n"

    return jsonify(output=output)


@app.route("/single-file", methods=["POST"])
def single_file():
    input_data = request.json
    query = input_data.get("query")
    query += "\n\n\nKeywords: Schedule of Benefits, Coverage, Deductibles, $"
    output = execute_query(query, messages2, chat, vectorstore)

    if "provider" in query.lower():
        output += "\n\n\nProvider Details: \n\n"
        query_2 = """Give me the name of the provider"""
        provider = execute_query(query_2, messages3, chat, vectorstore)
        provider_info = requests.post(
            "http://127.0.0.1:5000/provider_details", json={"provider": provider}
        )
        provider_info = provider_info.json()
        for key, value in provider_info.items():
            output += f"{key}: {value}\n"

    return jsonify(output=output)


@app.route("/upload-policies", methods=["POST"])
def upload_policies():
    if "pdf1" not in request.files or "pdf2" not in request.files:
        return "Missing files", 400

    uploaded_files = request.files.getlist("file")
    print(uploaded_files)

    pdf1 = request.files["pdf1"]
    pdf2 = request.files["pdf2"]
    pdf1.save("./pdf1.pdf")
    pdf2.save("./pdf2.pdf")

    text1 = pdf_to_text(r"C:\Nishkal\Bitcamp 2024\InsuranceHack\pdf1.pdf")
    text2 = pdf_to_text(r"C:\Nishkal\Bitcamp 2024\InsuranceHack\pdf1.pdf")

    pdf1_data = read_pdf(text1)
    pdf2_data = read_pdf(text2)

    pdf1_chunks = split_into_sentence_chunks(pdf1_data, max_chunk_length)
    pdf2_chunks = split_into_sentence_chunks(pdf2_data, max_chunk_length)

    add_embeds(pdf1_chunks, embed_model, index)
    add_embeds(pdf2_chunks, embed_model, index)

    query = "Can you compare these two policies and tell me the differences and similarities between them? Focus on deductibles, coverage, and schedule of benefits"

    query += "\n\n\nKeywords: Schedule of Benefits, Coverage, Deductibles, $"
    output = execute_query(query, messages, chat, vectorstore)
    pc.delete_index(index_name)

    return jsonify(output=output)


@app.route("/compare-policies", methods=["POST"])
def compare_policies():
    input_data = request.json
    query = input_data.get("query")
    query += "\n\n\nKeywords: Schedule of Benefits, Coverage, Deductibles, $"
    output = execute_query(query, messages, chat, vectorstore)
    pc.delete_index(index_name)

    return jsonify(output=output)


@app.route("/clear_database", methods=["GET"])
def clear_database():
    pc.delete_index(index_name)
    create_index(index_name, spec, pc)
    return "Database cleared!", 200


if __name__ == "__main__":
    app.run(debug=False)
