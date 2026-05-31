from skills import extract_skills

def analyze_skill_gap(
    resume_text,
    job_description
):

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )

    matched_skills = []

    missing_skills = []

    for skill in jd_skills:

        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    skill_match_percent = round(
        len(matched_skills)
        /
        max(len(jd_skills), 1)
        * 100,
        2
    )

    return {

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "skill_match_percent":
            skill_match_percent
    }