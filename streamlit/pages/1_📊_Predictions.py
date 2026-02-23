import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.api_client import get_match_prediction, get_upcoming_matches
from components.charts import plot_win_probability
from components.cards import display_match_card

st.set_page_config(page_title="توقعات المباريات", page_icon="📊", layout="wide")

st.title("📊 توقع نتيجة المباريات")
st.markdown("اختر مباراة من المباريات القادمة، وسيقوم الذكاء الاصطناعي بتحليلها وتوقع نتيجتها.")

# جلب المباريات القادمة
with st.spinner("جاري جلب مباريات الأسبوع..."):
    upcoming = get_upcoming_matches()

if upcoming:
    # إنشاء قائمة بالأسماء لتسهيل الاختيار
    match_options = [f"{m['homeTeam']} vs {m['awayTeam']}" for m in upcoming]
    selected_match_str = st.selectbox("🎯 اختر المباراة القادمة:", match_options)
    
    # فصل اسم الفريقين من الاختيار
    team_a, team_b = selected_match_str.split(" vs ")
else:
    st.warning("لا توجد مباريات قادمة حالياً، أو حدث خطأ في جلبها. يمكنك كتابة الأسماء يدوياً.")
    col1, col2 = st.columns(2)
    with col1: team_a = st.text_input("الفريق المستضيف")
    with col2: team_b = st.text_input("الفريق الضيف")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("احسب التوقع ⚽", use_container_width=True, type="primary"):
    if team_a and team_b:
        with st.spinner("🧠 جاري تدريب النموذج وتحليل البيانات التاريخية... (قد يستغرق 10 ثوانٍ في المرة الأولى)"):
            result = get_match_prediction(team_a, team_b)
            
            if result and result.get("status") == "success":
                st.balloons()
                display_match_card(team_a, team_b, result["prediction"], result["win_probability"])
                st.plotly_chart(plot_win_probability(team_a, team_b, result["win_probability"]), use_container_width=True)
            else:
                st.error("⚠️ فشل في جلب التوقع من الخادم.")
