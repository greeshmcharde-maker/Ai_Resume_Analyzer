import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


from modules.pdf_reader import extract_pdf_text
from modules.docx_reader import extract_docx_text
from modules.resume_parser import (
    extract_email,
    extract_phone,
    extract_skills
)
from modules.ats import calculate_ats_score
from modules.resume_score import calculate_resume_score
from modules.ai_feedback import get_ai_feedback   
from modules.skill_match import (
    extract_job_skills,
    compare_skills
)
from modules.pdf_report import create_pdf

ai_feedback = "AI feedback not generated."

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.title("AI Resume Analyzer")

    st.markdown("---")

    st.success("✔ Resume Parsing")

    st.success("✔ ATS Analysis")

    st.success("✔ Skill Matching")

    st.success("✔ Resume Score")

    st.success("✔ AI Suggestions")

    st.success("✔ PDF Report")

    st.markdown("---")

    st.info("Version 2.0")

st.markdown("""
<div style="
background:rgba(255,255,255,0.08);
backdrop-filter:blur(25px);
-webkit-backdrop-filter:blur(25px);
border:1px solid rgba(255,255,255,0.15);
border-radius:30px;
padding:40px;
margin-bottom:35px;
text-align:center;
box-shadow:0 15px 40px rgba(0,0,0,.25);
">

<h1 style="
color:#00D4FF;
font-size:60px;
margin-bottom:10px;
">

🚀 AI Resume Analyzer

</h1>

<p style="
font-size:22px;
color:#D1D5DB;
margin-bottom:20px;
">

Smart ATS Resume Evaluation Platform

</p>

<div style="
display:flex;
justify-content:center;
gap:12px;
flex-wrap:wrap;
">

<span style="
padding:10px 18px;
border-radius:25px;
background:rgba(255,255,255,.08);
">
📄 Resume Parsing
</span>

<span style="
padding:10px 18px;
border-radius:25px;
background:rgba(255,255,255,.08);
">
🎯 ATS Analysis
</span>

<span style="
padding:10px 18px;
border-radius:25px;
background:rgba(255,255,255,.08);
">
🤖 AI Feedback
</span>

<span style="
padding:10px 18px;
border-radius:25px;
background:rgba(255,255,255,.08);
">
📊 Skill Matching
</span>

</div>

</div>
""", unsafe_allow_html=True)

st.info(
    "👋 Welcome! Upload your resume and paste a job description to receive an ATS score, skill analysis, and personalized feedback."
)

left, right = st.columns([1,1], gap="large")

with left:

    resume = st.file_uploader(
        "📤 Upload Resume",
        type=["pdf", "docx"]
    )

with right:

    job_description = st.text_area(
        "📋 Job Description",
        height=220
    )

