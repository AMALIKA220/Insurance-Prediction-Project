from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user import UserInput
from schema.prediction_response import PredictionResponse
from predict import predict_output, MODEL_VERSION
import pandas as pd



app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Insurance Premium Prediction API'}

@app.get('/health')
def health_check():
    return {
        'status': 'okay',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
        
    }

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi':  data.bmi,
        'age_group': data.age_group,
        'city_tier': data.city_tier,
        'lifestyle_risk': data.lifestyle_risk,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
        }

    try:
        prediction = predict_output(user_input)
        
        return JSONResponse(status_code=200,  content={'responce': prediction})

    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))
        

    