import modal
from fastapi import FastAPI
from pydantic import BaseModel

# تعريف تطبيق Modal
app = modal.App("football-predictor")

# إعداد بيئة التشغيل (الصورة) مع المتطلبات
image = modal.Image.debian_slim().pip_install_from_requirements("requirements.txt")

# تهيئة FastAPI
web_app = FastAPI(title="Football Predictor API")

# نموذج البيانات المستقبلة من Streamlit
class MatchRequest(BaseModel):
    team_a: str
    team_b: str
    # يمكننا إضافة المزيد من الميزات لاحقاً مثل: team_a_form, team_b_injuries

@web_app.post("/predict")
def predict_match(request: MatchRequest):
    """
    هذه الدالة ستقوم لاحقاً باستدعاء نموذج التعلم الآلي المدرب.
    حالياً نضع بيانات وهمية (Mock Data) لاختبار الاتصال.
    """
    # TODO: استدعاء نموذج XGBoost/Scikit-learn هنا
    
    return {
        "status": "success",
        "match": f"{request.team_a} vs {request.team_b}",
        "prediction": f"فوز {request.team_a}",
        "win_probability": 0.65
    }

# ربط FastAPI بـ Modal وتحديد نقطة النهاية
@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    return web_app
