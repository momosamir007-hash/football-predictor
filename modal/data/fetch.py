import os
import requests
import pandas as pd
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env (للاختبار المحلي فقط)
load_dotenv()

def fetch_football_data_api(competition_code: str = "PL") -> pd.DataFrame:
    """
    جلب بيانات المباريات باستخدام football-data.org API
    PL = الدوري الإنجليزي الممتاز (Premier League)
    PD = الدوري الإسباني (Primera Division)
    """
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    
    if not api_key:
        print("⚠️ خطأ: لم يتم العثور على FOOTBALL_DATA_API_KEY")
        return pd.DataFrame()

    # رابط جلب مباريات بطولة محددة
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/matches"
    
    # تمرير مفتاح الـ API في الترويسة (Headers) كما يطلب الموقع
    headers = {
        "X-Auth-Token": api_key
    }

    try:
        print(f"جاري جلب البيانات من API لدوري: {competition_code}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status() # التأكد من عدم وجود خطأ في الاتصال
        
        data = response.json()
        matches = data.get("matches", [])
        
        if not matches:
            print("لم يتم العثور على مباريات.")
            return pd.DataFrame()

        # استخراج البيانات المهمة فقط من الاستجابة المعقدة
        processed_matches = []
        for match in matches:
            # نتجاهل المباريات التي لم تُلعب بعد (التي لا تحتوي على نتيجة)
            if match["status"] != "FINISHED":
                continue
                
            match_data = {
                "Date": match["utcDate"],
                "HomeTeam": match["homeTeam"]["name"],
                "AwayTeam": match["awayTeam"]["name"],
                "FTHG": match["score"]["fullTime"]["home"], # أهداف المستضيف
                "FTAG": match["score"]["fullTime"]["away"], # أهداف الضيف
                "FTR": match["score"]["winner"] # النتيجة النهائية (HOME_TEAM, AWAY_TEAM, DRAW)
            }
            processed_matches.append(match_data)
            
        df = pd.DataFrame(processed_matches)
        
        # توحيد صيغة النتيجة (FTR) لتطابق الكود القديم (H, A, D)
        winner_map = {"HOME_TEAM": "H", "AWAY_TEAM": "A", "DRAW": "D"}
        df["FTR"] = df["FTR"].map(winner_map)
        
        print(f"✅ تم جلب {len(df)} مباراة ملعوبة بنجاح.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ حدث خطأ أثناء الاتصال بالـ API: {e}")
        return pd.DataFrame()

# لاختبار الملف محلياً
if __name__ == "__main__":
    df = fetch_football_data_api("PL")
    if not df.empty:
        print(df.head())
