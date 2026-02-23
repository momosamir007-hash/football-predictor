import pandas as pd

def fetch_historical_data(league: str = "E0", season: str = "2324") -> pd.DataFrame:
    """
    جلب بيانات المباريات التاريخية لدوري وموسم محددين.
    
    league: رمز الدوري (مثلاً 'E0' للدوري الإنجليزي الممتاز).
    season: الموسم (مثلاً '2324' لموسم 2023-2024).
    """
    # رابط مبدئي لمصدر بيانات مجاني (football-data.co.uk)
    url = f"https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"
    
    try:
        print(f"جاري جلب البيانات من: {url}")
        df = pd.read_csv(url)
        
        # تنظيف أولي للبيانات (إزالة الأعمدة الفارغة إن وجدت)
        df = df.dropna(how='all')
        
        # اختيار الأعمدة الأساسية التي تهمنا مبدئياً
        # Date: التاريخ, HomeTeam: المستضيف, AwayTeam: الضيف
        # FTHG: أهداف المستضيف, FTAG: أهداف الضيف, FTR: النتيجة النهائية
        columns_to_keep = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
        
        # التأكد من وجود الأعمدة المطلوبة
        available_columns = [col for col in columns_to_keep if col in df.columns]
        df = df[available_columns]
        
        print(f"تم جلب {len(df)} مباراة بنجاح.")
        return df

    except Exception as e:
        print(f"حدث خطأ أثناء جلب البيانات: {e}")
        return pd.DataFrame() # إرجاع DataFrame فارغ في حالة الخطأ

# لاختبار الملف محلياً
if __name__ == "__main__":
    data = fetch_historical_data()
    if not data.empty:
        print(data.head())
