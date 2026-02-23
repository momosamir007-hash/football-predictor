import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    تطبيق هندسة الميزات (Feature Engineering) على البيانات الخام.
    """
    if df.empty:
        return df
        
    # إنشاء نسخة لتجنب التعديل على البيانات الأصلية
    processed_df = df.copy()
    
    # 1. تحويل النتيجة (FTR) إلى أرقام (Target Variable)
    # H = فوز المستضيف (Home), D = تعادل (Draw), A = فوز الضيف (Away)
    # سنقوم بتبسيطها: 1 إذا فاز المستضيف، 0 إذا لم يفز (تعادل أو خسر)
    if 'FTR' in processed_df.columns:
        processed_df['HomeWin'] = (processed_df['FTR'] == 'H').astype(int)
    
    # 2. إضافة ميزات بسيطة كمثال: فارق الأهداف في المباراة
    if 'FTHG' in processed_df.columns and 'FTAG' in processed_df.columns:
        processed_df['GoalDifference'] = processed_df['FTHG'] - processed_df['FTAG']
        
    # ملاحظة: في بيئة إنتاج حقيقية، ستقوم هنا بحساب ميزات معقدة مثل:
    # - متوسط الأهداف المسجلة/المستقبلة لكل فريق في آخر 5 مباريات (Rolling Averages).
    # - عدد أيام الراحة منذ آخر مباراة.
    # - تاريخ المواجهات المباشرة (Head-to-Head).
    # لتجنب تعقيد الكود الآن، سنكتفي بالأساسيات لتجهيز خط الأنابيب.
    
    # تحويل التواريخ إذا لزم الأمر
    if 'Date' in processed_df.columns:
        # بعض المصادر تستخدم صيغ تواريخ مختلفة، نقوم بتوحيدها
        processed_df['Date'] = pd.to_datetime(processed_df['Date'], dayfirst=True, errors='coerce')

    return processed_df

# لاختبار الملف محلياً
if __name__ == "__main__":
    from fetch import fetch_historical_data
    raw_data = fetch_historical_data()
    featured_data = create_features(raw_data)
    print("البيانات بعد هندسة الميزات:")
    print(featured_data.head())
