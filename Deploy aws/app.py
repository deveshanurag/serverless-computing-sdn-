from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.responses import JSONResponse
from mangum import Mangum

# Load model and scaler once
model = joblib.load('rf_model.pkl')
scaler = joblib.load('scaler.pkl')

# Initialize FastAPI
app = FastAPI()
handler = Mangum(app)  # Lambda entry point

# Define expected input format using Pydantic
class InputData(BaseModel):
    byteperflow: float
    tot_kbps: float
    rx_kbps: float
    flows: int
    bytecount: float
    tot_dur: float
    Protocol: str

def preprocess_input(input_data: InputData):
    """
    Preprocess the input data for prediction.
    """
    protocol = input_data.Protocol.upper()

    feature_vector = [
        input_data.byteperflow,
        input_data.tot_kbps,
        input_data.rx_kbps,
        input_data.flows,
        input_data.bytecount,
        input_data.tot_dur,
        1 if protocol == 'ICMP' else 0,
        1 if protocol == 'TCP' else 0,
        1 if protocol == 'UDP' else 0
    ]

    feature_vector = np.array(feature_vector).reshape(1, -1)
    return scaler.transform(feature_vector)

@app.post("/predict")
def predict_diabetes(data: InputData):
    try:
        processed_input = preprocess_input(data)
        prediction = model.predict(processed_input)
        return JSONResponse(content={"prediction": prediction.tolist()})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
