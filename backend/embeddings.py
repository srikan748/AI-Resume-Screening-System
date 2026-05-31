from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def calculate_similarity(

    resume_text,

    job_description
):

    resume_embedding = embedding_model.encode(
        resume_text
    )

    jd_embedding = embedding_model.encode(
        job_description
    )

    similarity = cosine_similarity(

        [resume_embedding],

        [jd_embedding]

    )[0][0]

    return round(
        similarity * 100,
        2
    )