import ray
import os
import re
import fitz

ray.init(ignore_reinit_error=True)

def extract_sections_from_pdf(path):
    document = fitz.open(path)
    text = ""
    for page in document:
        text = text + page.get_text()
    return text

@ray.remote
def parse_resume(path):
    extension = os.path.splitext(path)[1].lower()
    if extension == ".pdf":
        content = extract_sections_from_pdf(path)
    else:
        content = ""
    
    experience_section = re.findall(r"Experience(.*?)(?:\n\w+:|\Z)", content, re.DOTALL | re.IGNORECASE)
    projects_section = re.findall(r"Projects(.*?)(?:\n\w+:|\Z)", content, re.DOTALL | re.IGNORECASE)

    exp_text = " ".join([e.strip() for e in experience_section])
    proj_text = " ".join([p.strip() for p in projects_section])

    combined = f"{exp_text} {proj_text}".strip()

    return {
        "filename": os.path.basename(path), 
        "content": combined
    }

def parse_all_resumes(folder=""):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".pdf", ".txt"))]
    results = ray.get([parse_resume.remote(f) for f in files])
    return results
