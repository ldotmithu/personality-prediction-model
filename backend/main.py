from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load models
model = joblib.load("model/personality_model.pkl")
scaler = joblib.load("model/scaler.pkl")


stage_fear_mapping = {"No": 0, "Yes": 1}
drained_mapping = {"No": 0, "Yes": 1}

class PersonalData(BaseModel):
    Time_spent_Alone: float
    Stage_fear: str 
    Social_event_attendance: float
    Going_outside: float
    Drained_after_socializing: str 
    Friends_circle_size: float
    Post_frequency: float

app = FastAPI(title="Personality Prediction API", 
              description="Predict if a person is Extrovert or Introvert")

@app.get("/")
def home():
    return {"status": "Application Running", "message": "Use POST /predict/ to make predictions"}

@app.post("/predict/")
def predict(personal_data: PersonalData):
    stage_fear_encoded = stage_fear_mapping.get(personal_data.Stage_fear, 0)
    drained_encoded = drained_mapping.get(personal_data.Drained_after_socializing, 0)
    
    features = np.array([[
        personal_data.Time_spent_Alone,
        stage_fear_encoded,
        personal_data.Social_event_attendance,
        personal_data.Going_outside,
        drained_encoded,
        personal_data.Friends_circle_size,
        personal_data.Post_frequency
    ]])
   
    features_scaled = scaler.transform(features)
    
    
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]
    
   
    personality = "Extrovert" if prediction == 0 else "Introvert"
    
    return {
        "personality": personality,
        "confidence": float(max(probability)),
        "probabilities": {
            "Extrovert": float(probability[0]),
            "Introvert": float(probability[1])
        },
        "input_data": personal_data.dict()
    }