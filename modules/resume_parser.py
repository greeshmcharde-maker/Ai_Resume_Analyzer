import re
import pandas as pd


def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):

    pattern = r"(\+?\d[\d\s\-]{8,}\d)"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_skills(text):

    skills = pd.read_csv("data/skills.csv", header=None)

    skills = skills[0].tolist()

    found = []

    lower_text = text.lower()

    for skill in skills:

        if skill.lower() in lower_text:
            found.append(skill)

    return sorted(list(set(found)))