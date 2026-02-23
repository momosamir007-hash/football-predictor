import pandas as pd
import joblib
import os

# مسار النموذج المحفوظ
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'football_model.joblib')

def load_model():
    """تحميل النموذج المُدرب في الذاكرة"""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def predict_single_match(team_a: str, team_b: str, model_data: dict) -> dict:
    """
    استقبال فريقين وتوقع نتيجة المباراة باستخدام النموذج المحفوظ.
    """
    model = model_data['model']
    model_columns = model_data['columns']
    
    # إنشاء DataFrame ببيانات المباراة المطلوبة
    input_data = pd.DataFrame([{'HomeTeam': team_a, 'AwayTeam': team_b}])
    
    # تحويل البيانات بنفس طريقة التدريب (One-Hot Encoding)
    input_encoded = pd.get_dummies(input_data)
    
    # التأكد من أن المدخلات تحتوي على نفس أعمدة التدريب بالضبط
    # إذا كان هناك فريق جديد، سيتم ملء عموده بـ 0 (False)
    input_aligned = input_encoded.reindex(columns=model_columns, fill_value=0)
    
    # التنبؤ بالنتيجة (0 = تعادل/فوز الضيف، 1 = فوز المستضيف)
    prediction = model.predict(input_aligned)[0]
    
    # جلب احتمالية الفوز (نسبة الثقة في التوقع)
    probabilities = model.predict_proba(input_aligned)[0]
    win_prob = probabilities[1] if prediction == 1 else probabilities[0]
    
    result_text = f"فوز {team_a} (المستضيف)" if prediction == 1 else f"فوز {team_b} أو تعادل"
    
    return {
        "match": f"{team_a} vs {team_b}",
        "prediction": result_text,
        "win_probability": round(float(win_prob), 2)
    }
