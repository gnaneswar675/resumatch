# predict_eligibility.py

import os
import re
import fitz  # PyMuPDF
import docx
from sentence_transformers import SentenceTransformer, util

# Load BERT model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------------------
# 1. Extract Text from Resume
# ---------------------------
def extract_text_from_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        if ext == '.pdf':
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
        elif ext == '.docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        print("❌ Resume parsing error:", e)
        return ""

    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ---------------------------
# 2. BERT Similarity Matching
# ---------------------------
def check_eligibility_and_score(resume_text, job_description):
    if not resume_text or not job_description:
        return False, 0.0

    try:
        # Encode both texts
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        jd_embedding = model.encode(job_description, convert_to_tensor=True)

        similarity = util.cos_sim(resume_embedding, jd_embedding).item()

        # Normalize and convert to percentage
        score = max(0.0, round(similarity * 100, 2))  # Clamp to 0 if somehow negative

        # Eligibility threshold
        eligible = score >= 40

        print(f"✅ BERT Score: {score}% | Eligible: {eligible}")
        return eligible, score

    except Exception as e:
        print("❌ BERT similarity error:", e)
        return False, 0.0


# ---------------------------
# Test Run (Optional)
# ---------------------------
if __name__ == "__main__":
    resume_path = "path_to_resume.pdf"
    jd = "We are hiring a Software Developer Intern with experience in Python, Django, REST APIs, and problem-solving."
    resume_text = extract_text_from_resume(resume_path)
    result = check_eligibility_and_score(resume_text, jd)
    print(result)
