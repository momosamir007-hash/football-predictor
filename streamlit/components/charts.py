# streamlit/components/charts.py
import plotly.graph_objects as go
import sys
import os

# لاستيراد الثوابت
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from shared.constants import COLORS

def plot_win_probability(team_a: str, team_b: str, prob_a: float):
    """
    رسم بياني دائري يوضح احتمالية فوز المستضيف مقابل الضيف.
    """
    prob_b = 1.0 - prob_a
    
    labels = [f"فوز {team_a}", f"تعادل / فوز {team_b}"]
    values = [prob_a, prob_b]
    
    # استخدام ألوان مميزة
    marker_colors = [COLORS["primary"], COLORS["secondary"]]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.5, # تحويلها إلى شكل دائرة مفرغة (Donut)
        marker_colors=marker_colors,
        textinfo='label+percent',
        hoverinfo='label+percent'
    )])
    
    fig.update_layout(
        title_text="نسبة احتمالية النتيجة",
        title_x=0.5, # توسيط العنوان
        annotations=[dict(text='⚽', x=0.5, y=0.5, font_size=40, showarrow=False)],
        margin=dict(t=50, b=0, l=0, r=0)
    )
    
    return fig
