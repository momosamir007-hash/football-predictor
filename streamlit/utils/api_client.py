import requests
import streamlit as st

MODAL_API_URL = "https://momosamir007--football-predictor-fastapi-app.modal.run"

def get_match_prediction(team_a: str, team_b: str):
    """جلب توقع النتيجة من الخادم"""
    url = f"{MODAL_API_URL}/predict"
    payload = {"team_a": team_a, "team_b": team_b}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ خطأ في الاتصال بالخادم عند جلب التوقع: {e}")
        return None

def get_upcoming_matches():
    """جلب قائمة المباريات القادمة من الخادم"""
    url = f"{MODAL_API_URL}/upcoming"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("matches", [])
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ خطأ في الاتصال بالخادم عند جلب المباريات: {e}")
        return []

def get_team_stats():
    """جلب إحصائيات الفرق الحقيقية من الخادم"""
    url = f"{MODAL_API_URL}/stats"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("stats", [])
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ خطأ في الاتصال بالخادم عند جلب الإحصائيات: {e}")
        return []
