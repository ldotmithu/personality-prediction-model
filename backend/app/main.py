from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Personality Prediction API",
    description="Predict Introvert vs Extrovert"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = joblib.load("backend/model/personality_model.pkl")
scaler = joblib.load("backend/model/scaler.pkl")


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


@app.get("/")
def home():
    return {
        "status": "API Running",
        "message": "Use /predict endpoint for predictions"
    }


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

    
    personality = "Extrovert" if prediction == 1 else "Introvert"

    return {
        "personality": personality,
        "confidence": float(max(probability)),
        "probabilities": {
            "Class_0": float(probability[0]),
            "Class_1": float(probability[1])
        }
    }