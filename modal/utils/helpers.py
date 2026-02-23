import pandas as pd
import joblib
import os

def load_model():
    """دالة ذكية للبحث عن النموذج في كل المسارات المحتملة"""
    possible_paths = [
        "football_model.joblib",
        "/root/football_model.joblib",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "football_model.joblib"),
        os.path.join(os.path.dirname(__file__), "football_model.joblib"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'football_model.joblib')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ تم تحميل النموذج بنجاح من: {path}")
            return joblib.load(path)
            
    print("❌ لم يتم العثور على ملف النموذج!")
    return None

def predict_single_match(team_a: str, team_b: str, model_data: dict) -> dict:
    """
    استقبال فريقين وتوقع نتيجة المباراة باستخدام النموذج المحفوظ.
    """
    # حماية إضافية: إذا لم يجد النموذج لأي سبب، يعيد رسالة خطأ بدلاً من إيقاف الخادم
    if not model_data:
        return {
            "match": f"{team_a} vs {team_b}",
            "prediction": "جاري تجهيز الذكاء الاصطناعي... حاول مرة أخرى بعد قليل",
            "win_probability": 0.0
        }

    model = model_data['model']
    model_columns = model_data['columns']
    
    # إنشاء DataFrame ببيانات المباراة المطلوبة
    input_data = pd.DataFrame([{'HomeTeam': team_a, 'AwayTeam': team_b}])
    
    # تحويل البيانات بنفس طريقة التدريب (One-Hot Encoding)
    input_encoded = pd.get_dummies(input_data)
    
    # التأكد من أن المدخلات تحتوي على نفس أعمدة التدريب بالضبط
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
