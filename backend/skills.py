skills_list = [

    # Programming
    "Python","Java","C","C++","JavaScript","TypeScript",

    # Data
    "SQL","MongoDB","PostgreSQL","MySQL",

    # ML
    "Machine Learning","Deep Learning","NLP",
    "Computer Vision","Scikit-Learn",
    "TensorFlow","PyTorch","XGBoost",

    # LLM
    "RAG","LangChain","FAISS",
    "Hugging Face","Transformers",
    "Vector Database","ChromaDB",

    # Cloud
    "AWS","Azure","GCP",

    # Backend
    "FastAPI","Flask","Django",
    "Node.js","Spring Boot",

    # Frontend
    "React","Next.js","Angular",

    # DevOps
    "Docker","Kubernetes",
    "Jenkins","GitHub Actions",

    # Data Engineering
    "Spark","Hadoop","Kafka",
    "Airflow","Databricks",

    # Analytics
    "Power BI","Tableau",
    "Pandas","NumPy"
]


def extract_skills(
    resume_text
):

    extracted_skills = []

    resume_lower = resume_text.lower()

    for skill in skills_list:

        if skill.lower() in resume_lower:

            extracted_skills.append(skill)

    return extracted_skills