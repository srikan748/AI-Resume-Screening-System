import pandas as pd
import json
import os

OUTPUT_FILE = "../outputs/training_dataset_v2.jsonl"

ranking_df = pd.read_csv(
    "../datasets/resume_data_for_ranking.csv"
)

resume_df = pd.read_csv(
    "../datasets/UpdatedResumeDataSet.csv"
)

training_data = []

# ==================================================
# DATASET 1
# Resume Ranking Dataset
# ==================================================

for _, row in ranking_df.iterrows():

    try:

        resume_text = f"""
Skills:
{row.get('skills','')}

Education:
{row.get('degree_names','')}

Experience:
{row.get('positions','')}

Responsibilities:
{row.get('responsibilities','')}
"""

        job_description = f"""
Job Position:
{row.get('job_position_name','')}

Required Skills:
{row.get('skills_required','')}

Education:
{row.get('educationaL_requirements','')}

Experience:
{row.get('experiencere_requirement','')}
"""

        score = int(row.get("matched_score", 50))

        if score >= 85:
            recommendation = "Strong Hire"
        elif score >= 70:
            recommendation = "Hire"
        elif score >= 50:
            recommendation = "Consider"
        else:
            recommendation = "Reject"

        sample = {
            "instruction":
            "Analyze the candidate resume against the job description and provide recruiter evaluation.",

            "input":
            f"JOB DESCRIPTION:\n{job_description}\n\nRESUME:\n{resume_text}",

            "output":
            f"Match Score: {score}\nRecommendation: {recommendation}"
        }

        training_data.append(sample)

    except Exception:
        pass


# ==================================================
# DATASET 2
# Resume Classification Dataset
# ==================================================

for _, row in resume_df.iterrows():

    try:

        category = str(row["Category"])
        resume_text = str(row["Resume"])

        sample = {

            "instruction":
            "Identify the candidate professional category from the resume.",

            "input":
            resume_text,

            "output":
            category
        }

        training_data.append(sample)

    except Exception:
        pass


# ==================================================
# SAVE
# ==================================================

os.makedirs("../outputs", exist_ok=True)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    for row in training_data:
        f.write(json.dumps(row) + "\n")

print(
    f"Dataset created with {len(training_data)} samples."
)