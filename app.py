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
<h1>
🚀 AI Resume Analyzer
</h1>

<p style='text-align:center;
font-size:22px;
color:#B3B3B3;'>

Analyze your resume with ATS scoring,
skill matching and intelligent feedback.

</p>

""",unsafe_allow_html=True)
st.write("Upload your resume and compare it with a Job Description.")

left, right = st.columns(2)

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

    st.markdown("""
    <div class="glass-title">
    📊 Dashboard
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("📄 Resume Score", f"{resume_score}/100")

    c2.metric(
    "🎯 ATS Score",
    f"{ats_score:.1f}%" if ats_score is not None else "--"
    )
    
    c3.metric("🛠 Skills", len(skills))
    
    c4.metric("📧 Email", "✔" if email != "Not Found" else "✖")
    
    c5.metric("📱 Phone", "✔" if phone != "Not Found" else "✖")

    st.divider()

    if ats_score is not None:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ats_score,
            title={"text": "ATS Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 50], "color": "#ffb3b3"},
                    {"range": [50, 75], "color": "#ffe599"},
                    {"range": [75, 100], "color": "#b6fcb6"},
                ],
            },
        ))
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
        cols = st.columns(3)
        for i, skill in enumerate(skills):
            cols[i % 3].success(skill)

        fig = px.bar(
            x=skills,
            y=[1] * len(skills),
            labels={"x": "Skill", "y": "Detected"},
            title="Detected Skills"
        )
        st.plotly_chart(fig, use_container_width=True)
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
