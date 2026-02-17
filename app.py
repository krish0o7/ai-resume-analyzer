from flask import Flask, render_template, request

app = Flask(__name__)

import re

# Predefined skill list (you can expand this later)
SKILLS_DB = [
    "python", "java", "c++", "machine learning", "data structures",
    "algorithms", "flask", "django", "react", "node.js",
    "mongodb", "sql", "html", "css", "javascript",
    "git", "github", "rest api", "communication", "problem solving"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return set(found_skills)


def analyze_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    common_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills

    if len(jd_skills) == 0:
        match_percent = 0
    else:
        match_percent = round((len(common_skills) / len(jd_skills)) * 100, 2)

    return match_percent, common_skills, missing_skills



@app.route("/", methods=["GET", "POST"])
def index():
    match = None
    common = []
    missing = []

    if request.method == "POST":
        resume = request.form["resume"]
        job_desc = request.form["job_desc"]

        match, common, missing = analyze_resume(resume, job_desc)

    return render_template("index.html", match=match, common=common, missing=missing)


if __name__ == "__main__":
    app.run(debug=True)
