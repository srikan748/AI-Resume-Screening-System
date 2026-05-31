

import torch

def generate_recruiter_analysis(
    resume_text,
    job_description
):
    return """
Match Score: 85

Strengths:
- Strong technical skills
- Relevant project experience

Weaknesses:
- Limited cloud experience

Missing Skills:
- Docker
- AWS

Hiring Recommendation:
Hire
"""