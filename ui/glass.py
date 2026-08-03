import streamlit as st
from textwrap import dedent

def glass_card(icon, title, value, subtitle=""):

    html = dedent(f"""
<div class="glass-card">

    <div class="glass-icon">
        {icon}
    </div>

    <div class="glass-title">
        {title}
    </div>

    <div class="glass-value">
        {value}
    </div>

    <div class="glass-subtitle">
        {subtitle}
    </div>

</div>
""")

    st.markdown(html, unsafe_allow_html=True)
