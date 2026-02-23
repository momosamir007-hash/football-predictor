import modal
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# إضافة المسار الحالي لضمان عمل الاستيرادات الداخلية في Modal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 1. تعريف تطبيق Modal
app = modal.App("football-predictor")

# 2. إعداد بيئة التشغيل (الصورة) مع كافة المكتبات المطلوبة
image = (
    modal.Image.debian_slim()
    .pip_install(
        "fastapi", 
        "pydantic", 
        "pandas", 
        "scikit-learn", 
        "xgboost", 
        "requests", 
        "python-dotenv", 
        "joblib"
    )
)

# 3. تهيئة خادم FastAPI
web_app = FastAPI(title="Football Predictor API", version="1.0")

# نموذج البيانات المستقبلة من واجهة Streamlit
class MatchRequest(BaseModel):
    team_a: str
    team_b: str

# 4. تعريف نقطة النهاية (Endpoint) للتنبؤ
@web_app.post("/predict")
def predict_match(request: MatchRequest):
    """
    مستقبلاً: سيتم استيراد دالة 'predict_single_match' من 'utils.helpers' هنا.
    حالياً نرجع نتيجة مبدئية للتأكد من نجاح الاتصال.
    """
    return {
        "status": "success",
        "match": f"{request.team_a} vs {request.team_b}",
        "prediction": f"فوز {request.team_a}",
        "win_probability": 0.65 # سيتم استبدالها بنتيجة النموذج الحقيقية
    }

# 5. ربط FastAPI بـ Modal وتحديد نقطة النهاية للإنترنت
# لاحظ تمرير secrets ليتمكن السكريبت الداخلي من قراءة مفتاح الـ API
@app.function(
    image=image, 
    secrets=[modal.Secret.from_name("football-api-secret")]
)
@modal.asgi_app()
def fastapi_app():
    return web_app
