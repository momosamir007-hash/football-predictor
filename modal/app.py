import modal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.fetch import fetch_football_data_api, fetch_upcoming_matches, fetch_team_stats
from data.features import create_features
from models.train import train_and_save_model
from utils.helpers import load_model, predict_single_match

app = modal.App("football-predictor")

image = (
    modal.Image.debian_slim()
    .pip_install("fastapi", "pydantic", "pandas", "scikit-learn", "xgboost", "requests", "python-dotenv", "joblib")
    .add_local_dir(os.path.dirname(__file__), remote_path="/root")
)

web_app = FastAPI(title="Football Predictor API")

class MatchRequest(BaseModel):
    team_a: str
    team_b: str

@web_app.get("/upcoming")
def get_upcoming():
    matches = fetch_upcoming_matches("PL")
    return {"status": "success", "matches": matches}

@web_app.get("/stats")
def get_stats():
    stats = fetch_team_stats("PL")
    return {"status": "success", "stats": stats}

@web_app.post("/predict")
def predict_match(request: MatchRequest):
    model_data = load_model()
    
    if not model_data:
        print("🧠 جاري تدريب النموذج لأول مرة...")
        df = fetch_football_data_api("PL")
        if df.empty:
            raise HTTPException(status_code=500, detail="فشل جلب البيانات للتدريب.")
        
        df_features = create_features(df)
        train_and_save_model(df_features)
        model_data = load_model()
        
    result = predict_single_match(request.team_a, request.team_b, model_data)
    result["status"] = "success"
    return result

@app.function(
    image=image, 
    secrets=[modal.Secret.from_name("football-api-secret")]
)
@modal.asgi_app()
def fastapi_app():
    return web_app
