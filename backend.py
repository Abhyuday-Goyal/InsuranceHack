from flask import Flask, request
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import joblib

app = Flask(__name__)

@app.route('/predict-premium', methods=['POST'])
def predict_premium():
    input_data = request.get_json()
    df = pd.DataFrame(input_data)
    print(df)
    model = joblib.load('xgb_regression_model.pkl')
    print(df.shape)
    result = model.predict(df)
    return str(result[0])

if __name__ == '__main__':
    app.run(debug = True)