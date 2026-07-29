import pandas as pd

def extract_job_skills(job_description):

    skills_db = pd.read_csv("data/skills.csv", header=None)[0].tolist()

    found = []

    for skill in skills_db:
        if skill.lower() in job_description.lower():
            found.append(skill)

    return sorted(list(set(found)))


def compare_skills(resume_skills, job_skills):

    matched = []
    missing = []

    resume_set = set(skill.lower() for skill in resume_skills)

    for skill in job_skills:
        if skill.lower() in resume_set:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing