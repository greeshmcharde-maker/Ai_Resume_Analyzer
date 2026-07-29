from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(
    filename,
    email,
    phone,
    resume_score,
    ats_score,
    skills,
    matched_skills,
    missing_skills,
    ai_feedback
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"]))
    story.append(Spacer(1,12))

    story.append(Paragraph(f"<b>Email:</b> {email}", styles["Normal"]))
    story.append(Paragraph(f"<b>Phone:</b> {phone}", styles["Normal"]))
    story.append(Spacer(1,12))

    story.append(Paragraph(f"<b>Resume Score:</b> {resume_score}/100", styles["Normal"]))
    story.append(Paragraph(f"<b>ATS Score:</b> {ats_score:.1f}%", styles["Normal"]))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Detected Skills</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(skills), styles["Normal"]))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Matched Skills</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(matched_skills), styles["Normal"]))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(missing_skills), styles["Normal"]))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>AI Feedback</b>", styles["Heading2"]))
    story.append(Paragraph(ai_feedback.replace("\n","<br/>"), styles["Normal"]))

    pdf.build(story)