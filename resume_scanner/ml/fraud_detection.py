import re
import docx2txt
import pdfplumber
import string
from collections import Counter

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def count_suspicious_phrases(text):
    phrases = [
        "ai generated", "chatgpt", "openai", "gpt3", "gpt4", "bard",
        "visionary leader", "synergy", "paradigm shift", "fastpaced",
        "selfstarter", "strategic thinker", "resultsdriven", "natural leader",
        "buzzword only", "quantum algorithms", "motivated individual", "team player",
        "growth mindset", "excellent communication skills"
    ]
    return sum(1 for phrase in phrases if phrase in text)

def keyword_stuffing_score(text):
    words = text.split()
    freq = Counter(words)
    repeated_10 = [word for word, count in freq.items() if count > 10]
    repeated_15 = [word for word, count in freq.items() if count > 15]

    top_10_words = freq.most_common(10)
    top_10_count = sum(count for _, count in top_10_words)
    top_10_ratio = top_10_count / len(words) if words else 0

    score = 0
    if len(repeated_15) > 0:
        score += 2
    if len(repeated_10) > 4:
        score += 2
    if top_10_ratio > 0.4:
        score += 2

    diversity_ratio = len(set(words)) / len(words) if words else 0
    if diversity_ratio < 0.3:
        score += 2

    return score

def missing_sections_score(text):
    sections = ["education", "skills", "projects", "experience", "certifications"]
    missing = sum(1 for section in sections if section not in text)
    return missing

def project_and_experience_score(text):
    project_keywords = ["project", "built", "developed", "created", "case study"]
    exp_keywords = ["intern", "worked", "collaborated", "implemented", "deployed"]
    projects_present = any(word in text for word in project_keywords)
    exp_present = any(word in text for word in exp_keywords)
    score = 0
    if not projects_present:
        score += 2
    if not exp_present:
        score += 2
    return score

def short_resume_score(text):
    word_count = len(text.split())
    return 2 if word_count < 100 else 0

def is_resume_fraudulent(file_path):
    filename = file_path.split('/')[-1]
    ext = filename.split('.')[-1].lower()

    if ext == 'pdf':
        with open(file_path, 'rb') as f:
            text = extract_text_from_pdf(f)
    elif ext == 'docx':
        text = extract_text_from_docx(file_path)
    else:
        return True

    text = preprocess_text(text)

    # ----- Scoring -----
    fraud_score = 0
    fraud_score += count_suspicious_phrases(text) * 2
    fraud_score += keyword_stuffing_score(text)
    fraud_score += missing_sections_score(text)
    fraud_score += project_and_experience_score(text)
    fraud_score += short_resume_score(text)

    return fraud_score >= 5
