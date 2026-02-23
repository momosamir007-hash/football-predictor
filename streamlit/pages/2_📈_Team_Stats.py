import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# إضافة المسار الصحيح لاستدعاء ملفات المشروع
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.api_client import get_team_stats

st.set_page_config(page_title="إحصائيات الفرق", page_icon="📈", layout="wide")

st.title("📈 تحليل وإحصائيات الفرق الحقيقية")
st.markdown("استكشف أداء فرق الدوري الإنجليزي لهذا الموسم بشكل مباشر ⚽")

# جلب البيانات الحقيقية من الخادم
with st.spinner("جاري جلب الإحصائيات الحقيقية من الخادم السحابي..."):
    raw_stats = get_team_stats()

if not raw_stats:
    st.warning("⚠️ تعذر جلب الإحصائيات. تأكد من أن خادم Modal يعمل بشكل صحيح.")
else:
    df = pd.DataFrame(raw_stats)

    tab1, tab2 = st.tabs(["📊 نظرة عامة على فريق", "⚔️ مقارنة بين فريقين"])

    # ================= التبويب الأول =================
    with tab1:
        st.subheader("🔍 تفاصيل أداء الفريق")
        selected_team = st.selectbox("اختر فريقاً لعرض إحصائياته:", df['الفريق'].tolist(), key="single_team")
        team_data = df[df['الفريق'] == selected_team].iloc[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("⚽ الأهداف المسجلة", team_data['الأهداف المسجلة'])
        col2.metric("🛡️ الأهداف المستقبلة", team_data['الأهداف المستقبلة'])
        col3.metric("🔥 نسبة الفوز", f"{team_data['نسبة الفوز (%)']}%")
        col4.metric("⭐ النقاط الإجمالية", team_data['النقاط'])

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_chart1, col_chart2 = st.columns([1, 2])
        
        with col_chart1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = team_data['نسبة الفوز (%)'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "مؤشر القوة (نسبة الفوز)"},
                gauge = {'axis': {'range': [0, 100]},
                         'bar': {'color': "#E63946"},
                         'steps': [
                             {'range': [0, 40], 'color': "#F1FAEE"},
                             {'range': [40, 70], 'color': "#A8DADC"}]
                         }
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with col_chart2:
            labels = ['أهداف مسجلة', 'أهداف مستقبلة']
            values = [team_data['الأهداف المسجلة'], team_data['الأهداف المستقبلة']]
            fig_pie = px.pie(values=values, names=labels, hole=0.4, title="تحليل الهجوم والدفاع",
                             color_discrete_sequence=['#2A9D8F', '#E76F51'])
            st.plotly_chart(fig_pie, use_container_width=True)

    # ================= التبويب الثاني =================
    with tab2:
        st.subheader("⚔️ مواجهة الإحصائيات (Head-to-Head)")
        col_a, col_b = st.columns(2)
        with col_a:
            team1 = st.selectbox("الفريق الأول:", df['الفريق'].tolist(), index=0, key="team1")
        with col_b:
            team2 = st.selectbox("الفريق الثاني:", df['الفريق'].tolist(), index=1 if len(df) > 1 else 0, key="team2")

        if team1 and team2:
            df_compare = df[df['الفريق'].isin([team1, team2])]
            
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                categories = ['الأهداف المسجلة', 'نسبة الفوز (%)', 'النقاط']
                fig_radar = go.Figure()
                
                t1_stats = df[df['الفريق'] == team1].iloc[0]
                fig_radar.add_trace(go.Scatterpolar(
                    r=[t1_stats['الأهداف المسجلة'], t1_stats['نسبة الفوز (%)'], t1_stats['النقاط']], 
                    theta=categories, fill='toself', name=team1
                ))
                
                t2_stats = df[df['الفريق'] == team2].iloc[0]
                fig_radar.add_trace(go.Scatterpolar(
                    r=[t2_stats['الأهداف المسجلة'], t2_stats['نسبة الفوز (%)'], t2_stats['النقاط']],
                    theta=categories, fill='toself', name=team2
                ))
                
                max_val = max(df_compare['النقاط'].max(), df_compare['الأهداف المسجلة'].max())
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max_val + 10])), showlegend=True, title="مقارنة القوة الشاملة")
                st.plotly_chart(fig_radar, use_container_width=True)
                
            with col_c2:
                fig_bar = px.bar(
                    df_compare, 
                    x='الفريق', 
                    y=['الأهداف المسجلة', 'الأهداف المستقبلة'],
                    barmode='group',
                    title="مقارنة القوة الهجومية والصلابة الدفاعية",
                    labels={'value': 'عدد الأهداف', 'variable': 'النوع'},
                    color_discrete_map={'الأهداف المسجلة': '#2E8B57', 'الأهداف المستقبلة': '#B22222'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
