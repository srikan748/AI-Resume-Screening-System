from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pdf_report import (
    generate_candidate_report
)
from typing import List

import fitz
import shutil
import os
import re

# =========================================
# AI IMPORTS
# =========================================

from sentence_transformers import (
    SentenceTransformer,
    util
)

from recruiter_engine import (
    generate_recruiter_analysis
)

# =========================================
# FASTAPI APP
# =========================================

app = FastAPI()

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# UPLOAD FOLDER
# =========================================

UPLOAD_FOLDER = "uploaded_resumes"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =========================================
# REPORT FOLDER
# =========================================

REPORT_FOLDER = "reports"
LAST_RANKINGS = []

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)

# =========================================
# STATIC FILES
# =========================================

app.mount(
    "/resumes",
    StaticFiles(directory=UPLOAD_FOLDER),
    name="resumes"
)

# =========================================
# LOAD EMBEDDING MODEL
# =========================================

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================
# SKILLS DATABASE
# =========================================

skills_db = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "SQL",
    "FastAPI",
    "Docker",
    "AWS",
    "RAG",
    "LangChain",
    "FAISS",
    "Next.js",
    "React",
    "MongoDB",
    "TensorFlow",
    "PyTorch",
    "Generative AI",
    "LLM",
    "Transformers",
    "PEFT",
    "LoRA",
    "QLoRA",
]

# =========================================
# EXTRACT PDF TEXT
# =========================================

def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:

            text += page.get_text()

        doc.close()

    except Exception as e:

        print("PDF ERROR:", e)

    return text

# =========================================
# EXTRACT SKILLS
# =========================================

def extract_skills(text):

    found_skills = []

    for skill in skills_db:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_skills.append(skill)

    return list(set(found_skills))

# =========================================
# SEMANTIC MATCH SCORE
# =========================================

def calculate_semantic_score(
    resume_text,
    job_description
):

    resume_embedding = embedding_model.encode(
        resume_text,
        convert_to_tensor=True
    )

    jd_embedding = embedding_model.encode(
        job_description,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        resume_embedding,
        jd_embedding
    )

    score = float(similarity[0][0]) * 100

    score = max(
        min(score, 100),
        0
    )

    return round(score, 2)

# =========================================
# RECOMMENDATION ENGINE
# =========================================

def get_recommendation(score):

    if score >= 85:
        return "Strong Hire"

    elif score >= 70:
        return "Hire"

    elif score >= 50:
        return "Consider"

    else:
        return "Reject"

# =========================================
# HOME ROUTE
# =========================================

@app.get("/")
def home():

    return {
        "message": "LLM-Powered Resume Screener API Running",
        "model": "Fine-Tuned Recruiter LLM"
    }

# =========================================
# RANK CANDIDATES
# =========================================

