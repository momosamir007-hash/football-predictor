# streamlit/components/cards.py
import streamlit as st

def display_match_card(team_a: str, team_b: str, prediction: str, probability: float):
    """
    عرض بطاقة أنيقة لنتيجة التوقع باستخدام HTML مخصص.
    """
    prob_percentage = probability * 100
    
    # تحديد لون البطاقة بناءً على نسبة الثقة (أخضر إذا كانت عالية، برتقالي إذا كانت متوسطة)
    confidence_color = "#2ecc71" if prob_percentage > 60 else "#f39c12"
    
    html_content = f"""
    <div style="
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
        text-align: center;
        border-top: 5px solid {confidence_color};
        margin-bottom: 20px;
    ">
        <h2 style="color: #333; margin-bottom: 10px;">{team_a} 🆚 {team_b}</h2>
        <h3 style="color: #2980b9; margin-bottom: 5px;">التوقع الأرجح: {prediction}</h3>
        <p style="font-size: 18px; color: #555; font-weight: bold;">
            نسبة الثقة: <span style="color: {confidence_color};">{prob_percentage:.1f}%</span>
        </p>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)