if resume is not None:

    if resume.type == "application/pdf":
        resume_text = extract_pdf_text(resume)

    elif resume.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_docx_text(resume)

    else:
        st.error("Unsupported file format.")
        st.stop()

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)

    resume_score = calculate_resume_score(
        email,
        phone,
        skills
    )

    ats_score = None

    job_skills = []
    matched_skills = []
    missing_skills = []

    if job_description.strip():

        ats_score = calculate_ats_score(
        resume_text,
        job_description
        )

        job_skills = extract_job_skills(job_description)

        matched_skills, missing_skills = compare_skills(
        skills,
        job_skills
        )

    word_count = len(resume_text.split())
    character_count = len(resume_text)
    page_count = max(1, resume_text.count("\f") + 1)

    st.success("Resume Uploaded Successfully!")

    st.subheader("📊 Dashboard")

    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.metric(
            label="📄 Resume Score",
            value=f"{resume_score}/100"
        )
    
    with row1_col2:
        st.metric(
            label="🎯 ATS Score",
            value=f"{ats_score:.1f}%" if ats_score is not None else "--"
        )
    
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.metric(
            label="🛠 Skills",
            value=len(skills)
        )
    
    with row2_col2:
        contact_status = "✔ Verified" if email != "Not Found" and phone != "Not Found" else "⚠ Incomplete"
        st.metric(
            label="📧 Contact",
            value=contact_status
        )

    
    st.divider()

    if ats_score is not None:

        gauge = go.Figure(go.Indicator(
    
            mode="gauge+number",
    
            value=ats_score,
    
            number={
                "suffix": "%",
                "font": {"size": 46}
            },
    
            title={
                "text": "<b>ATS Score</b>",
                "font": {"size": 26}
            },
    
            gauge={
    
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "white"
                },
    
                "bar": {
                    "color": "#00D4FF"
                },
    
                "bgcolor": "rgba(0,0,0,0)",
    
                "borderwidth": 0,
    
                "steps": [
    
                    {"range": [0, 40], "color": "#E74C3C"},
    
                    {"range": [40, 70], "color": "#F39C12"},
    
                    {"range": [70, 90], "color": "#3498DB"},
    
                    {"range": [90, 100], "color": "#2ECC71"}
    
                ]
    
            }
    
        ))
    
        gauge.update_layout(
    
            height=420,
    
            paper_bgcolor="rgba(0,0,0,0)",
    
            plot_bgcolor="rgba(0,0,0,0)",
    
            font_color="white",
    
            margin=dict(l=20, r=20, t=50, b=20)
    
        )
    
        st.plotly_chart(gauge, use_container_width=True)

    st.header("📋 Contact Information")

    a, b = st.columns(2)
    a.info(f"📧 Email: {email}")
    b.info(f"📱 Phone: {phone}")

    st.header("📈 Resume Statistics")

    s1, s2, s3 = st.columns(3)
    s1.metric("Words", word_count)
    s2.metric("Characters", character_count)
    s3.metric("Pages", page_count)

    st.header("🛠 Detected Skills")

    if skills:
    
        st.markdown(
            """
            <style>
            .skill-chip{
                display:inline-block;
                padding:10px 18px;
                margin:8px;
                border-radius:25px;
                background:rgba(255,255,255,0.08);
                border:1px solid rgba(255,255,255,0.15);
                backdrop-filter:blur(15px);
                color:white;
                font-weight:600;
                transition:0.3s;
            }
    
            .skill-chip:hover{
                transform:scale(1.08);
                border:1px solid #00D4FF;
                box-shadow:0 0 15px rgba(0,212,255,.35);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
        chips = ""
    
        for skill in skills:
            chips += f'<span class="skill-chip">⚡ {skill}</span>'
    
        st.markdown(chips, unsafe_allow_html=True)
    
    else:
        st.warning("No skills detected.")

    st.header("✅ Matched Skills")

    if job_description.strip():

        if matched_skills:

            cols = st.columns(3)

            for i, skill in enumerate(matched_skills):
                cols[i % 3].success(skill)

        else:
            st.warning("No matched skills found.")

    else:
        st.info("Paste a Job Description to see matched skills.")

    st.divider()

    st.header("❌ Missing Skills")

    if job_description.strip():

        if missing_skills:

            cols = st.columns(3)

            for i, skill in enumerate(missing_skills):
                cols[i % 3].error(skill)

        else:
            st.success("Excellent! No missing skills detected.")

    else:
        st.info("Paste a Job Description to see missing skills.")

    with st.expander("📄 Resume Preview"):
        st.text_area("", resume_text, height=450)

        st.divider()

    st.divider()

    st.header("🤖 AI Resume Review")

    feedback = get_ai_feedback(
        resume_score,
        ats_score if ats_score else 0,
        matched_skills,
        missing_skills
    )

    st.markdown(feedback)

    create_pdf(
        "Resume_Report.pdf",
        email,
        phone,
        resume_score,
        ats_score if ats_score else 0,
        skills,
        matched_skills,
        missing_skills,
        feedback if job_description.strip() else ai_feedback
    )

    with open("Resume_Report.pdf", "rb") as file:
        st.download_button(
            "📥 Download PDF Report",
            file,
            file_name="Resume_Report.pdf"
        )
