# streamlit/pages/1_📊_Predictions.py
import streamlit as st
import sys
import os

# إضافة المسار الجذر للسماح باستيراد الملفات
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from streamlit.utils.api_client import get_match_prediction
from streamlit.components.charts import plot_win_probability
from streamlit.components.cards import display_match_card

# إعدادات الصفحة
st.set_page_config(page_title="توقعات المباريات", page_icon="📊", layout="wide")

st.title("📊 توقع نتيجة مباراة محددة")
st.markdown("أدخل أسماء الفرق وسيتم إرسال الطلب إلى **Modal** لتحليل البيانات باستخدام نموذج التعلم الآلي وإرجاع النتيجة.")

# واجهة إدخال البيانات
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        team_a = st.text_input("الفريق المستضيف (Home)", placeholder="مثال: Arsenal")
    with col2:
        team_b = st.text_input("الفريق الضيف (Away)", placeholder="مثال: Chelsea")

st.markdown("<br>", unsafe_allow_html=True) # مسافة فارغة

# زر التشغيل
if st.button("احسب التوقع ⚽", use_container_width=True, type="primary"):
    if team_a and team_b:
        with st.spinner("جاري الاتصال بخوادم Modal لتحليل البيانات واستخراج التوقع..."):
            # استدعاء الـ API الخاص بـ Modal
            result = get_match_prediction(team_a, team_b)
            
            if result and result.get("status") != "error":
                st.balloons() # تأثير بصري عند النجاح
                
                # عرض النتيجة والرسوم البيانية
                display_match_card(
                    team_a=team_a, 
                    team_b=team_b, 
                    prediction=result["prediction"], 
                    probability=result["win_probability"]
                )
                
                # عرض الرسم البياني الدائري
                st.plotly_chart(
                    plot_win_probability(team_a, team_b, result["win_probability"]), 
                    use_container_width=True
                )
            else:
                st.error("⚠️ فشل في جلب التوقع. تأكد من تشغيل Modal وأن الرابط (URL) في api_client.py صحيح.")
    else:
        st.warning("يرجى إدخال اسم الفريق المستضيف والضيف أولاً.")
