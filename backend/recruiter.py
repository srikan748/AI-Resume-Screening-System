from transformers import pipeline

from rag_engine import retrieve_recruiter_knowledge


generator = None


def load_model():

    global generator

    if generator is None:

        generator = pipeline(

            "text-generation",

            model="meta-llama/Llama-3.2-1B-Instruct"
        )

    return generator


def generate_recruiter_feedback(

    resume,

    job_description
):

    generator = load_model()

    # ==========================================
    # RAG KNOWLEDGE RETRIEVAL
    # ==========================================

    retrieved_knowledge = retrieve_recruiter_knowledge(

        job_description
    )

    # ==========================================
    # ADVANCED RECRUITER PROMPT
    # ==========================================

    prompt = f"""
You are an enterprise AI recruiter.

Use the recruiter knowledge and job requirements
to evaluate the candidate carefully.

Recruiter Knowledge:
{retrieved_knowledge}

Job Description:
{job_description}

Candidate Resume:
{resume}

Provide detailed analysis with:

1. Match Summary

2. Candidate Strengths

3. Missing Skills

4. Hiring Recommendation

5. Resume Highlights

6. Interview Questions

7. Final Recruiter Decision
"""

    # ==========================================
    # LLM GENERATION
    # ==========================================

    output = generator(

        prompt,

        max_new_tokens=300,

        do_sample=True,

        temperature=0.7
    )

    generated_text = output[0]["generated_text"]

    # ==========================================
    # CLEAN RESPONSE
    # ==========================================

    cleaned_response = generated_text.replace(

        prompt,

        ""

    ).strip()

    return cleaned_response