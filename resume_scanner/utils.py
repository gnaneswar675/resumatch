import PyPDF2
import spacy
import os

nlp = spacy.load ("en_core_web_sm")


def extract_text_from_resume(resume_path):
    """Extracts text from a PDF resume"""
    text = ""
    with open (resume_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader (pdf_file)
        for page in reader.pages:
            text += page.extract_text () + "\n"
    return text


def analyze_resume(resume_text):
    """Analyzes resume text using NLP"""
    doc = nlp (resume_text)
    skills = []
    experience = []

    # Extract named entities (like skills, education, etc.)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "WORK_OF_ART", "PRODUCT"]:
            skills.append (ent.text)
        if ent.label_ == "DATE":
            experience.append (ent.text)

    return {"skills": list (set (skills)), "experience": list (set (experience))}
