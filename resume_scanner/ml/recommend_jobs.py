import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_scanner.models import Job
from .predict_eligibility import extract_text_from_resume


def preprocess_text(text):
    """Clean and standardize text for vectorization."""
    if not text:
        return ""
    text = text.lower ()
    text = re.sub (r'\s+', ' ', text)
    text = text.translate (str.maketrans ('', '', string.punctuation))
    return text.strip ()


def recommend_jobs_for_resume(resume_text, job_queryset, top_n=3):
    """Recommend top N jobs based on resume similarity using TF-IDF and cosine similarity."""

    # Ensure job_queryset is a list
    if isinstance (job_queryset, Job):
        job_queryset = [job_queryset]

    # Preprocess job descriptions
    job_descriptions = [preprocess_text (job.description) for job in job_queryset]

    if not resume_text or not job_descriptions:
        return []

    # Preprocess resume text
    resume_text = preprocess_text (resume_text)
    documents = [resume_text] + job_descriptions

    # Vectorize documents
    vectorizer = TfidfVectorizer (stop_words='english')
    tfidf_matrix = vectorizer.fit_transform (documents)

    # Separate vectors
    resume_vector = tfidf_matrix[0]
    job_vectors = tfidf_matrix[1:]

    # Compute similarity scores
    similarities = cosine_similarity (resume_vector, job_vectors).flatten ()

    # Get top N indices
    ranked_indices = similarities.argsort ()[::-1][:top_n]

    # Build recommendation results
    recommended_jobs = []
    for i in ranked_indices:
        job = job_queryset[int (i)]  # Ensure index is a native Python int
        score = round (similarities[int (i)] * 100, 2)
        recommended_jobs.append ({
            "id": job.id,
            "title": job.title,
            "score": score,
            "description": job.description
        })

    return recommended_jobs
