import pandas as pd
import json
import random
import os

# ==========================
# PATHS
# ==========================

RESUME_DATASET = "../datasets/resume_data_for_ranking.csv"
JOB_DATASET = "../datasets/linkedin_job_postings.csv"

OUTPUT_FILE = "../outputs/training_dataset.jsonl"

# ==========================
# LOAD DATASETS
# ==========================

resume_df = pd.read_csv(RESUME_DATASET)
jobs_df = pd.read_csv(JOB_DATASET)

# ==========================
# CLEAN DATA
# ==========================


# ==========================
# CREATE OUTPUT FOLDER
# ==========================



# ==========================
# GENERATE TRAINING DATA
# ==========================

training_data = []

for i in range(len(resume_df)):

    try:

        # ----------------------
        # RESUME
        # ----------------------

        resume_row = resume_df.iloc[i]

        resume_text = " ".join(
            [str(v) for v in resume_row.values]
        )

        # ----------------------
        # RANDOM JOB
        # ----------------------

        job_row = jobs_df.sample(1).iloc[0]

        job_description = " ".join(
            [str(v) for v in job_row.values]
        )

        # ----------------------
        # SYNTHETIC SCORE
        # ----------------------

       resume_words = set(resume_text.lower().split())
       job_words = set(job_description.lower().split())

       common_skills = resume_words.intersection(job_words)

       score = min(
       95,
       40 + len(common_skills)
                )

        # ----------------------
        # TRAINING SAMPLE
        # ----------------------

        sample = {

            "instruction":
            "Evaluate the candidate resume against the job description and provide recruiter-style scoring.",

            "input":
            f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}",

            "output":
            f"Match Score: {score}\nRecommendation: {recommendation}"
        }

        training_data.append(sample)

    except Exception as e:

        print("ERROR:", e)

# ==========================
# SAVE JSONL
# ==========================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    for row in training_data:

        f.write(
            json.dumps(row) + "\n"
        )

print(f"Dataset created with {len(training_data)} samples.")