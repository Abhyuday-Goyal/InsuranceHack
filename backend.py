from flask import Flask, request
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import joblib
from pdftext import pdf_to_text
from main import read_pdf, split_into_chunks, add_embeds, process_query

app = Flask(__name__)

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
    
    pdf1 = request.files['pdf1']
    pdf2 = request.files['pdf2']

    pdf1.save('/tmp/pdf1.pdf')
    pdf2.save('/tmp/pdf2.pdf')

    text1 = pdf_to_text('/tmp/pdf1.pdf')
    text2 = pdf_to_text('/tmp/pdf2.pdf')

    pdf1_data = read_pdf(text1)
    pdf2_data = read_pdf(text2)

    pdf1_chunks = split_into_chunks(pdf1_data)
    pdf2_chunks = split_into_chunks(pdf2_data)

    add_embeds(pdf1_chunks)
    add_embeds(pdf2_chunks)

    return "Policies processed!", 200

@app.route('/compare-policies', methods=['POST'])
def compare_policies():
    input_data = request.get_json()
    query = input_data['query']

    result = process_query(query)

    print(result)
    return result

if __name__ == '__main__':
    app.run(debug = True)