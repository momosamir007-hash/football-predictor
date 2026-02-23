import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_and_save_model(df: pd.DataFrame, model_path: str = "football_model.joblib"):
    """
    تدريب نموذج التعلم الآلي وحفظه للاستخدام في تطبيق Modal.
    """
    if df.empty or 'HomeWin' not in df.columns:
        print("⚠️ البيانات غير صالحة للتدريب.")
        return False

    print("⚙️ جاري تجهيز البيانات للتدريب...")
    
    # 1. تحديد الميزات (Features) المتاحة قبل المباراة والهدف (Target)
    features = ['HomeTeam', 'AwayTeam']
    target = 'HomeWin'
    
    # 2. تحويل أسماء الفرق (نصوص) إلى أعمدة رقمية (One-Hot Encoding)
    # لأن النماذج الرياضية لا تفهم النصوص المباشرة
    X = pd.get_dummies(df[features])
    y = df[target]

    # حفظ أسماء الأعمدة الدقيقة لاستخدامها لاحقاً عند التنبؤ بمباراة جديدة
    model_columns = X.columns.tolist()

    # 3. تقسيم البيانات: 80% لتدريب النموذج، و 20% لاختبار ذكائه
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. بناء وتدريب النموذج (نستخدم Random Forest كبداية قوية)
    print("🧠 جاري تدريب النموذج...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)

    # 5. تقييم أداء النموذج
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"📊 دقة النموذج المبدئية (Accuracy): {accuracy * 100:.2f}%")

    # 6. حفظ النموذج والأعمدة معاً في ملف واحد
    model_data = {
        'model': model,
        'columns': model_columns
    }
    
    # التأكد من وجود مجلد الحفظ
    os.makedirs(os.path.dirname(model_path) if os.path.dirname(model_path) else '.', exist_ok=True)
    joblib.dump(model_data, model_path)
    print(f"✅ تم حفظ النموذج بنجاح في: {model_path}")
    
    return True

# لاختبار الملف محلياً
if __name__ == "__main__":
    import sys
    import os
    # إضافة المسار الجذر للمشروع لاستيراد الملفات السابقة
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data.fetch import fetch_historical_data
    from data.features import create_features
    
    raw_data = fetch_historical_data()
    featured_data = create_features(raw_data)
    train_and_save_model(featured_data)
