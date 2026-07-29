def calculate_resume_score(email, phone, skills):

    score = 0

    if email != "Not Found":
        score += 15

    if phone != "Not Found":
        score += 15

    if len(skills) >= 5:
        score += 30

    elif len(skills) >= 3:
        score += 20

    else:
        score += 10

    score += 40

    return min(score,100)