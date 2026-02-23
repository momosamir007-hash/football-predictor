import streamlit as st
from utils.api_client import get_match_prediction

# إعدادات الصفحة
st.set_page_config(
    page_title="محلل كرة القدم الذكي",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚽ محلل كرة القدم الذكي")
st.markdown("مرحباً بك في نظام التنبؤ بنتائج المباريات المعتمد على التعلم الآلي.")

# تصميم الواجهة كعناصر مبسطة للاختبار الأولي
st.subheader("توقع نتيجة مباراة سريعة")

col1, col2 = st.columns(2)

with col1:
    team_a = st.text_input("الفريق الأول (المستضيف)", "ريال مدريد")
with col2:
    team_b = st.text_input("الفريق الثاني (الضيف)", "برشلونة")

if st.button("توقع النتيجة 🚀", use_container_width=True):
    with st.spinner("جاري تحليل البيانات عبر Modal..."):
        result = get_match_prediction(team_a, team_b)
        
        if result and result.get("status") == "success":
            st.success("تم جلب التوقع بنجاح!")
            
            # عرض النتيجة في بطاقات جميلة
            res_col1, res_col2 = st.columns(2)
            res_col1.metric("التوقع الأرجح", result["prediction"])
            res_col2.metric("نسبة الفوز", f"{result['win_probability'] * 100}%")
