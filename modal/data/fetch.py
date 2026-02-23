import os
import requests
import pandas as pd
from dotenv import load_dotenv

# تحميل المتغيرات
load_dotenv()

def fetch_football_data_api(competition_code: str = "PL") -> pd.DataFrame:
    """جلب بيانات المباريات التاريخية للتدريب"""
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if not api_key: return pd.DataFrame()

    url = f"https://api.football-data.org/v4/competitions/{competition_code}/matches"
    headers = {"X-Auth-Token": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        matches = response.json().get("matches", [])
        
        processed_matches = []
        for match in matches:
            if match["status"] != "FINISHED": continue
            match_data = {
                "Date": match["utcDate"],
                "HomeTeam": match["homeTeam"]["name"],
                "AwayTeam": match["awayTeam"]["name"],
                "FTHG": match["score"]["fullTime"]["home"],
                "FTAG": match["score"]["fullTime"]["away"],
                "FTR": match["score"]["winner"]
            }
            processed_matches.append(match_data)
            
        df = pd.DataFrame(processed_matches)
        winner_map = {"HOME_TEAM": "H", "AWAY_TEAM": "A", "DRAW": "D"}
        df["FTR"] = df["FTR"].map(winner_map)
        return df
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return pd.DataFrame()

def fetch_upcoming_matches(competition_code: str = "PL") -> list:
    """جلب المباريات القادمة التي لم تُلعب بعد"""
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if not api_key: return []
    
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/matches?status=SCHEDULED"
    headers = {"X-Auth-Token": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        matches = response.json().get("matches", [])
        
        upcoming = []
        for match in matches[:10]: # جلب أقرب 10 مباريات
            upcoming.append({
                "homeTeam": match["homeTeam"]["name"],
                "awayTeam": match["awayTeam"]["name"],
                "date": match["utcDate"]
            })
        return upcoming
    except Exception as e:
        print(f"❌ خطأ في جلب المباريات القادمة: {e}")
        return []

def fetch_team_stats(competition_code: str = "PL") -> list:
    """جلب إحصائيات الفرق (ترتيب الدوري) الحقيقية"""
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if not api_key: return []
    
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/standings"
    headers = {"X-Auth-Token": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        standings = response.json().get("standings", [])
        
        if not standings: return []
        
        table = standings[0].get("table", [])
        stats = []
        for team in table:
            played = team["playedGames"]
            won = team["won"]
            win_pct = round((won / played * 100), 1) if played > 0 else 0
            
            stats.append({
                "الفريق": team["team"]["name"],
                "الأهداف المسجلة": team["goalsFor"],
                "الأهداف المستقبلة": team["goalsAgainst"],
                "النقاط": team["points"],
                "نسبة الفوز (%)": win_pct
            })
        return stats
    except Exception as e:
        print(f"❌ خطأ في جلب الإحصائيات: {e}")
        return []
