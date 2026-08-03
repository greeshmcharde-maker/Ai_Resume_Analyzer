import streamlit as st

def glass_card(icon, title, value, subtitle=""):

    st.markdown(f"""
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
    """, unsafe_allow_html=True)
