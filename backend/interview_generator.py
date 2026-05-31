from transformers import pipeline


generator = None


def load_model():

    global generator

    if generator is None:

        generator = pipeline(

            "text-generation",

            model="meta-llama/Llama-3.2-1B-Instruct"
        )

    return generator


def generate_interview_questions(

    skills,

    missing_skills,

    job_description
):

    generator = load_model()

    prompt = f"""
You are an expert technical interviewer.

Job Description:
{job_description}

Candidate Skills:
{skills}

Missing Skills:
{missing_skills}

Generate:

1. Technical Questions
2. Project-Based Questions
3. Scenario-Based Questions
4. Missing Skill Questions
5. HR Questions
"""

    output = generator(

        prompt,

        max_new_tokens=250,

        do_sample=True,

        temperature=0.7
    )

    generated_text = output[0]["generated_text"]

    cleaned_response = generated_text.replace(

        prompt,

        ""

    ).strip()

    return cleaned_response