@app.post("/rank_candidates")
async def rank_candidates(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):

    global LAST_RANKINGS

    rankings = []

    jd_skills = extract_skills(
        job_description
    )

    for file in files:

        try:

            # =====================================
            # SAVE FILE
            # =====================================

            file_path = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            with open(
                file_path,
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            # =====================================
            # EXTRACT RESUME TEXT
            # =====================================

            resume_text = extract_text_from_pdf(
                file_path
            )

            if not resume_text:
                resume_text = ""

            # =====================================
            # SKILL EXTRACTION
            # =====================================

            resume_skills = extract_skills(
                resume_text
            )

            matched_skills = list(
                set(resume_skills).intersection(
                    set(jd_skills)
                )
            )

            missing_skills = list(
                set(jd_skills).difference(
                    set(resume_skills)
                )
            )

            # =====================================
            # SEMANTIC SCORE
            # =====================================

            semantic_score = calculate_semantic_score(
                resume_text,
                job_description
            )

            skill_score = (
                len(matched_skills)
                /
                max(len(jd_skills), 1)
            ) * 100

            score = round(
                (
                    semantic_score * 0.7
                    +
                    skill_score * 0.3
                ),
                2
            )

            # =====================================
            # RECOMMENDATION
            # =====================================

            recommendation = get_recommendation(
                score
            )

            # =====================================
            # AI RECRUITER ANALYSIS
            # =====================================

            analysis = generate_recruiter_analysis(
                resume_text,
                job_description
            )

            # =====================================
            # RESPONSE OBJECT
            # =====================================

            rankings.append({
                "filename": file.filename,
                "match_score": score,
                "semantic_score": round(semantic_score, 2),
                "skill_score": round(skill_score, 2),
                "skill_match_percent": round(skill_score, 2),
                "recommendation": recommendation,
                "analysis": analysis,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "matched_skills_count": len(matched_skills),
                "missing_skills_count": len(missing_skills)
            })

        except Exception as e:

            print("ERROR:", e)

            rankings.append({
                "filename": file.filename,
                "match_score": 0,
                "recommendation": "Processing Error",
                "analysis": "Failed to analyze candidate.",
                "matched_skills": [],
                "missing_skills": []
            })

    # =========================================
    # SORT RANKINGS
    # =========================================

    rankings = sorted(
        rankings,
        key=lambda x: x["match_score"],
        reverse=True
    )

    LAST_RANKINGS = rankings

    return {
        "rankings": rankings
    }

# =========================================
# COMPARE CANDIDATES
# =========================================

@app.post("/compare_candidates")
async def compare_candidates(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):

    if len(files) != 2:

        return {
            "error": "Please upload exactly 2 resumes."
        }

    candidates = []

    jd_skills = extract_skills(
        job_description
    )

    for file in files:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        resume_text = extract_text_from_pdf(
            file_path
        )

        resume_skills = extract_skills(
            resume_text
        )

        matched_skills = list(
            set(resume_skills).intersection(
                set(jd_skills)
            )
        )

        missing_skills = list(
            set(jd_skills).difference(
                set(resume_skills)
            )
        )

        semantic_score = calculate_semantic_score(
            resume_text,
            job_description
        )

        skill_score = (
            len(matched_skills)
            /
            max(len(jd_skills), 1)
        ) * 100

        final_score = round(
            (
                semantic_score * 0.7
                +
                skill_score * 0.3
            ),
            2
        )

        candidates.append({
            "filename": file.filename,
            "final_score": final_score,
            "semantic_score": round(semantic_score, 2),
            "skill_score": round(skill_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    candidate_a = candidates[0]
    candidate_b = candidates[1]

    winner = (
        candidate_a
        if candidate_a["final_score"]
        >
        candidate_b["final_score"]
        else candidate_b
    )

    reasons = []

    if (
        candidate_a["skill_score"]
        >
        candidate_b["skill_score"]
    ):
        reasons.append(
            f"{candidate_a['filename']} has better skill match."
        )

    elif (
        candidate_b["skill_score"]
        >
        candidate_a["skill_score"]
    ):
        reasons.append(
            f"{candidate_b['filename']} has better skill match."
        )

    if (
        candidate_a["semantic_score"]
        >
        candidate_b["semantic_score"]
    ):
        reasons.append(
            f"{candidate_a['filename']} has higher semantic similarity."
        )

    elif (
        candidate_b["semantic_score"]
        >
        candidate_a["semantic_score"]
    ):
        reasons.append(
            f"{candidate_b['filename']} has higher semantic similarity."
        )

    return {
        "candidate_a": candidate_a,
        "candidate_b": candidate_b,
        "winner": winner["filename"],
        "winner_score": winner["final_score"],
        "comparison_reasons": reasons
    }

# =========================================
# GENERATE REPORT
# =========================================

@app.get("/generate_report/{candidate_index}")
async def generate_report(
    candidate_index: int
):

    if len(LAST_RANKINGS) == 0:

        return {
            "error": "Run rank_candidates first."
        }

    if candidate_index >= len(LAST_RANKINGS):

        return {
            "error": "Invalid candidate index."
        }

    candidate = LAST_RANKINGS[candidate_index]

    report_path = os.path.join(
        REPORT_FOLDER,
        f"{candidate['filename']}.pdf"
    )

    generate_candidate_report(
        candidate,
        report_path
    )

    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"{candidate['filename']}_report.pdf"
    )