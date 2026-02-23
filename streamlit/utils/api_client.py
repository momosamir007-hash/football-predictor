import requests
import streamlit as st

# سنقوم بتحديث هذا الرابط بعد نشر Modal
# مثال: "https://YOUR_WORKSPACE_NAME--football-predictor-fastapi-app.modal.run"
MODAL_API_URL = "https://momosamir007--football-predictor-fastapi-app.modal.run" # استخدم الرابط الفعلي بعد النشر

def get_match_prediction(team_a: str, team_b: str):
    """
    يرسل طلب لـ Modal لجلب توقع المباراة
    """
    url = f"{MODAL_API_URL}/predict"
    payload = {
        "team_a": team_a,
        "team_b": team_b
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"خطأ في الاتصال بالخادم: {e}")
        return None
