from flask import Flask, render_template, request

app = Flask(__name__)

# -----------------------------
# Helper Function: Extract Skills
# -----------------------------
def extract_skills(text, skill_list):
    found_skills = []
    text_lower = text.lower()

    for skill in skill_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        score=None,
        matched_skills=None,
        missing_skills=None,
        suggestions=None,
        structure_feedback=None
    )


# -----------------------------
# Analyze Route
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    resume_text = request.form.get("resume_text")
    job_description = request.form.get("job_description")

    if not resume_text or not job_description:
        return render_template("index.html", error="Please provide both Resume and Job Description.")

    resume_text_lower = resume_text.lower()
    job_description_lower = job_description.lower()

    # -----------------------------------
    # Define Skills (You can expand this)
    # -----------------------------------
    required_skills_master = [
        "python", "java", "c++", "flask", "django",
        "sql", "mysql", "postgresql", "mongodb",
        "javascript", "react", "node", "html", "css",
        "git", "github", "rest api", "docker",
        "aws", "data structures", "algorithms"
    ]

    # Extract skills mentioned in job description
    required_skills = extract_skills(job_description_lower, required_skills_master)

    # -----------------------------------
    # Match Skills
    # -----------------------------------
    matched_skills = extract_skills(resume_text_lower, required_skills)

    missing_skills = list(set(required_skills) - set(matched_skills))

    # -----------------------------------
    # Weighted Scoring
    # Required skills weight = 3
    # -----------------------------------
    score = 0
    total_weight = 0

    for skill in required_skills:
        total_weight += 3
        if skill in resume_text_lower:
            score += 3

    if total_weight > 0:
        final_score = round((score / total_weight) * 100, 2)
    else:
        final_score = 0

    # -----------------------------------
    # Suggestions
    # -----------------------------------
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Consider adding {skill} experience or a related project.")

    if len(resume_text.split()) < 150:
        suggestions.append("Your resume seems short. Add more detailed project descriptions.")

    if "github" not in resume_text_lower:
        suggestions.append("Add your GitHub profile link.")

    if "linkedin" not in resume_text_lower:
        suggestions.append("Add your LinkedIn profile.")

    if "project" not in resume_text_lower:
        suggestions.append("Include a dedicated Projects section.")

    # -----------------------------------
    # Resume Structure Check
    # -----------------------------------
    structure_feedback = []

    if "education" in resume_text_lower:
        structure_feedback.append("✔ Education section found")
    else:
        structure_feedback.append("✘ Education section missing")

    if "experience" in resume_text_lower:
        structure_feedback.append("✔ Experience section found")
    else:
        structure_feedback.append("✘ Experience section missing")

    if "skills" in resume_text_lower:
        structure_feedback.append("✔ Skills section found")
    else:
        structure_feedback.append("✘ Skills section missing")

    if "project" in resume_text_lower:
        structure_feedback.append("✔ Projects section found")
    else:
        structure_feedback.append("✘ Projects section missing")

    # -----------------------------------
    # Render Result Page
    # -----------------------------------
    return render_template(
        "result.html",
        score=final_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggestions=suggestions,
        structure_feedback=structure_feedback
    )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
