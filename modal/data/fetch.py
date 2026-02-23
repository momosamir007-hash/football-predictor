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
