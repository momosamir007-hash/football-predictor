import requests
import streamlit as st

# الرابط السحابي الخاص بك على سحابة Modal (تم تحديثه ليعمل مباشرة)
MODAL_API_URL = "https://momosamir007--football-predictor-fastapi-app.modal.run"

def get_match_prediction(team_a: str, team_b: str):
    """
    يرسل طلب لـ Modal لجلب توقع نتيجة المباراة بين فريقين
    """
    url = f"{MODAL_API_URL}/predict"
    payload = {
        "team_a": team_a,
        "team_b": team_b
    }
    
    try:
        # إرسال البيانات عبر POST
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ خطأ في الاتصال بالخادم عند جلب التوقع: {e}")
        return None

def get_upcoming_matches():
    """
    يجلب قائمة المباريات القادمة (المجدولة) من خادم Modal
    """
    url = f"{MODAL_API_URL}/upcoming"
    
    try:
        # جلب البيانات عبر GET
        response = requests.get(url)
        response.raise_for_status()
        # استخراج قائمة المباريات من الرد
        return response.json().get("matches", [])
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ خطأ في الاتصال بالخادم عند جلب المباريات القادمة: {e}")
        return []
