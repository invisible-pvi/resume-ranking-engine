from pdf_parser import parse_all_resumes
from ranker import rank_resumes
from fastapi import FastAPI, Query

main_app = FastAPI()

@main_app.get("/rank_provided_resumes")
def api_ranking_endpoint():
    with open("/Users/pavitrakamleshkumarmodi/Documents/resume-ranking-engine/job_description_folder/job_description.txt", "r") as f:
        job_description = f.read()
    resumes = parse_all_resumes("/Users/pavitrakamleshkumarmodi/Documents/resume-ranking-engine/resumes")
    ranked = rank_resumes(resumes, job_description)
    return {"results", ranked}

