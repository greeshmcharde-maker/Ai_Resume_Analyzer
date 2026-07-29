def get_ai_feedback(resume_score, ats_score, matched_skills, missing_skills):

    feedback = []

    overall = (resume_score + ats_score) / 20
    feedback.append(f"# 🤖 AI Resume Review\n")
    feedback.append(f"## Overall Rating: {overall:.1f}/10\n")

    feedback.append("### ✅ Strengths")
    if matched_skills:
        for skill in matched_skills[:5]:
            feedback.append(f"- Strong knowledge of {skill}")
    else:
        feedback.append("- Good technical foundation.")

    feedback.append("\n### ❌ Missing Skills")
    if missing_skills:
        for skill in missing_skills:
            feedback.append(f"- Learn {skill}")
    else:
        feedback.append("- No major missing skills detected.")

    feedback.append("\n### 📄 Resume Improvements")
    feedback.append("- Add measurable achievements.")
    feedback.append("- Include certifications.")
    feedback.append("- Highlight internship experience.")
    feedback.append("- Add GitHub and LinkedIn profile.")

    feedback.append("\n### 🎯 Interview Tips")
    feedback.append("- Revise core mechanical engineering subjects.")
    feedback.append("- Prepare to explain your projects clearly.")
    feedback.append("- Practice HR interview questions.")

    return "\n".join(feedback)